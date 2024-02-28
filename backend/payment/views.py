from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

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

    def create(self, request, *args, **kwargs):
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
        queryset = Payment.objects.filter(user=self.request.user.id)
        return queryset

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return PaymentReadSerializer
        return PaymentSerializer

    def create(self, request, *args, **kwargs):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(status=status.HTTP_201_CREATED,
                            data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data=serializer.errors)
