from typing import Any
from django.core.management.base import BaseCommand

from django.contrib.auth import get_user_model


from .factory import (
    UserFactory,
    PaymentFactory,
    CollectdonateFactory
    )

User = get_user_model()


class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any) -> str | None:
        UserFactory.create_batch(10)
        CollectdonateFactory.create_batch(3)
        PaymentFactory.create_batch(10)
