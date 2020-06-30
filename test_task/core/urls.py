from django.urls import path
from .views import RequestApiView, BlockedDomainApiView

urlpatterns = [
    path('request/', RequestApiView.as_view()),
    path('blocked-request/', BlockedDomainApiView.as_view())
]
