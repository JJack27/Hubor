from django.test import TestCase

# Create your tests here.
from rest_framework.test import APIRequestFactory, APIClient
from api.test_util import *
import uuid


client = APIClient()

# login as user 1
id = "b7b12657ed7a4f2fa6cddd2e5abf92f5"
user1 = User.objects.get(id=id) #create_user(client, 0)
login(client, user1)
response = client.get('/api/latest1hourvs/%s/'%str(user1.id))
assert response.status_code == 200, "Error!, expecting 200, get %d"%response.status_code
assert len(response.data) == 60, "Error!, expecting 60, get %d"%len(response.data)
