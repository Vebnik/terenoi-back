import re

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