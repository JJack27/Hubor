from django.test import TestCase
from rest_framework.test import APIRequestFactory, APIClient
import random
import uuid
import datetime
from accounts.models import *

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
            'date_of_birth': datetime.date(2010, 1, 1),
            'gender':0,
            'notes':'123123',
            'password':password
        }
    response = client.post('/api/register/', request_payload)
    user = User.objects.get(id=response.data['data']['id'])
    return user
 
def run():
    client = APIClient()
    password = "Apple"

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
            'first_name': 'Yizhou',
            'last_name':'Zhao',
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
    
    # Create 4 users
    user1 = create_user(client, 0)
    user2 = create_user(client, 0)
    doctor1 = create_user(client, 1)
    doctor2 = create_user(client, 1)

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





    print("\n======= api/takecareof/<uuid:doctor>/<uuid:patient>/ ========")
    print('--- Valid requests ---' )
    # login first
    response = client.post('/api/login/', {'username': user1.username, 'password':password})
    
    # check the post method
    print("Testing patient POST.", end=" ")
    response = client.post('/api/takecareof/%s/%s/'%(str(doctor1.id), str(user1.id)), {})
    assert response.status_code == 200, "Error! Expected 200, get %d" % response.status_code
    assert response.data['doctor']['id'] == str(doctor1.id), "Error on doctor's `id`, expected %s, get %s" \
        %(str(doctor1.id), str(response.data['doctor']['id']))
    assert response.data['doctor']['user_type'] == doctor1.user_type, "Error on doctor's `user_type`, expected %s, get %s" \
        %(str(doctor1.user_type), str(response.data['doctor']['user_type']))
    
    assert response.data['patient']['id'] == str(user1.id), "Error on doctor's `id`, expected %s, get %s" \
        %(str(user1.id), str(response.data['patient']['id']))
    assert response.data['patient']['user_type'] == user1.user_type, "Error on doctor's `user_type`, expected %s, get %s" \
        %(str(user1.user_type), str(response.data['patient']['user_type']))
    print("Pass!")
    
    # Doctor POST
    print("Testing doctor POST.", end=" ")
    # login as a doctor
    client.post('/api/logout/', {})
    client.post('/api/login/', {'username': doctor2.username, 'password':password})

    # check the post method
    response = client.post('/api/takecareof/%s/%s/'%(str(doctor1.id), str(user1.id)), {})
    assert response.status_code == 200, "Error! Expected 200, get %d" % response.status_code
    assert response.data['doctor']['id'] == str(doctor1.id), "Error on doctor's `id`, expected %s, get %s" \
        %(str(doctor1.id), str(response.data['doctor']['id']))
    assert response.data['doctor']['user_type'] == doctor1.user_type, "Error on doctor's `user_type`, expected %s, get %s" \
        %(str(doctor1.user_type), str(response.data['doctor']['user_type']))
    
    assert response.data['patient']['id'] == str(user1.id), "Error on doctor's `id`, expected %s, get %s" \
        %(str(user1.id), str(response.data['patient']['id']))
    assert response.data['patient']['user_type'] == user1.user_type, "Error on doctor's `user_type`, expected %s, get %s" \
        %(str(user1.user_type), str(response.data['patient']['user_type']))
    print("Pass!")
    
    print('--- Invalid requests ---')
    print("Un-permitted patient POST.", end=" ")
    client.post('/api/logout/', {})
    client.post('/api/login/', {'username': user1.username, 'password':password})
    response = client.post('/api/takecareof/%s/%s/'%(str(doctor1.id), str(user2.id)), {})
    assert response.status_code == 403, "Error! Expected 403, get %d" % response.status_code
    assert response.data == {}, "Non-empty data response!"
    print("Pass!")
    
    print("Non-existed doctor POST by existing patient.", end=" ")
    response = client.post('/api/takecareof/%s/%s/'%(str(uuid.uuid4()), str(user1.id)), {})
    assert response.status_code == 404, "Error! Expected 404, get %d" % response.status_code
    assert response.data == {}, "Non-empty data response!"
    print("Pass!")

    print("Non-existed patient POST by existing patient.", end=" ")
    response = client.post('/api/takecareof/%s/%s/'%(str(doctor1.id), str(uuid.uuid4())), {})
    assert response.status_code == 403, "Error! Expected 403, get %d" % response.status_code
    assert response.data == {}, "Non-empty data response!"
    print("Pass!")

    print("Non-existed doctor POST by existing doctor.", end=" ")
    client.post('/api/logout/', {})
    client.post('/api/login/', {'username': doctor1.username, 'password':password})
    response = client.post('/api/takecareof/%s/%s/'%(str(uuid.uuid4()), str(user1.id)), {})
    assert response.status_code == 404, "Error! Expected 404, get %d" % response.status_code
    assert response.data == {}, "Non-empty data response!"
    print("Pass!")

    print("Non-existed patient POST by existing doctor.", end=" ")
    response = client.post('/api/takecareof/%s/%s/'%(str(doctor1.id), str(uuid.uuid4())), {})
    assert response.status_code == 404, "Error! Expected 404, get %d" % response.status_code
    assert response.data == {}, "Non-empty data response!"
    print("Pass!")



    print('')