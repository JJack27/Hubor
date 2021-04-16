from django.test import TestCase

# Create your tests here.
from rest_framework.test import APIRequestFactory, APIClient
from api.test_util import *
import uuid


client = APIClient()

# login as user 1
id = "fb2796d56e444fac80d6e15261a7190c"
user1 = User.objects.get(id=id) #create_user(client, 0)
user2 = create_user(client, 0)
doctor1 = create_user(client, 1)
doctor2 = create_user(client, 1)

response = login(client, user1)
assert response.status_code == 200, "Error!, expecting 200, get %d"%response.status_code

put_payload = {"value": 0}
put_payload['value'] = 40

# test PUT /api/normalrange/<patient:uuid>/<type_range:string>/<type_range:string>/
print("================= PUT ==================")
print("----------- user1 -----------")
print("PUT  /api/normalrange/<patient:uuid>/<type_range:string>/", end=" ")
response = client.put('/api/normalrange/%s/hr_l/'%(str(user1.id)), put_payload)
assert response.status_code == 200, "Error!, expecting 200, get %d"%response.status_code
assert response.data['hr_l'] == 40, "Error!, expecting 40, get %d"%response.data['hr_l']
id1 = response.data['hr_l']
print("PASS!")

print("UPDATE PUT  /api/normalrange/<patient:uuid>/<type_range:string>/", end=" ")
put_payload['value'] = 45
response = client.put('/api/normalrange/%s/hr_l/'%(str(user1.id)), put_payload)
assert response.status_code == 200, "Error!, expecting 409, get %d"%response.status_code
assert response.data['hr_l'] == 45, "Error!, expecting 45, get %d"%response.data['hr_l']
print("PASS!")

print("INVALID=VALUE PUT  /api/normalrange/<patient:uuid>/<type_range:string>/", end=" ")
put_payload['value'] = -10
response = client.put('/api/normalrange/%s/hr_l/'%(str(user1.id)), put_payload)
assert response.status_code == 400, "Error!, expecting 400, get %d"%response.status_code
print("PASS!")

print("INVALID=type_of_range PUT  /api/normalrange/<patient:uuid>/<type_range:string>/", end=" ")
response = client.put('/api/normalrange/%s/hr_x/'%(str(user1.id)), put_payload)
assert response.status_code == 400, "Error!, expecting 400, get %d"%response.status_code
print("PASS!")

print("INVALID=vs PUT  /api/normalrange/<patient:uuid>/<type_range:string>/", end=" ")
response = client.put('/api/normalrange/%s/asdf_l/'%(str(user1.id)), put_payload)
assert response.status_code == 400, "Error!, expecting 400, get %d"%response.status_code
print("PASS!")

# let doctor1 has the permission of user 1
print("PUT  /api/accessrequest/<uuid:owner>/<uuid:requestor>/", end=" ")
response = client.post('/api/accessrequest/%s/%s/'%(str(user1.id), str(doctor1.id)), {})
assert response.status_code == 200, "Error!, expecting 400, get %d"%response.status_code
print("PASS!")

# check if the permission is granted
print("GET  /api/takecareof/<uuid:doctor>/<uuid:patient>/", end=" ")
response = client.get('/api/takecareof/%s/%s/'%(str(doctor1.id), str(user1.id)), {})
assert response.status_code == 200, "Error!, expecting 400, get %d"%response.status_code
print("PASS!")

print("----------- doctor1 -----------")
login(client, doctor1)
put_payload['value'] = 16

print("PUT  /api/normalrange/<patient:uuid>/<type_range:string>/", end=" ")
response = client.put('/api/normalrange/%s/rr_l/'%(str(user1.id)), put_payload)
assert response.status_code == 200, "Error!, expecting 200, get %d"%response.status_code
assert response.data['rr_l'] == 16, "Error!, expecting 16, get %d"%response.data['rr_l']
print("PASS!")

print("----------- doctor2 -----------")
login(client, doctor2)
print("PUT  /api/normalrange/<patient:uuid>/<type_range:string>/", end=" ")
response = client.put('/api/normalrange/%s/rr_h/'%(str(user1.id)), put_payload)
assert response.status_code == 403, "Error!, expecting 403, get %d"%response.status_code
print("PASS!")

# test GET /api/normalrange/<patient:uuid>/<type_range:string>/
print("================= GET ==================")
print("----------- doctor1 -----------")
login(client, doctor1)
print("GET  /api/allnormalrange/<patient:uuid>/", end=" ")
response = client.get('/api/allnormalrange/%s/'%(str(user1.id)))
assert response.status_code == 200, "Error!, expecting 200, get %d"%response.status_code
assert response.data['hr_l'] == 45, "Error!, expecting 40, get %d"%response.data['hr_l']
print("PASS!")

print("----------- user1 -----------")
login(client, user1)
print("GET  //api/allnormalrange/<patient:uuid>/", end=" ")
response = client.get('/api/allnormalrange/%s/'%(str(user1.id)))
assert response.status_code == 200, "Error!, expecting 200, get %d"%response.status_code
assert response.data['hr_l'] == 45, "Error!, expecting 40, get %d"%response.data['hr_l']
print("PASS!")

print("GET UNAUTHORIZED  /api/allnormalrange/<patient:uuid>/", end=" ")
response = client.get('/api/allnormalrange/%s/'%(str(user2.id)))
assert response.status_code == 403, "Error!, expecting 403, get %d"%response.status_code
print("PASS!")

