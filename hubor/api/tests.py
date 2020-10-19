from django.test import TestCase
from rest_framework.test import APIRequestFactory, APIClient
import random
import uuid
import datetime
from accounts.models import *
from data.models import *

# Create your tests here.
test_user = False
test_data = False
test_emergency = True

# Testing views_user.py
if(test_user):
    client = APIClient()
    
    print('\n======= api/register/ ========' )
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
        assert str(request_payload[key]) == str(item), "%s: request=%s resposne=%s"%(key, str(request_payload[key]), str(item))
    
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
    assert response.status_code == 401
    print("OK")
    
    print("* user_type * ")
    request_payload['user_type'] = 4
    response = client.post('/api/register/', request_payload)
    print("Status = ", response.status_code)
    request_payload['user_type'] = 1
    assert response.status_code == 401 
    print("OK")

    print('* gender *')
    request_payload['gender'] = 4
    response = client.post('/api/register/', request_payload)
    print("Status = ", response.status_code)
    request_payload['gender'] = 1
    assert response.status_code == 401
    print("OK")

    print('* notes *')
    request_payload['notes'] = "".join(['x' for _ in range(801)])
    response = client.post('/api/register/', request_payload)
    print("Status = ", response.status_code)
    request_payload['notes'] = '123'
    assert response.status_code == 401
    print("OK")
    print("\n======= api/login/ ========")
    print('--- Valid requests ---' )
    user = User.objects.get(id=user_id)
    response = client.post('/api/login/', {'username': user.username, 'password':password})
    print(response.status_code, response.data)
    print('--- Invalid requests ---' )
    user = User.objects.get(id=user_id)
    response = client.post('/api/login/', {'username': user.username, 'password':"password"})
    print(response.status_code, response.data)

    print("\n======= api/logout/ ========")
    print('--- Valid requests ---' )
    response = client.post('/api/logout/', {})
    print(response.status_code, response.data)


    print('\n======= api/bracelet/%s/ ========'%(str(user.id)) )
    print('--- Valid requests ---' )
    # login first
    response = client.post('/api/login/', {'username': user.username, 'password':password})
    
    # check get method
    print("Check if current user having any bracelets, should be empty.", end=" ")
    response = client.get('/api/bracelet/'+str(user.id)+'/')
    assert response.status_code == 404, "\n!Current user should not have any bracelets."
    print("Pass!")
    
    # check post method
    print('Adding 2 new bracelets to current user.', end=" ")
    request_payload = {'mac_addr':'01:23:45:67:89:AB'}
    bracelets = {}
    response = client.post('/api/bracelet/'+str(user.id)+'/', request_payload)
    bracelets[response.data['bracelet']['id']] = response.data['bracelet']
    assert str(user.id) == str(response.data['bracelet']['owner']), "Owner ID is not the same."
    assert request_payload['mac_addr'] == response.data['bracelet']['mac_addr'], "Mac address is not the same"
    
    request_payload = {'mac_addr':'01:23:45:67:89:ff'}
    response = client.post('/api/bracelet/'+str(user.id)+'/', request_payload)
    bracelets[response.data['bracelet']['id']] = response.data['bracelet']
    assert str(user.id) == str(response.data['bracelet']['owner']), "Owner ID is not the same."
    assert request_payload['mac_addr'] == response.data['bracelet']['mac_addr'], "Mac address is not the same"
    print("Pass!")
    
    # Test get method
    print("Check if bracelets were successfully added", end=" ")
    response = client.get('/api/bracelet/'+str(user.id)+'/')
    assert response.status_code == 200, "Incorrect status code, expecting 200, received " + str(response.status_code)
    recv_braclets = response.data['bracelets']
    for b in recv_braclets:
        b_id = b['id']
        for key in b.keys():
            assert b[key] == bracelets[b_id][key], "Doesn't match! Expecting: %s, get: %s"%(str(bracelets[b_id][key]), str(b[key]))
    print("Pass!")

    # Testing invalid requests
    print('--- Invalid requests ---' )
    
    # Testing non-exist user GET
    print("Non-existed user GET.", end=" ")
    response = client.get('/api/bracelet/'+str(uuid.uuid4())+'/')
    assert response.status_code == 404, "\nIncorrect status code: %s" %(str(response.status_code))
    assert response.data['bracelets'] == [], "\nNon-empty response: %s" %(str(response.data['bracelets'])) 
    print("Pass!")

    # Testing non-exist user POST
    print("Non-existed user POST.", end=" ")
    response = client.post('/api/bracelet/'+str(uuid.uuid4())+'/', request_payload)
    assert response.status_code == 404, "\nIncorrect status code: %s" %(str(response.status_code))
    assert response.data['bracelet'] == {}, "\nNon-empty response: %s" %(str(response.data['bracelet'])) 
    print("Pass!")

    # Testing invalid request payload
    print("Invalid POST payload.")
    request_payload = {'mac_addr':'01:23:45:67:89:GF'}
    print("\tmac_addr = %s."%(request_payload['mac_addr']), end=" ")
    response = client.post('/api/bracelet/'+str(user.id)+'/', request_payload)
    assert response.status_code == 401, "\nIncorrect status code: %s" %(str(response.status_code))
    assert response.data['bracelet'] == {}, "\nNon-empty response: %s" %(str(response.data['bracelet'])) 
    print("Pass!")

    request_payload = {'mac_addr':'23:45:67:89:GF'}
    print("\tmac_addr = %s."%(request_payload['mac_addr']), end=" ")
    response = client.post('/api/bracelet/'+str(user.id)+'/', request_payload)
    assert response.status_code == 401, "\nIncorrect status code: %s" %(str(response.status_code))
    assert response.data['bracelet'] == {}, "\nNon-empty response: %s" %(str(response.data['bracelet'])) 
    print("Pass!")

    print("Invalid POST payload + non-existed user.")
    request_payload = {'mac_addr':'23:45:67:89:GF'}
    print("\tmac_addr = %s."%(request_payload['mac_addr']), end=" ")
    response = client.post('/api/bracelet/'+str(uuid.uuid4())+'/', request_payload)
    assert response.status_code == 404, "\nIncorrect status code: %s" %(str(response.status_code))
    assert response.data['bracelet'] == {}, "\nNon-empty response: %s" %(str(response.data['bracelet'])) 
    print("Pass!")



# Testing views_data.py
if(test_data):
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
    response = client.post('/api/emergency/%s/'%str(user.id), {})
    assert response.status_code == 200, "Incorrect status code, expecting 200, get %d"%(response.status_code)
    assert len(response.body['data']) == 1, "Incorrect response length, expecting 1, get %d."%len(response.body['data'])
    print("Pass!")
    
    print('--- Valid requests ---' )
print("\n========== End of the Test ===========\n")