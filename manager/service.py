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
    date = config.get('date_range')

    start_date = [*map(int, date.split(' to ')[0].split('-'))]
    end_date = [*map(int, date.split(' to ')[1].split('-'))]
    time = [*map(int, time.split(':'))]

    start_date = dt.datetime(start_date[0], start_date[1], start_date[2], time[0], time[1])
    end_date = dt.datetime(end_date[0], end_date[1], end_date[2], time[0], time[1])

    return {
      'start_date': start_date, 
      'end_date': end_date
    }

  @staticmethod
  def serialize_only_date(date_str):
    if 'to' in date_str:
      start_date = [*map(int, date_str.split(' to ')[0].split('-'))]
      end_date = [*map(int, date_str.split(' to ')[1].split('-'))]

      start_date = dt.date(start_date[0], start_date[1], start_date[2])
      end_date = dt.date(end_date[0], end_date[1], end_date[2])

      return {
        'start_date': start_date, 
        'end_date': end_date
      }

    start_date = [*map(int, date_str.split('-'))]
    start_date = dt.date(start_date[0], start_date[1], start_date[2])

    return {
      'start_date': start_date, 
    }
