from django.test import TestCase
from rest_framework.test import APIRequestFactory, APIClient
import random
import uuid
import datetime
from accounts.models import *
from data.models import *
from . import test_user as user_test
from . import test_data as data_test
from . import test_emergency as emergency_test

# Create your tests here.
test_user = False
test_data = False
test_emergency = True
test_config = False

# Testing views_user.py
if(test_user):
    user_test.run()

# Testing views_data.py
if(test_data):
    data_test.run()


if(test_emergency):
    emergency_test.run()

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