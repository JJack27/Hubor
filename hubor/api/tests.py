from django.test import TestCase
from rest_framework.test import APIRequestFactory, APIClient
import random
import datetime
# Create your tests here.
test_user = True

# Testing views_user.py
if(test_user):
    client = APIClient()
    username = str(random.random())
    last4digits = str(random.randint(1000,9999))
    email = str(random.randint(100000, 9999999)) + "@ualberta.ca"
    request_payload = {   
            "username": username,
            "email": email,
            'height': 175,
            'weight': 63,
            'user_type': 0,
            'phone':'780-995-'+last4digits,
            'date_of_birth': datetime.date(2010, 1, 1),
            'gender':0,
            'notes':'123123',
            'password':'Apple'
        }
    response = client.post('/api/register/', request_payload)
    print('======= api/register/ ========' )
    print('--- Invalid requests ---' )
    print("Status = ", response.status_code)
    for key, item in response.data['data'].items():
        if(key == 'id'):
            user_id = item
            continue
        print(key, '=' ,item)
        assert(request_payload[key] == item, "%s: request=%s resposne=%s"%(key, str(request_payload[key]), str(item)))
    username = str(random.random())
    last4digits = str(random.randint(1000,9999))
    email = str(random.randint(100000, 9999999)) + "@ualberta.ca"
    request_payload = {   
            "username": username,
            "email": email,
            'height': 175,
            'weight': 63,
            'user_type': 0,
            'phone':'780-995-'+last4digits,
            'date_of_birth': datetime.date(2222, 1, 1),
            'gender':0,
            'notes':'123123',
            'password':'Apple'
        }
    response = client.post('/api/register/', request_payload)
    print('--- Invalid requests ---' )
    print('Invalid date_of_birth')
    print("Status = ", response.status_code)
    assert(response.status_code == 401)