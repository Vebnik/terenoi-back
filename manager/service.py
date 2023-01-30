import re


class CleanData:
  @staticmethod
  def phone_clener(phone):
    return re.sub(r'[^\d]', '', phone)