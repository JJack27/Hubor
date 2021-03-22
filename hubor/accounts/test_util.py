import random
import uuid
import datetime
import pytz
from accounts.models import *

def logout(client):
    return client.post('/api/logout/', {})

def login(client, user):
    password = "Apple"
    return client.post('/api/login/', {'username': user.username, 'password':password})

def create_user(client, user_type):
    username = str(random.random())
    last7digits = str(random.randint(1000000,9999999))
    email = str(random.randint(100000, 9999999)) + "@ualberta.ca"
    password = "Apple"
    request_payload = {   
            "username": username,
            "email": email,
            'height': 175,
            'weight': 63,
            'user_type': user_type,
            'first_name': 'Yizhou',
            'last_name':'Zhao',
            'phone':'780'+last7digits,
            'date_of_birth': datetime.datetime.now(tz=pytz.timezone("UTC")) - datetime.timedelta(days=90),
            'gender':0,
            'notes':'123123',
            'password':password
        }
    response = client.post('/api/register/', request_payload)
    user = User.objects.get(id=response.data['data']['id'])
    return user

def create_facility(client, name):
    request_payload = {}
    last7digits = str(random.randint(1000000,9999999))
    address = str(random.randint(1000000,9999999))
    request_payload['name'] = name
    request_payload['phone'] = '780'+last7digits
    request_payload['address'] = address
    request_payload['description'] = address
    response = client.post('/api/facilities/', request_payload)
    facility = Facilities.objects.get(id=response.data['id'])
    return facility