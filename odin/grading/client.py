import hashlib
import hmac
import json
import requests
import time
from typing import Dict, Callable

from django.conf import settings
from django.apps import apps
from django.shortcuts import get_object_or_404

from .models import GraderRequest
from.exceptions import PollingError


class GraderClient:
    def __init__(self,
                 solution_model_repr: str,
                 settings_module=settings,
                 grader_ready_data: Dict=None):

        self.settings = settings
        self.data = grader_ready_data
        self.solution_model_repr = solution_model_repr
        self.solution_model = apps.get_model(solution_model_repr)
        self.req_and_resource = self._generate_req_and_resource()

    def _generate_req_and_resource(self) -> Dict[str, str]:
        req_and_resource = {}
        req_and_resource['GET'] = f'GET {self.settings.GRADER_GRADE_PATH}'
        req_and_resource['POST'] = f'POST {self.settings.GRADER_GRADE_PATH}'
        return req_and_resource

    def _generate_grader_headers(self, body: Dict, req_and_resource: str) -> Dict:
        nonce = self._get_and_update_req_nonce(req_and_resource)
        date = time.strftime("%c")
        msg = body + date + nonce
        digest = hmac.new(bytearray(settings.GRADER_API_SECRET.encode('utf-8')),
                          msg=msg.encode('utf-8'),
                          digestmod=hashlib.sha256).hexdigest()

        request_headers = {'Authentication': digest,
                           'Date': date,
                           'X-API-Key': settings.GRADER_API_KEY,
                           'X-Nonce-Number': nonce}

        return request_headers

    def _get_and_update_req_nonce(self, req_and_resource: str) -> str:
        request = GraderRequest.objects.filter(request_info=req_and_resource).first()

        if request is not None:
            nonce = request.nonce
            nonce += 1
            request.nonce = nonce
            request.save()
            return str(nonce)

        nonce = 1
        GraderRequest.objects.create(nonce=nonce, request_info=req_and_resource)
        return str(nonce)

    def _update_req_and_resource_nonce(self, req_and_resource: str, nonce: int):
        grader_request = get_object_or_404(GraderRequest, request_info=req_and_resource)
        grader_request.nonce = nonce
        grader_request.save()

    def _get_valid_nonce(self, req_and_resource: str):
        get_nonce_url = settings.GRADER_ADDRESS + settings.GRADER_GET_NONCE_PATH

        headers = {
            'Request-Info': req_and_resource,
            'X-USER-Key': settings.GRADER_API_KEY
        }
        response = requests.get(get_nonce_url, headers=headers)
        nonce = response.json()["nonce"]
        self._update_req_and_resource_nonce(req_and_resource, nonce)

    def submit_request_to_grader(self, solution_id: int, polling_task: Callable):
        """
        The task is waiting 202 status code. The infinite loop is to get right nonce.
        """
        solution = self.solution_model.objects.get(id=solution_id)
        url = self.settings.GRADER_ADDRESS + self.settings.GRADER_GRADE_PATH
        body = json.dumps(self.data)
        while True:
            headers = self._generate_grader_headers(body, self.req_and_resource['POST'])

            response = requests.post(url, json=self.data, headers=headers)

            if response.status_code == 202:
                solution.status = self.solution_model.PENDING
                solution.build_id = response.json()['run_id']
                solution.check_status_location = response.headers['Location']
                solution.save()

                polling_task.delay(solution.id, self.solution_model_repr)
                break
            elif response.status_code == 403 and response.text == "Nonce check failed":
                self._get_valid_nonce(self.req_and_resource['POST'])
            else:
                solution.status = self.solution_model.NOT_OK
                solution.save()
                break

    def poll_grader(self, solution_id: int):
        solution = self.solution_model.objects.get(id=solution_id)

        path = self.settings.GRADER_CHECK_PATH.format(build_id=solution.build_id)
        url = solution.check_status_location
        req_and_resource = self.req_and_resource['GET']

        headers = self._generate_grader_headers(path, req_and_resource)
        response = requests.get(url, headers=headers)
        if response.status_code == 403 and response.text == "Nonce check failed":
            self._get_valid_nonce(req_and_resource)
            raise PollingError(response.text)

        elif response.status_code == 200:
            data = response.json()

            if data['result_status'] == 'ok':
                solution.status = self.solution_model.OK
            elif data['result_status'] == 'not_ok':
                solution.status = self.solution_model.NOT_OK

            solution.test_output = data['output']
            solution.save()
        else:
            raise PollingError("Grading not finished yet")

    def __str__(self):
        return self.data
