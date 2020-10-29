from django.test import TestCase
from rest_framework.test import APIRequestFactory, APIClient
import random
import uuid
import datetime
from accounts.models import *
from data.models import *

def run():
    client = APIClient()
    print("\n======== Testing views_data.py ========")
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

    # add user a bracelet
    print("Adding user a bracelet...", end=" ")
    request_payload = {'mac_addr':'01:23:45:67:89:AB'}
    response = client.post('/api/bracelet/'+str(user.id)+'/', request_payload)
    bracelet_id = response.data['bracelet']['id']
    assert response.status_code == 200, "Not pass!"
    print("Pass!")

    # Starting testing APIs
    # Testing api/data/<uuid:pk>/
    print('\n======= api/data/%s/ ========'%(str(user.id)))
    # Creating random payload
    request_payloads = []
    num_entries = 10
    for i in range(num_entries):
        request_payloads.append({
            'bracelet': bracelet_id,
            'tem': random.random(),
            'acx': random.random(),
            'acz': random.random(),
            'bat': random.random(),
            'red': random.random(),
            'ir': random.random(),
        })
    
    print('--- Valid requests ---' )
    # Testing GET none data
    print("Testing GET empty data.", end=" ")
    response = client.get('/api/data/%s/'%(str(user.id)))
    assert response.status_code == 404, "Incorrect status_code, expecting 404, get %d"%(response.status_code)
    assert response.data['data'] == [], "Non-empty return: %s"%(str(response.data['data']))
    print("Pass!")

    # Testing POST data
    print("Testing POST data.", end=" ")
    for i in range(num_entries):
        response = client.post('/api/data/%s/'%(str(user.id)), request_payloads[i])
        assert response.status_code == 200, "Incorrect status_code, expecting 404, get %d"%(response.status_code)
        assert response.data == {}, "Non-empty return: %s"%(str(response.data))
    print('Pass!')

    # Testing GET added data
    print("Testing GET added data.", end=' ')
    response = client.get('/api/data/%s/'%(str(user.id)))
    assert response.status_code == 200, "Incorrect status_code, expecting 404, get %d"%(response.status_code)
    assert len(response.data['data']) == num_entries, "Incorrect num_entries, expecting %d, get %d"%(num_entries, len(response.data['data']))
    for i in range(num_entries):
        result = response.data['data'][i] 
        for key, value in result.items():
            if(key == 'id' or key == 'time'):
                continue
            if(key == 'owner'):
                assert str(result[key]) == str(user.id), "Owner Id isn't match"
                continue
            assert str(result[key]) == str(request_payloads[i][key]), "Doesn't match on %s, expecting %s, get %s"%(key, str(result[key]), str(request_payloads[i][key]))
    print("Pass!")

    # Testing GET added data
    print("Testing GET added data.", end=' ')
    response = client.get('/api/data/%s/'%(str(user.id)))
    assert response.status_code == 200, "Incorrect status_code, expecting 404, get %d"%(response.status_code)
    assert len(response.data['data']) == num_entries, "Incorrect num_entries, expecting %d, get %d"%(num_entries, len(response.data['data']))
    for i in range(num_entries):
        result = response.data['data'][i] 
        for key, value in result.items():
            if(key == 'id' or key == 'time'):
                continue
            if(key == 'owner'):
                assert str(result[key]) == str(user.id), "Owner Id isn't match"
                continue
            assert str(result[key]) == str(request_payloads[i][key]), "Doesn't match on %s, expecting %s, get %s"%(key, str(result[key]), str(request_payloads[i][key]))
    print("Pass!")

    # Test doctor GET
    client.post('/api/logout/', {})
    client.post('/api/login/', {'username': doctor.username, 'password':password})
    print("Testing doctor GET added data.", end=' ')
    response = client.get('/api/data/%s/'%(str(user.id)))
    assert response.status_code == 200, "Incorrect status_code, expecting 404, get %d"%(response.status_code)
    assert len(response.data['data']) == num_entries, "Incorrect num_entries, expecting %d, get %d"%(num_entries, len(response.data['data']))
    for i in range(num_entries):
        result = response.data['data'][i] 
        for key, value in result.items():
            if(key == 'id' or key == 'time'):
                continue
            if(key == 'owner'):
                assert str(result[key]) == str(user.id), "Owner Id isn't match"
                continue
            assert str(result[key]) == str(request_payloads[i][key]), "Doesn't match on %s, expecting %s, get %s"%(key, str(result[key]), str(request_payloads[i][key]))
    

    # Testing api/data/<uuid:pk>/
    print('\n======= api/vs/%s/ ========'%(str(user.id)))
    # Creating random payload
    request_payloads = []
    num_entries = 10
    for i in range(num_entries):
        request_payloads.append({
            'bracelet': bracelet_id,
            'temp': random.random(),
            'spo2': random.random(),
            'hr': random.random(),
            'rr': random.random()
        })
    
    # Testing GET none vital sign
    print("Testing GET empty vital sign.", end=" ")
    response = client.get('/api/vs/%s/'%(str(user.id)))
    assert response.status_code == 404, "Incorrect status_code, expecting 404, get %d"%(response.status_code)
    assert response.data['data'] == [], "Non-empty return: %s"%(str(response.data['data']))
    print("Pass!")

    # Testing POST data
    print("Testing POST data.", end=" ")
    for i in range(num_entries):
        response = client.post('/api/data/%s/'%(str(user.id)), request_payloads[i])
        assert response.status_code == 200, "Incorrect status_code, expecting 404, get %d"%(response.status_code)
        assert response.data == {}, "Non-empty return: %s"%(str(response.data))
    print('Pass!')

    # Testing GET added data
    print("Testing GET added data.", end=' ')
    response = client.get('/api/data/%s/'%(str(user.id)))
    assert response.status_code == 200, "Incorrect status_code, expecting 404, get %d"%(response.status_code)
    assert len(response.data['data']) == num_entries, "Incorrect num_entries, expecting %d, get %d"%(num_entries, len(response.data['data']))
    for i in range(num_entries):
        result = response.data['data'][i] 
        for key, value in result.items():
            if(key == 'id' or key == 'time'):
                continue
            if(key == 'owner'):
                assert str(result[key]) == str(user.id), "Owner Id isn't match"
                continue
            assert str(result[key]) == str(request_payloads[i][key]), "Doesn't match on %s, expecting %s, get %s"%(key, str(result[key]), str(request_payloads[i][key]))
    print("Pass!")

    # Testing GET added data
    print("Testing GET added data.", end=' ')
    response = client.get('/api/data/%s/'%(str(user.id)))
    assert response.status_code == 200, "Incorrect status_code, expecting 404, get %d"%(response.status_code)
    assert len(response.data['data']) == num_entries, "Incorrect num_entries, expecting %d, get %d"%(num_entries, len(response.data['data']))
    for i in range(num_entries):
        result = response.data['data'][i] 
        for key, value in result.items():
            if(key == 'id' or key == 'time'):
                continue
            if(key == 'owner'):
                assert str(result[key]) == str(user.id), "Owner Id isn't match"
                continue
            assert str(result[key]) == str(request_payloads[i][key]), "Doesn't match on %s, expecting %s, get %s"%(key, str(result[key]), str(request_payloads[i][key]))
    print("Pass!")

    # Test doctor GET
    client.post('/api/logout/', {})
    client.post('/api/login/', {'username': doctor.username, 'password':password})
    print("Testing doctor GET added data.", end=' ')
    response = client.get('/api/data/%s/'%(str(user.id)))
    assert response.status_code == 200, "Incorrect status_code, expecting 404, get %d"%(response.status_code)
    assert len(response.data['data']) == num_entries, "Incorrect num_entries, expecting %d, get %d"%(num_entries, len(response.data['data']))
    for i in range(num_entries):
        result = response.data['data'][i] 
        for key, value in result.items():
            if(key == 'id' or key == 'time'):
                continue
            if(key == 'owner'):
                assert str(result[key]) == str(user.id), "Owner Id isn't match"
                continue
            assert str(result[key]) == str(request_payloads[i][key]), "Doesn't match on %s, expecting %s, get %s"%(key, str(result[key]), str(request_payloads[i][key]))
    
    
    
    
    client.post('/api/logout/', {})
    print("Pass!")

    print('--- Invalid requests ---' )
    # Testing Unauthorized GET
    # Creating an unautorized user
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
    unauthorized_user = User.objects.get(id=response.data['data']['id'])
    client.post('/api/login/', {'username':unauthorized_user.username, 'password':password})
    # testing the get method
    print("Testing unauthorized GET.", end=" ")
    response = client.get('/api/data/%s/'%(str(user.id)))
    assert response.status_code == 403, "Incorrect status_code, expecting 403, get %d"%(response.status_code)
    assert response.data['data'] == [], "Non-empty response: %s"%response.data['data']
    print("Pass!")

    # Testing non-exist user POST
    print("Testing non-exist user POST.", end=" ")
    response = client.post('/api/data/%s/'%(str(uuid.uuid4())), request_payloads[0])
    assert response.status_code == 403, "Incorrect status_code, expecting 403, get %d"%(response.status_code)
    assert response.data == {}, "Non-empty response: %s"%response.data
    print("Pass!")

    # Testing non-exist bracelet POST
    print("Testing non-exist bracelet POST.", end=" ")
    request_payload = {
            'bracelet': uuid.uuid4(),
            'tem': random.random(),
            'acx': random.random(),
            'acz': random.random(),
            'bat': random.random(),
            'red': random.random(),
            'ir': random.random(),
        }
    response = client.post('/api/data/%s/'%(str(unauthorized_user.username)), request_payload)
    assert response.status_code == 404, "Incorrect status_code, expecting 403, get %d"%(response.status_code)
    print("Pass!")