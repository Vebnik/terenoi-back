from django.db import models

# Create your models here.
import authapp

NULLABLE = {'blank': True, 'null': True}


class Funnel(models.Model):
    id_amo_funnel = models.BigIntegerField(verbose_name='Айди воронки в Амо', **NULLABLE)
    name = models.CharField(verbose_name='Название воронки', **NULLABLE, max_length=255)
    is_main = models.BooleanField(verbose_name='Главная воронка', default=False)

    class Meta:
        verbose_name = 'Воронки'
        verbose_name_plural = 'Воронка'

    def __str__(self):
        return self.name


class FunnelStatus(models.Model):
    id_amo_funnel_status = models.BigIntegerField(verbose_name='Айди статуса воронки в Амо', **NULLABLE)
    name = models.CharField(verbose_name='Название воронки', **NULLABLE, max_length=255)
    funnel = models.ForeignKey(Funnel, on_delete=models.CASCADE, verbose_name='Воронка')

    class Meta:
        verbose_name = 'Статусы воронок'
        verbose_name_plural = 'Статус воронки'

    def __str__(self):
        return self.name


class Clients(models.Model):
    amo_id = models.BigIntegerField(verbose_name='Айди в Амо', **NULLABLE)
    name = models.CharField(verbose_name='Название', **NULLABLE, max_length=255)
    phone = models.CharField(verbose_name='Телефон', **NULLABLE, max_length=255)
    first_name = models.CharField(verbose_name='Имя', **NULLABLE, max_length=255)
    last_name = models.CharField(verbose_name='Фамилия', **NULLABLE, max_length=255)

    class Meta:
        verbose_name = 'Клиенты'
        verbose_name_plural = 'Клиент'

    def __str__(self):
        return f'{self.name}'


class Leads(models.Model):
    amo_id = models.BigIntegerField(verbose_name='Айди в Амо', **NULLABLE)
    name = models.CharField(verbose_name='Название', **NULLABLE, max_length=255)
    price = models.IntegerField(verbose_name='Цена', **NULLABLE)
    funnel = models.ForeignKey(Funnel, on_delete=models.CASCADE, verbose_name='Воронка')
    funnel_status = models.ForeignKey(FunnelStatus, on_delete=models.CASCADE, verbose_name='Статус воронки')
    created_at = models.DateTimeField(**NULLABLE, verbose_name='Дата создания')
    updated_at = models.DateTimeField(**NULLABLE, verbose_name='Дата обновления')
    client = models.ForeignKey(Clients, on_delete=models.CASCADE, verbose_name='Клиент', **NULLABLE)

    class Meta:
        verbose_name = 'Сделки'
        verbose_name_plural = 'Сделка'

    def __str__(self):
        return f'{self.name}'


class CustomerStatus(models.Model):
    id_amo = models.BigIntegerField(verbose_name='Айди статуса воронки в Амо', **NULLABLE)
    name = models.CharField(verbose_name='Название воронки', **NULLABLE, max_length=255)

    class Meta:
        verbose_name = 'Статусы покупателей'
        verbose_name_plural = 'Статус покупателя'

    def __str__(self):
        return self.name


class Customers(models.Model):
    amo_id = models.BigIntegerField(verbose_name='Айди в Амо', **NULLABLE)
    user = models.ForeignKey('authapp.User', on_delete=models.CASCADE, verbose_name='Пользователь Terenoi', **NULLABLE)
    name = models.CharField(verbose_name='Название', **NULLABLE, max_length=255)
    status = models.ForeignKey(CustomerStatus, on_delete=models.CASCADE, verbose_name='Статус покупателя')
    price = models.IntegerField(verbose_name='Ожидаемая сумма покупки', **NULLABLE)
    next_date = models.DateTimeField(**NULLABLE, verbose_name='Ожидаемая дата следующей покупки.')
    created_at = models.DateTimeField(**NULLABLE, verbose_name='Дата создания')
    updated_at = models.DateTimeField(**NULLABLE, verbose_name='Дата обновления')
    client = models.ForeignKey(Clients, on_delete=models.CASCADE, verbose_name='Клиент', **NULLABLE)

    class Meta:
        verbose_name = 'Покупатели'
        verbose_name_plural = 'Покупатель'

    def __str__(self):
        return self.name
