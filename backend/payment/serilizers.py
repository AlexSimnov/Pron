from rest_framework import serializers

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
        return obj.date.strftime('%Y-%m-%d %H:%M')


class PaymentSerializer(serializers.ModelSerializer):

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
    payments = PaymentReadSerializer(many=True,
                                     read_only=True)
    end_donate_date = serializers.SerializerMethodField()

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
            'payments',
        )
        read_only_fields = [
            'collected_amount',
        ]

    def get_end_donate_date(self, obj):
        return obj.end_donate_date.strftime('%Y-%m-%d %H:%M')


class CollectdonateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Collectdonate
        fields = (
            'id',
            'name',
            'occasion',
            'description',
            'free_amount',
            'end_donate_date'
        )
