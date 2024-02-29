from django.db import models

from django.core.validators import MinValueValidator

from django.contrib.auth import get_user_model

from .tasks import send_successful_email_message

User = get_user_model()


class Collectdonate(models.Model):

    CHOICES = (
        ('свадьба', 'свадьба'),
        ('день рождения', 'день рождения'),
        ('новый год', 'новый год')
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='collectdonates'
    )
    name = models.CharField(
        'название',
        max_length=50,
        blank=False,
        null=False
    )
    occasion = models.CharField(
        max_length=300,
        choices=CHOICES
    )
    description = models.TextField(
        'описание',
        max_length=256,
        blank=False,
        null=False
    )
    free_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)]
    )
    collected_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        default=0
    )
    end_donate_date = models.DateTimeField(
        blank=False,
        null=False
    )
    image = models.ImageField()

    def __str__(self) -> str:
        return f'{self.name}'

    def save(self, *args, **kwargs):
        send_successful_email_message.delay(
            self.user.email,
            self.name)
        return super().save(*args, **kwargs)


class Payment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='payments'
    )
    name = models.ForeignKey(
        Collectdonate,
        on_delete=models.SET_NULL,
        related_name='payments',
        null=True,
        blank=True
    )
    pay = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,
        blank=False,
        validators=[MinValueValidator(0)]
    )
    date = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self) -> str:
        return '{}, {}, {}'.format(
            self.pay, self.get_date, self.user.username
        )

    def save(self, *args, **kwargs):
        self.name.collected_amount += self.pay
        self.name.save()
        send_successful_email_message.delay(
            self.user.email,
            self.name.name)
        return super().save(*args, **kwargs)
