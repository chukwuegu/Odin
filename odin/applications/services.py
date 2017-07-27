from datetime import date

from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Application, ApplicationInfo
from odin.education.models import Course
from odin.users.models import BaseUser


def create_application_info(*,
                            start_date: date,
                            end_date: date,
                            course: Course,
                            start_interview_date: date=None,
                            end_interview_date: date=None,
                            description: str=None,
                            external_application_form: str=None) -> ApplicationInfo:

    if start_date < timezone.now().date() or end_date <= timezone.now().date():
        raise ValidationError("Can not create an application in the past")

    if start_date >= end_date:
        raise ValidationError("Start date can not be after end date")

    if start_interview_date and end_interview_date:
        if start_interview_date < timezone.now().date() or end_interview_date <= timezone.now().date():
            raise ValidationError("Can not create interview dates in the past")

        if start_interview_date >= end_interview_date:
            raise ValidationError("Start interview date can not be after end interview date")

    return ApplicationInfo.objects.create(start_date=start_date,
                                          end_date=end_date,
                                          course=course,
                                          start_interview_date=start_interview_date,
                                          end_interview_date=end_interview_date,
                                          description=description,
                                          external_application_form=external_application_form)


def create_application(*,
                       application_info: ApplicationInfo,
                       user: BaseUser,
                       phone: str=None,
                       works_at: str=None,
                       studies_at: str=None,
                       has_interview_date: bool=False) -> Application:

    if not application_info.apply_is_active():
        raise ValidationError(f"The application period for {application_info.course} has expired!")

    if Application.objects.filter(user=user, application_info=application_info).exists():
        raise ValidationError(f"You have already applied for {application_info.course}.")

    return Application.objects.create(application_info=application_info,
                                      user=user,
                                      phone=phone,
                                      works_at=works_at,
                                      studies_at=studies_at,
                                      has_interview_date=has_interview_date)
