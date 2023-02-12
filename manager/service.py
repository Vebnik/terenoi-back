import re, datetime as dt

from authapp.models import User

class Utils:
  @staticmethod
  def phone_clener(phone):
    return re.sub(r'[^\d]', '', phone)

  @staticmethod
  def get_schdule_context():
    return {
      'teachers': User.objects.filter(is_teacher=True),
    }

  @staticmethod
  def serialize_date(config):
    time = config.get('lesson_start')
    date = config.get('date_start')

    start_date = [*map(int, date.split('-'))]
    time = [*map(int, time.split(':'))]

    return dt.datetime(start_date[0], start_date[1], start_date[2], time[0], time[1])

  @staticmethod
  def serialize_only_date(date_str):
    start_date = [*map(int, date_str.split('-'))]
    return dt.date(start_date[0], start_date[1], start_date[2])
