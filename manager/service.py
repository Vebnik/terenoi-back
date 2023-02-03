import re


class Utils:
  @staticmethod
  def phone_clener(phone):
    return re.sub(r'[^\d]', '', phone)