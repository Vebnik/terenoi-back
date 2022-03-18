import calendar

from dateutil.rrule import rrule, WEEKLY
from django.db.models.signals import post_save
from django.dispatch import receiver

from lessons.models import ScheduleSettings, Lesson


@receiver(post_save, sender=ScheduleSettings)
def add_schedule(sender, instance, **kwargs):
    lesson = Lesson.objects.filter(student=instance.shedule.student, teacher=instance.shedule.teacher,
                                   date=instance.near_lesson)
    if lesson:
        pass
    else:
        number_list = []
        for i in instance.shedule.weekday.all().values('number'):
            number_list.append(i['number'])
        date_list = rrule(freq=WEEKLY, dtstart=instance.near_lesson, count=instance.count,
                          wkst=calendar.firstweekday(),
                          byweekday=number_list)

        len_date_list = len(list(date_list))
        for i, date in enumerate(list(date_list)):
            Lesson.objects.create(student=instance.shedule.student, teacher=instance.shedule.teacher,
                                  subject=instance.shedule.subject, date=date)
            if i == len_date_list - 1:
                instance.last_lesson = date
                instance.save()
