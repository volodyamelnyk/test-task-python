from django.shortcuts import render
from rest_framework import generics
from .models import Request, BlockedDomain
from .serializers import RequestSerializer, BlockedDomainSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
# Create your views here.


class RequestApiView(generics.CreateAPIView, generics.ListAPIView):
    queryset = Request.objects.filter(is_blocked=False)
    serializer_class = RequestSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        request.data['ip'] = ip
        return self.create(request, *args, **kwargs)

class BlockedDomainApiView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = BlockedDomainSerializer
