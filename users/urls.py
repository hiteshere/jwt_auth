from django.conf.urls import url
from .views import CreateUserAPIView, authenticate_user, UserRetrieveUpdateAPIView, JobRetrieveUpdateAPIView

urlpatterns = [
    url(r'^create/$', CreateUserAPIView.as_view()),
    url(r'^obtain_token/$', authenticate_user),
    url(r'^update/$', UserRetrieveUpdateAPIView.as_view()),
    url(r'^dashboard_details/$', UserRetrieveUpdateAPIView.as_view()),
    url(r'^job_details/$', JobRetrieveUpdateAPIView.as_view()),
]
