from django.test import TestCase
from rest_framework.test import APIRequestFactory, APIClient
import random
import uuid
import datetime
from accounts.models import *
from .test_util import *
 
def run():
    client = APIClient()
    password = "Apple"
    # Create 4 users
    user1 = create_user(client, 0)
    user2 = create_user(client, 0)
    doctor1 = create_user(client, 1)
    doctor2 = create_user(client, 1)
    print("======= User created =======")
    print("user1 = %s" %str(user1.id))
    print("user2 = %s" %str(user2.id))
    print("doctor1 = %s" %str(doctor1.id))
    print("doctor2 = %s" %str(doctor2.id))
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
    assert response.status_code == 400
    print("OK")
    
    print("* user_type * ")
    request_payload['user_type'] = 4
    response = client.post('/api/register/', request_payload)
    print("Status = ", response.status_code)
    request_payload['user_type'] = 1
    assert response.status_code == 400 
    print("OK")

    print('* gender *')
    request_payload['gender'] = 4
    response = client.post('/api/register/', request_payload)
    print("Status = ", response.status_code)
    request_payload['gender'] = 1
    assert response.status_code == 400
    print("OK")

    print('* notes *')
    request_payload['notes'] = "".join(['x' for _ in range(801)])
    response = client.post('/api/register/', request_payload)
    print("Status = ", response.status_code)
    request_payload['notes'] = '123'
    assert response.status_code == 400
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





    print('\n======= api/bracelet/%s/ ========'%(str(user1.id)) )
    print('--- Valid requests ---' )
    # login first
    response = client.post('/api/login/', {'username': user1.username, 'password':password})
    
    # check get method
    print("Check if current user having any bracelets, should be empty.", end=" ")
    response = client.get('/api/bracelet/'+str(user1.id)+'/')
    assert response.status_code == 404, "\n!Current user should not have any bracelets."
    print("Pass!")
    
    # check post method
    print('Adding 2 new bracelets to current user.', end=" ")
    request_payload = {'mac_addr':'01:23:45:67:89:AB'}
    bracelets = {}
    response = client.post('/api/bracelet/'+str(user1.id)+'/', request_payload)
    assert response.status_code == 200, "Incorrect status code %d"%response.status_code
    bracelets[response.data['bracelet']['id']] = response.data['bracelet']
    assert str(user1.id) == str(response.data['bracelet']['owner']), "Owner ID is not the same."
    assert request_payload['mac_addr'] == response.data['bracelet']['mac_addr'], "Mac address is not the same"
    
    request_payload = {'mac_addr':'01:23:45:67:89:ff'}
    response = client.post('/api/bracelet/'+str(user1.id)+'/', request_payload)
    bracelets[response.data['bracelet']['id']] = response.data['bracelet']
    assert str(user1.id) == str(response.data['bracelet']['owner']), "Owner ID is not the same."
    assert request_payload['mac_addr'] == response.data['bracelet']['mac_addr'], "Mac address is not the same"
    print("Pass!")
    
    # Test get method
    print("Check if bracelets were successfully added", end=" ")
    response = client.get('/api/bracelet/'+str(user1.id)+'/')
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
    response = client.post('/api/bracelet/'+str(user1.id)+'/', request_payload)
    assert response.status_code == 400, "\nIncorrect status code: %s" %(str(response.status_code))
    assert response.data['bracelet'] == {}, "\nNon-empty response: %s" %(str(response.data['bracelet'])) 
    print("Pass!")

    request_payload = {'mac_addr':'23:45:67:89:GF'}
    print("\tmac_addr = %s."%(request_payload['mac_addr']), end=" ")
    response = client.post('/api/bracelet/'+str(user1.id)+'/', request_payload)
    assert response.status_code == 400, "\nIncorrect status code: %s" %(str(response.status_code))
    assert response.data['bracelet'] == {}, "\nNon-empty response: %s" %(str(response.data['bracelet'])) 
    print("Pass!")

    print("Invalid POST payload + non-existed user.")
    request_payload = {'mac_addr':'23:45:67:89:GF'}
    print("\tmac_addr = %s."%(request_payload['mac_addr']), end=" ")
    response = client.post('/api/bracelet/'+str(uuid.uuid4())+'/', request_payload)
    assert response.status_code == 404, "\nIncorrect status code: %s" %(str(response.status_code))
    assert response.data['bracelet'] == {}, "\nNon-empty response: %s" %(str(response.data['bracelet'])) 
    print("Pass!")




    print("\n======= api/facilities/ ========")
    print('--- Valid requests ---')
    # login as doctor
    response = login(client, doctor1)
    print("Testing doctor POST.", end=" ")
    request_payload = {
        'name': "facility",
        'address': "123123123",
        'phone': "123123123"
    }
    response = client.post('/api/facilities/', request_payload)
    assert response.status_code == 200, "Incorrect status code: %s" %(str(response.status_code))
    facility1 = Facilities.objects.get(id = response.data['id'])
    assert response.data['name'] == facility1.name, "Incorrect name! Expected %s, get %s" %(facility1.name, response.data['name'])
    assert response.data['address'] == facility1.address, "Incorrect address! Expected %s, get %s" %(facility1.address, response.data['address'])
    assert response.data['phone'] == facility1.phone, "Incorrect phone! Expected %s, get %s" %(facility1.phone, response.data['phone'])
    
    response = client.post('/api/facilities/', request_payload)
    facility2 = Facilities.objects.get(id = response.data['id'])
    print("Pass!")

    print("Testing doctor GET.", end=" ")
    response = client.get('/api/facilities/')
    assert response.status_code == 200, "Incorrect status code: %s" %(str(response.status_code))
    print("Pass!")

    print("Testing patient GET.", end=" ")
    logout(client)
    login(client, user1)
    response = client.get('/api/facilities/')
    assert response.status_code == 200, "Incorrect status code: %s" %(str(response.status_code))
    print("Pass!")

    print('--- Invalid requests ---')
    print("Testing patient POST.", end=" ")
    response = client.post('/api/facilities/', request_payload)
    assert response.status_code == 403, "Incorrect status code: %s" %(str(response.status_code))
    print("Pass!")

    print("\n======= api/belongsto/<uuid:facility>/ ========")
    print('--- Valid requests ---')
    
    # doctor1 -> facility1
    logout(client)
    login(client, doctor1)
    print("Testing doctor PUT.", end=" ")
    response = client.put('/api/belongsto/%s/'%str(facility1.id), {'user':str(doctor1.id)})
    assert response.status_code == 200, "Incorrect status code: %s" %(str(response.status_code))
    assert str(response.data['user']['id']) == str(doctor1.id), "User is not match. Expecting (%s), get (%s)" \
        %(str(doctor1.id), str(response.data['user']['id']))
    assert str(response.data['facility']['id']) == str(facility1.id), "Facility is not match. Expecting (%s), get (%s)" \
        %(str(facility1.id), str(response.data['facility']['id']))
    print("Pass!")
    
    print("Testing doctor GET.", end=" ")
    response = client.get('/api/belongsto/%s/'%str(facility1.id))
    assert response.status_code == 200, "Incorrect status code: %s" %(str(response.status_code))
    print("Pass!")
    
    # user1 -> facility1
    logout(client)
    login(client, user1)
    print("Testing patient PUT.", end=" ")
    response = client.put('/api/belongsto/%s/'%str(facility1.id), {'user':str(user1.id)})
    assert response.status_code == 200, "Incorrect status code: %s" %(str(response.status_code))
    assert str(response.data['user']['id']) == str(user1.id), "User is not match. Expecting (%s), get (%s)" \
        %(str(user1.id), str(response.data['user']['id']))
    assert str(response.data['facility']['id']) == str(facility1.id), "Facility is not match. Expecting (%s), get (%s)" \
        %(str(facility1.id), str(response.data['facility']['id']))
    print("Pass!")

    print("Testing patient GET.", end=" ")
    response = client.get('/api/belongsto/%s/'%str(facility1.id))
    assert response.status_code == 200, "Incorrect status code: %s" %(str(response.status_code))
    len_of_response = len(response.data)
    print("Pass!")

    print("Testing duplicate patient PUT.", end=" ")
    response = client.put('/api/belongsto/%s/'%str(facility1.id), {'user':str(user1.id)})
    assert response.status_code == 200, "Incorrect status code: %s" %(str(response.status_code))
    response = client.get('/api/belongsto/%s/'%str(facility1.id))
    assert response.status_code == 200, "Incorrect status code: %s" %(str(response.status_code))
    assert len(response.data) == len_of_response, "len after put (%d) != len before put (%d)" \
        %(len(response.data), len_of_response)
    print("Pass!")

    # user2 -> facility1
    logout(client)
    login(client, doctor1)
    print("Testing doctor-patient PUT.", end=" ")
    response = client.put('/api/belongsto/%s/'%str(facility1.id), {'user':str(user2.id)})
    assert response.status_code == 200, "Incorrect status code: %s" %(str(response.status_code))
    print("Pass!")


    print('--- Invalid requests ---')
    logout(client)
    login(client, doctor2)
    print("Tesing no-facility doctor GET.", end=" ")
    response = client.get('/api/belongsto/%s/'%str(facility1.id))
    assert response.status_code == 403, "Incorrect status code: %s" %(str(response.status_code))
    print("Pass!")

    print("Tesing diff-facility doctor GET.", end=" ")
    # doctor2 -> facility2
    response = client.put('/api/belongsto/%s/'%str(facility2.id), {'user':str(doctor2.id)})
    assert response.status_code == 200, "Incorrect status code: %s" %(str(response.status_code))
    response = client.get('/api/belongsto/%s/'%str(facility1.id)) 
    assert response.status_code == 403, "Incorrect status code: %s" %(str(response.status_code))
    print("Pass!")
    
    #===========================================================================
    '''
    doctor1 -> fa-1
    doctor2 -> fa-2
    user1 -> fa-1
    user2 -> fa-1
    '''
    print("\n======= api/takecareof/<uuid:doctor>/<uuid:patient>/ ========")
    print('--- Valid requests ---' )
    # login first
    logout(client)
    login(client, user1)
    # check the post method
    # doctor1 <-> user1
    print("Testing patient POST (same facility).", end=" ")
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
    logout(client)
    login(client, doctor1)

    # check the post method
    # doctor1 <-> user2
    response = client.post('/api/takecareof/%s/%s/'%(str(doctor1.id), str(user2.id)), {})
    assert response.status_code == 200, "Error! Expected 200, get %d" % response.status_code
    assert response.data['doctor']['id'] == str(doctor1.id), "Error on doctor's `id`, expected %s, get %s" \
        %(str(doctor1.id), str(response.data['doctor']['id']))
    assert response.data['doctor']['user_type'] == doctor1.user_type, "Error on doctor's `user_type`, expected %s, get %s" \
        %(str(doctor1.user_type), str(response.data['doctor']['user_type']))
    assert response.data['patient']['id'] == str(user2.id), "Error on doctor's `id`, expected %s, get %s" \
        %(str(user2.id), str(response.data['patient']['id']))
    assert response.data['patient']['user_type'] == user2.user_type, "Error on doctor's `user_type`, expected %s, get %s" \
        %(str(user2.user_type), str(response.data['patient']['user_type']))
    print("Pass!")
    
    

    print('--- Invalid requests ---')
    print("Un-permitted patient POST.", end=" ")
    logout(client)
    login(client, user1)
    response = client.post('/api/takecareof/%s/%s/'%(str(doctor1.id), str(user2.id)), {})
    assert response.status_code == 403, "Error! Expected 403, get %d" % response.status_code
    assert response.data == {}, "Non-empty data response!"
    print("Pass!")
    
    print("Non-existed doctor POST by existing patient.", end=" ")
    response = client.post('/api/takecareof/%s/%s/'%(str(uuid.uuid4()), str(user1.id)), {})
    assert response.status_code == 403, "Error! Expected 404, get %d" % response.status_code
    assert response.data == {}, "Non-empty data response!"
    print("Pass!")

    print("Non-existed patient POST by existing patient.", end=" ")
    response = client.post('/api/takecareof/%s/%s/'%(str(doctor1.id), str(uuid.uuid4())), {})
    assert response.status_code == 403, "Error! Expected 403, get %d" % response.status_code
    assert response.data == {}, "Non-empty data response!"
    print("Pass!")

    print("Non-existed doctor POST by existing doctor.", end=" ")
    logout(client)
    login(client, doctor2)
    response = client.post('/api/takecareof/%s/%s/'%(str(uuid.uuid4()), str(user1.id)), {})
    assert response.status_code == 403, "Error! Expected 404, get %d" % response.status_code
    assert response.data == {}, "Non-empty data response!"
    print("Pass!")

    print("Non-existed patient POST by existing doctor.", end=" ")
    response = client.post('/api/takecareof/%s/%s/'%(str(doctor1.id), str(uuid.uuid4())), {})
    assert response.status_code == 403, "Error! Expected 404, get %d" % response.status_code
    assert response.data == {}, "Non-empty data response!"
    print("Pass!")

    print("Doctor POST by doctor from other facilities", end=" ")
    response = client.post('/api/takecareof/%s/%s/'%(str(doctor1.id), str(user1.id)), {})
    assert response.status_code == 403, "Error! Expected 403, get %d" % response.status_code
    assert response.data == {}, "Non-empty data response!"
    print("Pass!")


    
    print("\n======= api/patientsof/<uuid:doctor>/ ========")
    print('--- Valid requests ---' )
    # login as doctor1
    logout(client)
    login(client, doctor1)
    print("Testing doctor GET.", end=" ")
    response = client.get('/api/patientsof/%s/'%str(doctor1.id))
    assert response.status_code == 200, "Error! Expected 200, get %d" % response.status_code
    patients = response.data
    assert len(patients) == 2, "Error! Expect length of 2, get %d" % len(patients)
    assert str(patients[0]['id']) == str(user1.id) or str(patients[0]['id']) == str(user2.id), "Error! Invalid id: %s" %str(patients[0]['id'])
    assert str(patients[1]['id']) == str(user1.id) or str(patients[1]['id']) == str(user2.id), "Error! Invalid id: %s" %str(patients[1]['id'])
    print("Pass!")

    print('--- Invalid requests ---' )
    # login as doctor1
    response = client.post('/api/login/', {'username': doctor1.username, 'password':password})
    print("Testing doctor GET of doctor without any patients.", end=" ")
    response = client.get('/api/patientsof/%s/'%str(doctor2.id))
    assert response.status_code == 403, "Error! Expected 404, get %d" % response.status_code
    print("Pass!")

    print("Testing doctor GET of non-existed doctor.", end=" ")
    response = client.get('/api/patientsof/%s/'%str(uuid.uuid4()))
    assert response.status_code == 403, "Error! Expected 404, get %d" % response.status_code
    print("Pass!")


    # login as uesr1
    response = client.post('/api/login/', {'username': user1.username, 'password':password})
    print("Testing patient GET.", end=" ")
    response = client.get('/api/patientsof/%s/'%str(doctor2.id))
    assert response.status_code == 403, "Error! Expected 403, get %d" % response.status_code
    print("Pass!")

    print("Testing patient GET of non-existed doctor.", end=" ")
    response = client.get('/api/patientsof/%s/'%str(uuid.uuid4()))
    assert response.status_code == 403, "Error! Expected 403, get %d" % response.status_code
    print("Pass!")


    #================
    '''
    all in facility 1
    '''
    print("\n======= api/doctorof/<uuid:patient>/ ========")
    logout(client)
    login(client, doctor2)
    print("Testing patient PUT.", end=" ")
    response = client.put('/api/belongsto/%s/'%str(facility1.id), {'user':str(doctor2.id)})
    assert response.status_code == 200, "Incorrect status code: %s" %(str(response.status_code))
    print('--- Valid requests ---' )
    # Test patient GET
    # login as user 1
    response = client.post('/api/login/', {'username': user1.username, 'password':password})
    print("Testing patient GET.", end=" ")
    response = client.get('/api/doctorof/%s/'%str(user1.id))
    assert response.status_code == 200, "Error! Expected 200, get %d" % response.status_code
    doctor = response.data
    assert str(doctor['id']) == str(doctor1.id), "Incorrect doctor id (%s). Expecting (%s)" \
        %(str(doctor['id']), str(doctor1.id))
    print("Pass!")
    

    # Test patient PUT
    print("Testing patient PUT.", end=" ")
    response = client.put('/api/doctorof/%s/'%str(user1.id), {'doctor_id':str(doctor2.id)})
    assert response.status_code == 200, "Error! Expected 200, get %d" % response.status_code
    assert str(response.data['patient']['id']) == str(user1.id), "Incorrect patient id (%s). Expecting (%s)" \
        %(str(response.data['patient']['id']), str(user1.id))
    assert str(response.data['doctor']['id']) == str(doctor2.id), "Incorrect doctor id (%s). Expecting (%s)" \
        %(str(response.data['doctor']['id']), str(doctor2.id))
    print("Pass!")

    # logout
    client.post("/api/logout/", {})

    # Test doctor GET
    # login as doctor 1
    response = client.post('/api/login/', {'username': doctor1.username, 'password':password})
    print("Testing doctor GET.", end=" ")
    response = client.get('/api/doctorof/%s/'%str(user1.id))
    assert response.status_code == 200, "Error! Expected 200, get %d" % response.status_code
    doctor = response.data
    assert str(doctor['id']) == str(doctor2.id), "Incorrect doctor id (%s). Expecting (%s)" \
        %(str(doctor['id']), str(doctor2.id))
    print("Pass!")

    print('--- Invalid requests ---' )
    print("Testing unauthorized patient GET.", end=' ')
    response = client.post('/api/login/',  {'username': user2.username, 'password':password})
    response = client.get('/api/doctorof/%s/'%str(user1.id))
    assert response.status_code == 403, "Error! Expected 403, get %d" % response.status_code
    print("Pass!")

    print("Testing unauthorized patient PUT.", end=' ')
    response = client.put('/api/doctorof/%s/'%str(user1.id), {'doctor_id':doctor1.id})
    assert response.status_code == 403, "Error! Expected 403, get %d" % response.status_code
    print("Pass!")

    print("Testing patient non-exist GET.", end=' ')
    response = client.get('/api/doctorof/%s/'%str(uuid.uuid4()))
    assert response.status_code == 403, "Error! Expected 403, get %d" % response.status_code
    print("Pass!")

    print("Testing doctor non-exist GET.", end=' ')
    response = client.post('/api/login/',  {'username': doctor1.username, 'password':password})
    response = client.get('/api/doctorof/%s/'%str(uuid.uuid4()))
    assert response.status_code == 403, "Error! Expected 404, get %d" % response.status_code
    print("Pass!")

    print("Testing doctor non-exist PUT.", end=' ')
    response = client.post('/api/login/',  {'username': doctor1.username, 'password':password})
    response = client.put('/api/doctorof/%s/'%str(uuid.uuid4()), {'doctor_id':doctor1.id})
    assert response.status_code == 403, "Error! Expected 404, get %d" % response.status_code
    print("Pass!")

    print("Testing patient PUT empty.", end=" ")
    response = client.put('/api/doctorof/%s/'%str(user1.id), {'doctor_id':""})
    assert response.status_code == 400, "Error! Expected 400, get %d" % response.status_code
    print("Pass!")


    print("\n======= api/doctors/ ========")
    print('--- Valid requests ---' )
    # login as doctor1
    response = client.post('/api/login/', {'username': doctor1.username, 'password':password})
    print("Testing doctor GET.", end=" ")
    response = client.get('/api/doctors/')
    assert response.status_code == 200, "Error! Expected 200, get %d" % response.status_code
    doctors = response.data
    assert len(doctors) >= 2, "Error! Expect length >= 2, get %d" % len(patients)
    print(len(doctors), end=". ")
    print("Pass!")

    print('')