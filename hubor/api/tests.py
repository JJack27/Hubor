from django.test import TestCase
from rest_framework.test import APIRequestFactory, APIClient
import random
import datetime
from accounts.models import User
# Create your tests here.
test_user = True

# Testing views_user.py
if(test_user):
    client = APIClient()
    
    print('======= api/register/ ========' )
    print('--- Valid requests ---' )
    username = str(random.random())
    last4digits = str(random.randint(1000,9999))
    email = str(random.randint(100000, 9999999)) + "@ualberta.ca"
    password = "Apple"
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
            'password':password
        }
    response = client.post('/api/register/', request_payload)
    print("Status = ", response.status_code)
    for key, item in response.data['data'].items():
        if(key == 'id'):
            user_id = item
            continue
        print(key, '=' ,item)
        assert(request_payload[key] == item, "%s: request=%s resposne=%s"%(key, str(request_payload[key]), str(item)))
    
    print('--- Invalid requests ---' )
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
    print('* date_of_birth *')
    response = client.post('/api/register/', request_payload)
    print("Status = ", response.status_code)
    assert(response.status_code == 401)
    print("OK")
    
    print("* user_type * ")
    request_payload['user_type'] = 4
    response = client.post('/api/register/', request_payload)
    print("Status = ", response.status_code)
    request_payload['user_type'] = 1
    assert(response.status_code == 401)
    print("OK")

    print('* gender *')
    request_payload['gender'] = 4
    response = client.post('/api/register/', request_payload)
    print("Status = ", response.status_code)
    request_payload['gender'] = 1
    assert(response.status_code == 401)
    print("OK")

    print('* notes *')
    request_payload['notes'] = "".join(['x' for _ in range(801)])
    response = client.post('/api/register/', request_payload)
    print("Status = ", response.status_code)
    request_payload['notes'] = '123'
    assert(response.status_code == 401)
    print("OK")
    print("======= api/login/ ========")
    print('--- Valid requests ---' )
    user = User.objects.get(id=user_id)
    response = client.post('/api/login/', {'username': user.username, 'password':password})
    print(response.status_code, response.data)

    print("======= api/logout/ ========")
    print('--- Valid requests ---' )
    response = client.post('/api/logout/', {})
    print(response.status_code, response.data)