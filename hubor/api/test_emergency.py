from django.test import TestCase
from rest_framework.test import APIRequestFactory, APIClient
import random
import uuid
import datetime
from accounts.models import *
from data.models import *

def run():
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
    request_payload = {
        "longitude": 129.3,
        "latitude": -80,
        "configuration": 1,
    }
    print('Testing adding emergency events.', end=" ")
    response = client.post('/api/emergency/%s/'%str(user.id), request_payload)
    assert response.status_code == 200, "Incorrect status code, expecting 200, get %d"%(response.status_code)
    print("Pass!")

    # Testing GET
    print('Testing getting emergency events.', end=" ")
    response = client.get('/api/emergency/%s/'%str(user.id))
    assert response.status_code == 200, "Incorrect status code, expecting 200, get %d"%(response.status_code)
    assert len(response.data['data']) == 1, "Incorrect response length, expecting 1, get %d."%len(response.body['data'])
    assert float(response.data['data'][0]["longitude"]) == float(request_payload['longitude']), "Incorrect longitude, expect %s, get %s" %(str(request_payload['longitude']), response.data['data'][0]["longitude"])
    assert float(response.data['data'][0]["latitude"]) == float(request_payload['latitude']), "Incorrect latitude, expect %s, get %s" %(str(request_payload['latitude']), response.data['data'][0]["latitude"])
    assert float(response.data['data'][0]["configuration"]) == float(request_payload['configuration']), "Incorrect latitude, expect %s, get %s" %(str(request_payload['configuration']), response.data['data'][0]["configuration"])
    print("Pass!")