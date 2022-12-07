from django.core.management import BaseCommand

from authapp.models import User
from lessons.services.pruffme import PruffMe


class Command(BaseCommand):

    def handle(self, *args, **options):
        headers = {
            'X-ALFACRM-TOKEN': settings
        }
        data = {
            'study_status_id': 1
        }
        url = f'{settings.ALFA_HOST_NAME}v2api/{1}/customer/index'
        response = requests.post(url=url, headers=headers, json=data)
        capture_message(response.json())
        try:
            student_list = response.json().get('items')
            for student in student_list:
                alfa_student = authapp.models.User.objects.filter(alfa_id=student.get("id"))
                if alfa_student:
                    pass
                else:
                    name = student.get('name').split(' ')[:2]
                    name_list = []
                    for item in name:
                        k = slugify(item.lower())
                        name_list.append(k)
                    username = f'{name_list[1][0]}.{name_list[0]}'
                    alfa_id = student.get("id")
                    first_name = name[1]
                    last_name = name[0]
                    student_phone = None
                    parent = student.get('legal_name')
                    phones = student.get('phone')
                    b_date = student.get('b_date').split(' ')[0]
                    if phones:
                        for index, phone in enumerate(phones):
                            if index == 0:
                                student_phone = phone
                                phones.remove(student_phone)
                        user = authapp.models.User.objects.create_user(username=username, first_name=first_name,
                                                                       last_name=last_name,
                                                                       phone=student_phone, password='qwe123rty456',
                                                                       birth_date=b_date,
                                                                       is_crm=True, alfa_id=alfa_id)
                    else:
                        user = authapp.models.User.objects.create_user(username=username, first_name=first_name,
                                                                       last_name=last_name,
                                                                       password='qwe123rty456',
                                                                       birth_date=b_date,
                                                                       is_crm=True, alfa_id=alfa_id)

                    if phones:
                        count = 0
                        for phone in phones:
                            if parent and count == 0:
                                profileapp.models.UserParents.objects.create(user=user, parent_phone=phone,
                                                                             full_name=parent)
                                count += 1
                            else:
                                profileapp.models.UserParents.objects.create(user=user, parent_phone=phone)
        except Exception as e:
            capture_exception(e)
