from django.conf.urls import url, include

from .views import TempDashboardIndexView

urlpatterns = [
    url(
        regex='^$',
        view=TempDashboardIndexView.as_view(),
        name='index'
    ),
    url(
        regex='^education/',
        view=include('odin.education.urls', namespace='education')
    ),
    url(
        regex='^management/',
        view=include('odin.management.urls', namespace='management')
    ),
    url(
        regex='^users/',
        view=include('odin.users.urls', namespace='users')
    ),
    url(
        regex='^applications/',
        view=include('odin.applications.urls', namespace='applications')
    ),
    url(
        regex='^competitions/',
        view=include('odin.competitions.urls', namespace='competitions')
    ),
    url(
        regex='^interviews/',
        view=include('odin.interviews.urls', namespace='interviews')
    ),
]
