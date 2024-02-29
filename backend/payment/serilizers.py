from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from .models import Collectdonate, Payment


class PaymentReadSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    date = serializers.SerializerMethodField()
    name = serializers.StringRelatedField()

    class Meta:
        model = Payment
        fields = [
            'id',
            'pay',
            'date',
            'user',
            'name'
        ]

    def get_date(self, obj):
        if isinstance(obj, dict):
            return obj['date'].strftime('%Y-%m-%d %H:%M')
        return obj.date.strftime('%Y-%m-%d %H:%M')


class PaymentSerializer(serializers.ModelSerializer):
    name = serializers.PrimaryKeyRelatedField(
        queryset=Collectdonate.objects.all(),
        required=True)

    class Meta:
        model = Payment
        fields = [
            'id',
            'pay',
            'date',
            'name'
        ]


class CollectdonateReadSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    payments = PaymentReadSerializer(many=True)
    end_donate_date = serializers.SerializerMethodField()
    image = serializers.ReadOnlyField(source='image.url')

    class Meta:
        model = Collectdonate
        fields = (
            'id',
            'name',
            'occasion',
            'description',
            'free_amount',
            'collected_amount',
            'end_donate_date',
            'user',
            'image',
            'payments',
        )
        read_only_fields = [
            'collected_amount',
        ]

    def get_end_donate_date(self, obj):
        return obj.end_donate_date.strftime('%Y-%m-%d %H:%M')


class CollectdonateSerializer(serializers.ModelSerializer):
    image = Base64ImageField(use_url=True)

    class Meta:
        model = Collectdonate
        fields = (
            'id',
            'name',
            'occasion',
            'description',
            'free_amount',
            'image',
            'end_donate_date'
        )
