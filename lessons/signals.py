import calendar

from dateutil.rrule import rrule, WEEKLY
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from lessons.models import ScheduleSettings, Lesson, Schedule


@receiver(post_save, sender=ScheduleSettings)
def add_schedule_settings(sender, instance, **kwargs):

    print('in add_schedule_settings', instance)
    return

    lesson = Lesson.objects.filter(group=instance.shedule.group, teacher=instance.shedule.teacher,
                                   date=instance.near_lesson)

    lesson_last = Lesson.objects.filter(group=instance.shedule.group, teacher=instance.shedule.teacher,
                                   date=instance.last_lesson)
    if lesson or lesson_last:
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
            new_lesson = Lesson.objects.create(teacher=instance.shedule.teacher,
                                  subject=instance.shedule.subject, date=date, schedule=instance.shedule, group=instance.shedule.group)
            for student in instance.shedule.students.all():
                new_lesson.students.add(student)
            new_lesson.save()
            if i == len_date_list - 1:
                instance.last_lesson = date
                instance.save()


@receiver(pre_save, sender=Schedule)
def add_schedule(sender, instance, **kwargs):
    try:
        old_instance = Schedule.objects.get(id=instance.id)
        lessons = Lesson.objects.filter(group=instance.group, teacher=old_instance.teacher,
                                        subject=instance.subject)
        lessons.update(teacher=instance.teacher)
    except Schedule.DoesNotExist:
        return None
