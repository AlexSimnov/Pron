from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.conf import settings
from django.views.decorators.vary import vary_on_cookie

from .permissions import AuthorOrReadOnly

from .models import Collectdonate, Payment

from .serilizers import (
    CollectdonateReadSerializer,
    PaymentSerializer,
    PaymentReadSerializer,
    CollectdonateSerializer,
    )


class CollectdonateViewSet(viewsets.ModelViewSet):
    queryset = Collectdonate.objects.all()
    permission_classes = [AuthorOrReadOnly]

    @method_decorator(cache_page(settings.CACHE_TIME))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request):
        serializer = CollectdonateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(status=status.HTTP_201_CREATED,
                            data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data=serializer.errors)

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return CollectdonateReadSerializer
        return CollectdonateSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    permission_classes = [AuthorOrReadOnly]

    def get_queryset(self):
        queryset = Payment.objects.filter(
            user=self.request.user.id
            ).order_by('-pay').values()
        return queryset

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return PaymentReadSerializer
        return PaymentSerializer

    @method_decorator(cache_page(settings.CACHE_TIME))
    @method_decorator(vary_on_cookie)
    def list(self, request):
        return super().list(request)

    def create(self, request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(status=status.HTTP_201_CREATED,
                            data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data=serializer.errors)
