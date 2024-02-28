from django.db import models

from django.core.validators import MinValueValidator

from django.contrib.auth import get_user_model

User = get_user_model()


class Collectdonate(models.Model):

    CHOICES = (
        ('wed', 'свадьба'),
        ('br', 'день рождения'),
        ('ne', 'новый год')
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

    def __str__(self) -> str:
        return f'{self.name}'

    def save(self, *args, **kwargs):
        # def send_email
        return super(Collectdonate, self).save(*args, **kwargs)


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

    @property
    def get_date(self):
        return self.date.strftime('%Y-%m-%d %H:%M')

    def __str__(self) -> str:
        return '{}, {}, {}'.format(
            self.pay, self.get_date, self.user.username
        )

    def save(self, *args, **kwargs):
        self.name.collected_amount += self.pay
        self.name.save()
        return super(Payment, self).save(*args, **kwargs)
