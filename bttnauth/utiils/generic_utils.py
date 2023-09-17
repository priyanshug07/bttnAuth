from datetime import datetime
from django.utils import timezone
import uuid


def check_token_sanity(expiry_date):
    return expiry_date > timezone.now()

def get_new_auth_token():
    return uuid.uuid4()
