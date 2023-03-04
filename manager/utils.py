from authapp.models import User
from finance.models import StudentBalance


def get_context_student_data():
    students = User.objects.filter(is_student__exact=True)
    balance = StudentBalance.objects.all()

    data = []

    for student in students:
        student.balance = balance.get(user_id=student.id)
        
        data.append(student)

    return data