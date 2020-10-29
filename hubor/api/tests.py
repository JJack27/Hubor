from django.test import TestCase
from rest_framework.test import APIRequestFactory, APIClient
import random
import uuid
import datetime
from accounts.models import *
from data.models import *
import test_user as user_test
import test_data as data_test

# Create your tests here.
test_user = False
test_data = False
test_emergency = False
test_config = True

# Testing views_user.py
if(test_user):
    user_test.run()

# Testing views_data.py
if(test_data):
    data_test.run()


if(test_emergency):
    client = APIClient()
    print("\n======== Testing views_emergency.py ========")
    # Creating user
    print("Creating user...", end=" ")
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
    assert response.status_code == 200, "Not pass!"
    user = User.objects.get(id=response.data['data']['id'])
    
    # Creating a doctor user
    username = str(random.random())
    last4digits = str(random.randint(1000,9999))
    email = str(random.randint(100000, 9999999)) + "@ualberta.ca"
    password = "Apple"
    request_payload = {   
            "username": username,
            "email": email,
            'height': 175,
            'weight': 63,
            'user_type': 1,
            'phone':'780-995-'+last4digits,
            'date_of_birth': datetime.date(2010, 1, 1),
            'gender':1,
            'notes':'123123',
            'password':password
        }
    response = client.post('/api/register/', request_payload)
    assert response.status_code == 200, "Not pass!"
    doctor = User.objects.get(id=response.data['data']['id'])
    print("Pass!")

    # login user
    print("Logging in user...", end=" ")
    response = client.post('/api/login/', {'username': user.username, 'password':password})
    assert response.status_code == 200, "Not pass!"
    print("Pass!")

    print('--- Valid requests ---' )
    
    # Testing empty GET
    print('Testing empty GET.', end=" ")
    response = client.get('/api/emergency/%s/'%str(user.id))
    assert response.status_code == 404, "Incorrect status code, expecting 404, get %d"%(response.status_code)
    print("Pass!")

    # Testing post
    print('Testing adding emergency events.', end=" ")
    response = client.post('/api/emergency/%s/'%str(user.id), {})
    assert response.status_code == 200, "Incorrect status code, expecting 200, get %d"%(response.status_code)
    print("Pass!")

    # Testing GET
    print('Testing getting emergency events.', end=" ")
    response = client.get('/api/emergency/%s/'%str(user.id))
    assert response.status_code == 200, "Incorrect status code, expecting 200, get %d"%(response.status_code)
    assert len(response.data['data']) == 1, "Incorrect response length, expecting 1, get %d."%len(response.body['data'])
    print("Pass!")

if(test_config):
    client = APIClient()
    
    print('\n======= api/latestconfig/ ========' )
    print('--- Valid requests ---' )
    print("Testing getting the latest version of config.", end=" ")
    response = client.get('/api/latestconfig/')
    assert response.status_code == 200, "Incorrect status code, expecting 200, get %d"%(response.status_code)
    assert len(response.data['config']) == 9, "Incorrect response length, expecting 9, get %d."%len(response.body['data'])
    print("Pass!")
print("\n========== End of the Test ===========\n")