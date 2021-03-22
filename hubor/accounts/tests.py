from django.test import TestCase
from rest_framework.test import APIRequestFactory, APIClient
import random
import uuid
import datetime
from accounts.models import *
from .test_util import *

# Create your tests here.
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

'''
Test of Data Permission
'''
print("======== Testing Data Permission Related ========")

login(client, doctor1)

print("doctor1 -> user1", end=" ")
response = client.post('/api/accessrequest/%s/%s/'%(str(user1.id), str(doctor1.id)), {})
assert response.status_code == 200, "Expecting status code 200, get %d" % response.status_code
print("Pass!")

print("(duplicated) doctor1 -> user1", end=" ")
response = client.post('/api/accessrequest/%s/%s/'%(str(user1.id), str(doctor1.id)), {})
assert response.status_code == 409, "Expecting status code 409, get %d" % response.status_code
print("Pass!")

print('api/takecareof/doctor1/user1/ (as doctor1)', end=" ")
response = client.get('/api/takecareof/%s/%s/'%(str(doctor1.id), str(user1.id)), {})
assert response.status_code == 409, "Expecting status code 409, get %d" % response.status_code
print("Pass!")


logout(client)
login(client, user1)
print('user1 -> user1 + doctor1', end=" ")
response = client.post('/api/accessrequest/%s/%s/'%(str(user1.id), str(doctor1.id)), {})
assert response.status_code == 200, "Expecting status code 200, get %d" % response.status_code
print("Pass!")

print('(duplicated) user1 -> user1 + doctor1', end=" ")
response = client.post('/api/accessrequest/%s/%s/'%(str(user1.id), str(doctor1.id)), {})
assert response.status_code == 404, "Expecting status code 404, get %d" % response.status_code
print("Pass!")

print('api/takecareof/doctor1/user1/ (as user1)', end=" ")
response = client.get('/api/takecareof/%s/%s/'%(str(doctor1.id), str(user1.id)))
assert response.status_code == 200, "Expecting status code 200, get %d" % response.status_code
print("Pass!")

logout(client)
login(client, doctor1)
print('api/takecareof/doctor1/user1/ (as doctor1)', end=" ")
response = client.get('/api/takecareof/%s/%s/'%(str(doctor1.id), str(user1.id)))
assert response.status_code == 200, "Expecting status code 200, get %d" % response.status_code
print("Pass!")

logout(client)
login(client, doctor2)
print('doctor2 -> user1 + doctor1', end=" ")
response = client.post('/api/accessrequest/%s/%s/'%(str(user1.id), str(doctor1.id)), {})
assert response.status_code == 403, "Expecting status code 403, get %d" % response.status_code
print("Pass!")

print('api/takecareof/doctor1/user1/ (as doctor2)', end=" ")
response = client.get('/api/takecareof/%s/%s/'%(str(doctor1.id), str(user1.id)))
assert response.status_code == 403, "Expecting status code 403, get %d" % response.status_code
print("Pass!")
logout(client)