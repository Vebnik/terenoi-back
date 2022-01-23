from django.conf import settings
from pydantic import BaseModel


def create_voxi_file(func):
    def wrapper(*args, **kwargs):
        page = {
            "account_email": settings.VOXI_ACCOUNT_EMAIL,
            "account_id": settings.VOXI_ACCOUNT_ID,
            "key_id": settings.VOXI_API_KEY,
            "private_key": settings.VOXI_PRIVATE_KEY
        }

        class Private(BaseModel):
            account_email: str
            account_id: int
            key_id: str
            private_key: str

        pr = Private(**page)
        with open('authapp/json/credentials.json', 'w', encoding='utf-8') as f:
            pr.private_key = pr.private_key.replace('\\n', '\n')
            f.write(pr.json())

        func(*args, **kwargs)
        with open('authapp/json/credentials.json', 'w', encoding='utf-8') as f:
            f.write('')
    return wrapper
