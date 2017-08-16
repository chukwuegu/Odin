from django.db import transaction

from typing import Dict, BinaryIO

from .models import GraderBinaryProblem, GraderPlainProblem
from .validators import run_create_problem_service_validation
from .tasks import submit_solution


def create_plain_problem(*,
                         language: str='',
                         test_type: int=GraderPlainProblem.UNITTEST,
                         file_type: int=GraderPlainProblem.PLAIN,
                         solution: str=None,
                         test: str=None,
                         extra_options: Dict={}) -> GraderPlainProblem:

    run_create_problem_service_validation(language=language,
                                          test_type=test_type,
                                          file_type=file_type)

    return GraderPlainProblem.objects.create(
        language=language,
        test_type=test_type,
        file_type=file_type,
        solution=solution,
        test=test,
        extra_options=extra_options
    )


def create_binary_problem(*,
                          language: str='',
                          test_type: int=GraderBinaryProblem.UNITTEST,
                          file_type: int=GraderBinaryProblem.BINARY,
                          solution: BinaryIO=None,
                          test: BinaryIO=None,
                          extra_options: Dict={}) -> GraderBinaryProblem:

    run_create_problem_service_validation(language=language,
                                          test_type=test_type,
                                          file_type=file_type)

    return GraderBinaryProblem.objects.create(
        language=language,
        test_type=test_type,
        file_type=file_type,
        solution=solution,
        test=test,
        extra_options=extra_options
    )


def start_grader_communication(solution_id: int):
    transaction.on_commit(lambda: submit_solution.delay(solution_id))