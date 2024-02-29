import factory
from factory.django import DjangoModelFactory

from payment.models import Collectdonate, Payment

from django.contrib.auth import get_user_model


User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    email = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')


class CollectdonateFactory(DjangoModelFactory):
    class Meta:
        model = Collectdonate

    user = factory.SubFactory(UserFactory)
    name = factory.Faker('word')
    occasion = 'свадьба'
    description = factory.Faker('text')
    free_amount = 100000.00
    collected_amount = 0.00
    end_donate_date = factory.Faker('date_time')
    image = factory.django.ImageField(filename='test.jpg')


class PaymentFactory(DjangoModelFactory):
    class Meta:
        model = Payment

    user = factory.SubFactory(UserFactory)
    name = factory.SubFactory(CollectdonateFactory)
    pay = 150.00
    date = factory.Faker('date_time')
