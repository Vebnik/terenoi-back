from django.db import models

from profileapp.models import Subject

NULLABLE = {'blank': True, 'null': True}
TENGE = 'KZT'
DOLLARS = 'USD'
CURRENCY_CHOICES = (
    (TENGE, 'KZT'),
    (DOLLARS, 'USD')
)


class ReferralSettings(models.Model):
    lesson_count = models.IntegerField(verbose_name='Кол-во уроков для ученика', **NULLABLE)
    friend_lesson_count = models.IntegerField(verbose_name='Кол-во уроков для ученика,которого пригласили', **NULLABLE)
    amount = models.IntegerField(verbose_name='Сумма выплаты для учителя', **NULLABLE)
    friend_amount = models.IntegerField(verbose_name='Сумма выплаты для учителя,которого пригласили', **NULLABLE)
    currency = models.CharField(verbose_name='Валюта', choices=CURRENCY_CHOICES, default=TENGE, max_length=5)

    class Meta:
        verbose_name = 'Реферальная система'
        verbose_name_plural = 'Реферальная система'

    def save(self, *args, **kwargs):
        self.__class__.objects.exclude(id=self.id).delete()
        super(ReferralSettings, self).save(*args, **kwargs)


class RateTeachers(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name='Предмет')
    rate = models.IntegerField(verbose_name='Ставка')

    class Meta:
        verbose_name = 'Ставка учителя по-умолчанию'
        verbose_name_plural = 'Ставки учителя по-умолчанию'

    def save(self, *args, **kwargs):
        subjects = RateTeachers.objects.filter(subject=self.subject)
        if not subjects:
            super(RateTeachers, self).save(*args, **kwargs)
        else:
            RateTeachers.objects.get(subject=self.subject).delete()
            super(RateTeachers, self).save(*args, **kwargs)


class DeadlineSettings(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name='Предмет')
    day_count = models.IntegerField(verbose_name='Кол-во дней')

    class Meta:
        verbose_name = 'Дедлайн для домашнего задания'
        verbose_name_plural = 'Дедлайн для домашнего задания'

    def save(self, *args, **kwargs):
        subjects = DeadlineSettings.objects.filter(subject=self.subject)
        if not subjects:
            super(DeadlineSettings, self).save(*args, **kwargs)
        else:
            DeadlineSettings.objects.get(subject=self.subject).delete()
            super(DeadlineSettings, self).save(*args, **kwargs)


class CityTimeZone(models.Model):
    city = models.CharField(verbose_name='Город', max_length=150)
    time_zone = models.CharField(verbose_name='Часовой пояс', max_length=15)

    class Meta:
        verbose_name = 'Город и часовой пояс'
        verbose_name_plural = 'Города и часовые пояса'

    def save(self, *args, **kwargs):
        city = CityTimeZone.objects.filter(city=self.city)
        if not city:
            super(CityTimeZone, self).save(*args, **kwargs)
        else:
            CityTimeZone.objects.get(city=self.city).delete()
            super(CityTimeZone, self).save(*args, **kwargs)
