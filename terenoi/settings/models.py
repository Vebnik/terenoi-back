from django.db import models

NULLABLE = {'blank': True, 'null': True}
TENGE = 'KZT'
DOLLARS = 'USD'
CURRENCY_CHOICES = (
    (TENGE, 'KZT'),
    (DOLLARS, 'USD')
)


class ReferralSettings(models.Model):
    lesson_count = models.IntegerField(verbose_name='Кол-во уроков для ученика', **NULLABLE)
    amount = models.IntegerField(verbose_name='Сумма выплаты для учителя', **NULLABLE)
    currency = models.CharField(verbose_name='Валюта', choices=CURRENCY_CHOICES, default=TENGE, max_length=5)

    class Meta:
        verbose_name = 'Реферальная система'
        verbose_name_plural = 'Реферальная система'

    def save(self, *args, **kwargs):
        self.__class__.objects.exclude(id=self.id).delete()
        super(ReferralSettings, self).save(*args, **kwargs)
