from django.test import TestCase
from rest_framework.test import APIRequestFactory, APIClient
import random
import uuid
import datetime
from accounts.models import *
from data.models import *
from .test_util import *

def run():
    client = APIClient()
    password = "Apple"
    print("\n======== Testing views_emergency.py ========")
    # Creating user
    user = create_user(client, 0)
    
    # Creating a doctor user
    doctor = create_user(client, 1)

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
        "risk": 2
    }
    print('Testing adding emergency events.', end=" ")
    response = client.post('/api/emergency/%s/'%str(user.id), request_payload)
    assert response.status_code == 200, "Incorrect status code, expecting 200, get %d"%(response.status_code)
    
    # assign user to doctor
    login(client, doctor)
    facility = create_facility(client, "Alibaba")
    request_payload = {"user": str(doctor.id)}
    response = client.put('/api/belongsto/%s/'%(str(facility.id)), request_payload)
    assert response.status_code == 200, "User is not assigned to the facility!"

    request_payload['user'] = str(user.id)
    response = client.put('/api/belongsto/%s/'%(str(facility.id)), request_payload)
    assert response.status_code == 200, "Doctor is not assigned to the facility!"

    response = client.post('/api/takecareof/%s/%s/'%(str(doctor.id), str(user.id)), {})
    assert response.status_code == 200, "User is not assigned to the doctor!"


    # Testing user's status is up-to-date
    response = client.get('/api/patientsof/%s/'%str(doctor.id))
    assert response.status_code == 200, "Incorrect status code, expecting 200, get %d"%(response.status_code)
    assert len(response.data) == 1, "Incorrect length, expecting 1, get %d" % (len(response.data))
    assert response.data[0]['id'] == str(user.id), "ID: doesn't match"
    print(response.data[0]['status'])
    assert response.data[0]['status'][0] == 2, "status: doesn't match"
    print("Pass!")

    # Testing GET
    request_payload = {
        "longitude": 129.3,
        "latitude": -80,
        "configuration": 1,
        "risk": 2
    }
    print('Testing getting emergency events.', end=" ")
    response = client.get('/api/emergency/%s/'%str(user.id))
    assert response.status_code == 200, "Incorrect status code, expecting 200, get %d"%(response.status_code)
    assert len(response.data) == 1, "Incorrect response length, expecting 1, get %d."%len(response.body['data'])
    assert float(response.data[0]["longitude"]) == float(request_payload['longitude']), "Incorrect longitude, expect %s, get %s" %(str(request_payload['longitude']), response.data['data'][0]["longitude"])
    assert float(response.data[0]["latitude"]) == float(request_payload['latitude']), "Incorrect latitude, expect %s, get %s" %(str(request_payload['latitude']), response.data['data'][0]["latitude"])
    assert float(response.data[0]["configuration"]) == float(request_payload['configuration']), "Incorrect latitude, expect %s, get %s" %(str(request_payload['configuration']), response.data['data'][0]["configuration"])
    print("Pass!")