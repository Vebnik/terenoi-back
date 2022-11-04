from django.contrib.sessions.models import Session
from django.db import models
from authapp.models import User

NULLABLE = {'blank': True, 'null': True}


class AbstractNotification(models.Model):
    to_user = models.ForeignKey(User, verbose_name='Уведомлениe пользователя', on_delete=models.CASCADE)
    lesson_id = models.IntegerField(verbose_name='Номер урока', **NULLABLE)
    lesson_date = models.DateTimeField(verbose_name='Дата урока', **NULLABLE)
    payment_date = models.DateTimeField(verbose_name='Дата оплаты', **NULLABLE)
    message = models.CharField(max_length=255, verbose_name='Сообщение', **NULLABLE)
    is_read = models.BooleanField(default=False, verbose_name='Просмотрено')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')

    class Meta:
        abstract = True


class Notification(AbstractNotification):
    LESSON_SCHEDULED = 'LSN_SCH'
    LESSON_COMING_SOON = 'LSN_CMN'
    LESSON_PROGRESS = 'LSN_PRG'
    LESSON_DONE = 'LSN_DN'
    LESSON_REQUEST_RESCHEDULED = 'LSN_REQ_RESCH'
    LESSON_RESCHEDULED = 'LSN_RESCH'
    LESSON_REQUEST_CANCEL = 'LSN_REQ_CNL'
    LESSON_CANCEL = 'LSN_CNL'

    CHOICES_NOTIFICATIONS = (
        (LESSON_SCHEDULED, 'Урок назначен'),
        (LESSON_COMING_SOON, 'Урок скоро состоится'),
        (LESSON_PROGRESS, 'Урок идет'),
        (LESSON_DONE, 'Урок проведен'),
        (LESSON_REQUEST_RESCHEDULED, 'Запрос на перенос урока'),
        (LESSON_REQUEST_CANCEL, 'Запрос на отмену урока'),
        (LESSON_RESCHEDULED, 'Урок перенесен'),
        (LESSON_CANCEL, 'Урок отменен')
    )

    type = models.CharField(max_length=20, choices=CHOICES_NOTIFICATIONS, verbose_name='Тип уведомления', **NULLABLE)

    class Meta:
        verbose_name = 'Уведомление по уроку'
        verbose_name_plural = 'Уведомления по урокам'


class PaymentNotification(AbstractNotification):
    PAID = 'PD'
    AWAITING_PAYMENT = 'AP'
    WITHDRAWALS = 'WD'
    ENROLLMENT_REF = 'EN_REF'
    CHOICES_NOTIFICATIONS = (
        (PAID, 'Оплачено'),
        (AWAITING_PAYMENT, 'Ожидает оплаты'),
        (WITHDRAWALS, 'Вывод средств'),
        (ENROLLMENT_REF, 'Зачисление реферальной программы'),
    )
    type = models.CharField(max_length=20, choices=CHOICES_NOTIFICATIONS, verbose_name='Тип уведомления', **NULLABLE)

    class Meta:
        verbose_name = 'Уведомление об оплате'
        verbose_name_plural = 'Уведомления об оплате'


class ManagerNotification(models.Model):
    NEW_USER = 'NU'
    REQUEST_LESSON_RESCHEDULED = 'REQ_LSN_RESCH'
    REQUEST_LESSON_CANCEL = 'REQ_LSN_CNL'
    REQUEST_REJECT_STUDENT = 'REQ_RJC_U'
    REQUEST_CHANGE_PASS = 'REQ_CHN_PSS'
    LESSON_RATE_HIGH = 'LESS_RT_HGH'
    LESSON_RATE_LOW = 'LESS_RT_HGH'

    CHOICES_NOTIFICATIONS = (
        (NEW_USER, 'Новый пользователь'),
        (REQUEST_LESSON_RESCHEDULED, 'Запрос на перенос урока'),
        (REQUEST_LESSON_CANCEL, 'Запрос на отмену урока'),
        (REQUEST_REJECT_STUDENT, 'Запрос на отказ от ученика'),
        (REQUEST_CHANGE_PASS, 'Запрос на смену пароля'),
        (LESSON_RATE_LOW, 'Оценка за урок не удовлетворительная'),
        (LESSON_RATE_HIGH, 'Оценка за урок высокая')
    )

    manager = models.ForeignKey(User, verbose_name='Менежер', on_delete=models.CASCADE,
                                related_name='manager_notification')
    lesson_id = models.IntegerField(verbose_name='Номер урока', **NULLABLE)
    to_user = models.ForeignKey(User, verbose_name='Пользователь,который поставил оценку к уроку',
                                on_delete=models.CASCADE, related_name='user_notification', **NULLABLE)
    type = models.CharField(max_length=20, choices=CHOICES_NOTIFICATIONS, verbose_name='Тип уведомления', **NULLABLE)
    is_read = models.BooleanField(default=False, verbose_name='Просмотрено')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')

    class Meta:
        verbose_name = 'Уведомление для менеджера'
        verbose_name_plural = 'Уведомления для менеджеров'


class HomeworkNotification(AbstractNotification):
    HOMEWORK_ADD = 'HM_ADD'
    HOMEWORK_CHECK = 'HM_CHK'

    CHOICES_NOTIFICATIONS = (
        (HOMEWORK_ADD, 'Домашнее задание добавлено'),
        (HOMEWORK_CHECK, 'Домашнее задание проверено'),
    )
    type = models.CharField(max_length=20, choices=CHOICES_NOTIFICATIONS, verbose_name='Тип уведомления', **NULLABLE)

    class Meta:
        verbose_name = 'Уведомление по домашнему заданию'
        verbose_name_plural = 'Уведомления по домашним заданиям'


class LessonRateNotification(AbstractNotification):
    LESSON_RATE_HIGH = 'LESS_RT_HGH'
    LESSON_RATE_LOW = 'LESS_RT_LOW'

    CHOICES_NOTIFICATIONS = (
        (LESSON_RATE_HIGH, 'Урок оценен высоко'),
        (LESSON_RATE_LOW, 'Урок оценен не удовлетворительно'),
    )
    type = models.CharField(max_length=20, choices=CHOICES_NOTIFICATIONS, verbose_name='Тип уведомления', **NULLABLE)

    class Meta:
        verbose_name = 'Уведомление по оценке урока'
        verbose_name_plural = 'Уведомления по оценке урока'
