# Hubor
A Django project running on Raspberry Pi (or any local network)

# How to run
### Intall required modules
```
pip install -r ./requirements.txt
```

### Run the server with Docker
Assuming you have already have docker installed.
```
cd /Hubor/deployment/docker-noproxy
docker build -t hubor .
docker run -itdp 80:8000 hubor
```
Above command will run the server and listen to your 80 port.


### Run the server localy
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```
This will run at the IP address of your local machine with the port 8000

**Note**: To know your IP address under local network, try `ifconfig` in powershell and bash
# Supported APIs
## Accounts
[comment]: # ("/api/login/")
<details><summary><code>/api/login/</code>
</summary>
<p>

- Login a user
- `POST`
    - Request
        ```json
        {
            "username": String,
            "password": String
        }
        ```
    - Response
        ```json
        {
            "query": "login",
            "id": uuid
        }
        ```
</p>
</details>

[comment]: # ("/api/logout/")
<details><summary><code>/api/logout/</code>
</summary>
<p>

- logout request user. User info should be stored in client"s cookie.
- POST
    - Request
        ```json
        {} - empty payload
        ```
    - Response
        ```json
        {
            "query": "logout"
        }
        ```
</p>
</details>


[comment]: # ("/api/register/")
<details><summary><code>/api/register/</code>
</summary>
<p>

- Register a user
- `POST`
    - Request
        ```json
        {
            "username": String **,
            "email": String **,
            "height": float *,
            "weight": float *,
            "user_type": int (0=patient, 1=doctor, 2=admin),
            "phone": String **,
            "date_of_birth": String *,
            "gender": int (0=male, 1=female),
            "notes": Stirng,
            "password":String *,
            "first_name": String *,
            "last_name": String *
        }
        ```
    - Response
        ```json
        {
            "query": "register",
            "data": {
                "id": UUID,
                "email": String,
                "weight": float,
                "height": float,
                "user_type": int,
                "phone": String,
                "date_of_birth": Stirng,
                "gender": int,
                "notes": Sting
            }
        }
        ```
</p>
</details>


[comment]: # ("/api/bracelet/<uuid:owner>/")
<details><summary><code>/api/bracelet/[uuid:owner]/</code>
</summary>
<p>

- `POST`
    - Add a bracelet for the `owner` in the request URL
    - Request
        ```json
        {
            "mac_addr": String **
        }
        ```
    - Response
        ```json
        {
            "query": "bracelet",
            "bracelet": UUID
        }
        ```
- `GET`
    - Get all bracelets owned by the `owner` in the request URL
    - Response
        ```json
        {
            "query": "bracelet"
            "bracelets": [
                {
                    "id": UUID,
                    "owner": UUID,
                    "mac_addr": String
                },
                {
                    "id": UUID,
                    "owner": UUID,
                    "mac_addr": String
                },
                ...
            ]
        }
            
        ```
</p>
</details>

[comment]: # ("/api/takecareof/<uuid:doctor>/<uuid:patient>/")
<details><summary><code>/api/takecareof/[uuid:doctor]/[uuid:patient]/</code>
</summary>
<p>

- Check if given doctor has the permission of accessing the data of the givien patient
- `GET`
    - Check if given doctor is taking care of given patient
        - 200: if true
        - 404: 
            - `type=0`: either the doctor or the patient doesn't exist. 
            - `type=1`: the relationship doesn't exist.
        - 409: permission request still on hold
        - 403: request is sent by neither the given doctor nor the given patient
    - Response
        ```json
        4XX:
            {
                "message": string
            }
        404:
            {
                "message": string,
                "type": int  [0 (user doesn't exist) / 1 (no permission)]
            }
        200:
            {
                "id": int,
                "doctor" : {
                    "id": UUID,
                    "first_name": String,
                    "last_name": String,
                    "date_joined": DateTime,
                    "date_of_birth": DateTime,
                    "user_type": int,
                    "gender": int,
                    "phone": String,
                    "email": String,
                    "facility": <Facility>
                },
                "patient" : {
                    "id": UUID,
                    "first_name": String, 
                    "last_name": String, 
                    "user_type": int,
                    "height": int, 
                    "weigh"': int, 
                    "date_of_birth": datetime, 
                    "notes": String, 
                    "phone": String,
                    "status": List<int>     
                }
            }
        ```
- `DELETE`
    - Remove a given TakeCareOf relationship
    - Method can only be used by given patient or doctor
    - Response:
        - status code:
            - 200: succeed
            - 403: requestor is neither the given patient nor the doctor
            - 404: the relationship between given patient and the doctor is not found.
                   Or the given patient or the given doctor doens't exist
        - response:
            ```json
            {
                "message": string
            }
            ```
</p>
</details>

[comment]: # ("/api/patientsof/<uuid:doctor>/")
<details><summary><code>/api/patientsof/[uuid:doctor]/</code>
</summary>
<p>
- Get a list of patients of the given doctor

- `GET`
    - Response
        ```json
            [
                {
                    "id": UUID,
                    "first_name": String, 
                    "last_name": String, 
                    "user_type": int,
                    "height": int, 
                    "weight": int, 
                    "date_of_birth": datetime, 
                    "notes": String, 
                    "phone": String,
                    "status": List<int>,
                    "facility": <Facility>
                },
                {
                    "id": UUID,
                    "first_name": String, 
                    "last_name": String, 
                    "user_type": int,
                    "height": int, 
                    "weight": int, 
                    "date_of_birth": datetime, 
                    "notes": String, 
                    "phone": String,
                    "status": List<int>,
                    "facility": <Facility>
                }
            ]
        ```
</p>
</details>

[comment]: # ("/api/doctorof/<uuid:patient>/")
<details><summary><code>/api/doctorof/[uuid:patient]/</code>
</summary>
<p>
- Get and update the doctor's information of given patient

- `GET`
    - Get the doctor's information of the given patient
    - Response
        ```json
        {
            "id": UUID,
            "first_name": String,
            "last_name": String,
            "date_joined": DateTime,
            "date_of_birth": DateTime,
            "user_type": int,
            "gender": int,
            "phone": String,
            "email": String,
            "facility": <Facility>
        }
        ```
</p>
</details>

[comment]: # ("/api/doctors/")
<details><summary><code>/api/doctors/</code>
</summary>
<p>
- Get a list of registered doctors

- `GET`
    - Response
        ```json
            [
                {
                    "id": UUID,
                    "first_name": String,
                    "last_name": String,
                    "date_joined": DateTime,
                    "date_of_birth": DateTime,
                    "user_type": int,
                    "gender": int,
                    "phone": String,
                    "email": String,
                    "facility": <Facility>
                },
                ...
            ]
        ```
</p>
</details>

[comment]: # ("/api/facilities/")
<details><summary><code>/api/facilities/</code>
</summary>
<p>
- GET: Get a all facilities. Only short information included
- POST: Create a facility.

- `GET`
    - Response
        ```json
            [
                {
                    "id": UUID,
                    "name": String,
                    "address": String,
                    "phone": String,
                    "Description": String
                },
                {
                    "id": UUID,
                    "name": String,
                    "address": String,
                    "phone": String,
                    "Description": String
                }
            ]
        ```
- `POST`
    - Request
        ```json
        {
            "id": UUID,
            "name": String,
            "address": String,
            "phone": String,
            "Description": String
        }
        ```
    - Response
        ```json
        {
            "id": UUID,
            "name": String,
            "address": String,
            "phone": String,
            "Description": String
        }
        ```
</p>
</details>

[comment]: # ("/api/belongsto/<uuid:facility>")
<details><summary><code>/api/belongsto/[uuid:facility]</code>
</summary>
<p>
- GET: Get a all user belongs to given facility
- PUT: Create a belongs to relationship

- `GET`
    - Response
        ```json
        [
            {
                "id": UUID,
                "user": {
                    "id": UUID,
                    "first_name": String,
                    "last_name": String,
                    "date_joined": DateTime,
                    "date_of_birth": DateTime,
                    "user_type": int,
                    "gender": int,
                    "phone": String,
                    "email": String,
                    "facility": <Facility>
                },
                "facility":{
                    "id": UUID,
                    "name": String,
                    "address": String,
                    "phone": String,
                    "Description": String
                }
            },
            ...
        ]
        ```
- `PUT`
    - Request
        ```json
        {
            "user": UUID
        }
        ```
    - Response
        ```json
        {
            "id": UUID,
            "user": {
                "id": UUID,
                "first_name": String,
                "last_name": String,
                "date_joined": DateTime,
                "date_of_birth": DateTime,
                "user_type": int,
                "gender": int,
                "phone": String,
                "email": String,
                "facility": <Facility>
            },
            "facility":{
                "id": UUID,
                "name": String,
                "address": String,
                "phone": String,
                "Description": String
            }
        }
        ```
</p>
</details>

[comment]: # ("/api/accessrequest/<uuid:owner>/<uuid:requestor>/")
<details><summary><code>/api/accessrequest/[uuid:owner]/[uuid:requestor]/</code>
</summary>
<p>
- API allows requestor to send a request to the data owner so that he/she can access the vital sign data

- `POST`
    - requestor can be both requestor and the onwer.
        - Requestor POST: asking for the access.
        - Owner POST: Accept the request. this will delete the DataPermissionRequest tuple, but will create a 
          TakeCareOf object instead. If there is not existing request, then a TakeCareOf object will be created
          directly.
    - payload:
      ```json
        {} - empty payload
      ```
    - Response:
        - 200: the request is sent or the TakeCareOf is created
        - 404: either the requestor or the owner doesn't exist
        - 409: the request already exist in the database and the post is sent by the reqeustor not by the owner
        ```json
        4XX:
            {
                "message": string
            }
        200 - requestor:
            {
                "message": string
            }
        200 - owner:
            {
                "id": int,
                "doctor" : {
                    "id": UUID,
                    "first_name": String,
                    "last_name": String,
                    "date_joined": DateTime,
                    "date_of_birth": DateTime,
                    "user_type": int,
                    "gender": int,
                    "phone": String,
                    "email": String,
                    "facility": <Facility>
                },
                "patient" : {
                    "id": UUID,
                    "first_name": String, 
                    "last_name": String, 
                    "user_type": int,
                    "height": int, 
                    "weigh"': int, 
                    "date_of_birth": datetime, 
                    "notes": String, 
                    "phone": String,
                    "status": List<int>     
                }
            }
        ```
- `DELETE`
    - Reject or cancel the request
    - Status Code:
        - 200: the request is rejected.
        - 403: the requestor is neither the owner nor the requestor
        - 404: given request is not found
    - Response
        ```json
        {
            "message": string
        }
        ```
</p>
</details>

[comment]: # ("/api/mypendingrequests/")
<details><summary><code>/api/mypendingrequests/</code>
</summary>
<p>

- API allows user to get a list of their pending requests
- GET
    - Get a list of their pending requests
    - Response:
        - status codes:
            - `200`: Response with a list of pending requests
            - `404`: no pending requests found
        - response:
            ```json
            200:[
                    {
                        "id": int,
                        "owner" : {
                            "id": UUID,
                            "first_name": String,
                            "last_name": String,
                            "date_joined": DateTime,
                            "date_of_birth": DateTime,
                            "user_type": int,
                            "gender": int,
                            "phone": String,
                            "email": String,
                            "facility": <Facility>
                        },
                        "requestor": {
                            "id": UUID,
                            "first_name": String,
                            "last_name": String,
                            "date_joined": DateTime,
                            "date_of_birth": DateTime,
                            "user_type": int,
                            "gender": int,
                            "phone": String,
                            "email": String,
                            "facility": <Facility>
                        }
                        ...
                    },
                    ...
                ]
            400:{
                "message": string
            }
            ```
</p>
</details>

[comment]: # ("/api/myinfo/")
<details><summary><code>/api/myinfo/</code>
</summary>
<p>

- API allows user to get his/her basic info
- GET
    - Get an object of personal info
    - Response:
        - status codes:
            - `200`: Response with a current user's info
        - response:
            ```json
            {
                "id": UUID,
                "first_name": String,
                "last_name": String,
                "date_joined": DateTime,
                "date_of_birth": DateTime,
                "user_type": int,
                "gender": int,
                "phone": String,
                "email": String,
                "facility": <Facility>
            }
            ```
</p>
</details>

## Data & Vital Sign
[comment]: # ("/api/data/<uuid:pk>/")
<details><summary><code>/api/data/[uuid:pk]/</code>
</summary>
<p>

- `POST`
    - Add an entry of raw data for the `owner` in the request URL
    - Request
        ```json
        {
            "bracelet": UUID *,
            "tem": float *,
            "acx": float *,
            "acz": float *,
            "bat": float *,
            "red": float *,
            "ir": float *,
            "time": String
        }
        ```
    - Response
        ```json
        {}
        ```
- `GET`
    - Get all raw data owned by the `owner` in the request URL
    - Response
        ```json
        {
            "query": "bracelet"
            "data": [
                {
                    "id": int,
                    "owner": UUID,
                    "bracelet": UUID,
                    "tem": float,
                    "acx": float,
                    "acz": float,
                    "bat": float,
                    "red": float,
                    "ir": float,
                    "time": String
                },
                {
                    "id": int,
                    "owner": UUID,
                    "bracelet": UUID,
                    "tem": float,
                    "acx": float,
                    "acz": float,
                    "bat": float,
                    "red": float,
                    "ir": float,
                    "time": String
                },
                ...
            ]
        }
            
        ```
</p>
</details>


[comment]: # ("/api/vitalsign/<uuid:owner>/?from=<time_with_time_zone>&to=<time_with_time_zone>&type=['min', 'hr', 'day', 'month']")
<details><summary><code>/api/vitalsign/[uuid:owner]/</code>
</summary>
<p>

- `POST`
    - Add an entry of vital sign for the `owner` in the request URL
    - Request
        ```json
        {
            "bracelet": UUID *,
            "temp": float *,
            "spo2": float *,
            "hr": float *,
            "rr": float *,
            "time": String
        }
        ```
    - Response
        ```json
        {}
        ```
- `GET`
    - Get all vital signs owned by the `owner` in the request URL within a specific time. 
    - The array is in **ascending** order in terms of time.
    - Response
        ```json
        [
            {
                "time": datetime,
                "hr": {
                    "mean": float,
                    "med": float,
                    "min": float,
                    "max": float,
                    "std": float,
                },
                "rr": {
                    "mean": float,
                    "med": float,
                    "min": float,
                    "max": float,
                    "std": float,
                },
                "spo2": {
                    "mean": float,
                    "med": float,
                    "min": float,
                    "max": float,
                    "std": float,
                },
                "temp": {
                    "mean": float,
                    "med": float,
                    "min": float,
                    "max": float,
                    "std": float,
                },
            },
            ...
        ]   
        ```
</p>
</details>

[comment]: # ("normalrange/<uuid:patient>/<str:typerange>/")
<details><summary><code>/api/normalrange/[uuid:patient]/[str:typerange]/</code>
</summary>
<p>

- `PUT`:
    - API for updating and creating an entry of a normal range
    - request:
        ```json
        {
            "value": number
        }
        ```
    - response:
        - 400: request is invalid
        - 403: the request is forbidened
        - 200: success
            ```json
            {
                "hr_l": number,
                "hr_h": number,
                "temp_l": number,
                "temp_h": number,
                "rr_l": number,
                "rr_h": number,
                "spo2_l": number,
                "spo2_h": number,
                "bplh_l": number,
                "bph_h": number,
                "bpl_l": number,
                "bpl_h": number
            }
            ```

</p>
</details>


[comment]: # ("/api/allnormalrange/<uuid:patient>/")
<details><summary><code>/api/allnormalrange/[uuid:patient]/</code>
</summary>
<p>

- `GET`:
    - get all normal ranges of given patient
    - response:
        - 404: given patient is not found or given patient has no normal ranges
        - 403: the request is forbidened
        - 200: success
            ```json
            {
                "hr_l": number,
                "hr_h": number,
                "temp_l": number,
                "temp_h": number,
                "rr_l": number,
                "rr_h": number,
                "spo2_l": number,
                "spo2_h": number,
                "bplh_l": number,
                "bph_h": number,
                "bpl_l": number,
                "bpl_h": number
            }
            ```
            
</p>
</details>

## Emergency
[comment]: # ("/api/emergency/<uuid:pk>/")
<details><summary><code>/api/emergency/[uuid:pk]/</code>
</summary>
<p>

- `POST`
    - Initiate an emergency event
    - Request
        ```json
        {
            "longitude": float *,
            "latitude": float *,
            "configuration": int *,
            "risk" : int * (0="LOW", 1="MID", 2="HIGH")
            "time": String
        }
        ```
    - Response
        ```json
        {}
        ```
- `GET`
    - Get a list of emergency events sent by given user
    - Response
        ```json
        {
            "data": [
                {
                    "id" = UUID,
                    "patient" = UUID,
                    "time" = String,
                    "solved" = int,
                    "longitude" = float,
                    "latitude" = float,
                    "configuration": int
                },
                {
                    "id" = UUID,
                    "patient" = UUID,
                    "time" = String,
                    "solved" = int,
                    "longitude" = float,
                    "latitude" = float,
                    "configuration": int
                },
                ...
            ]
        }
        ```
</p>
</details>


[comment]: # ("/api/emergencycontacts/<uuid:pk>/")
<details><summary><code>/api/emergencycontacts/[uuid:pk]/</code>
</summary>
<p>

- `POST`
    - Create an emergency contact for given user
    - Request
        ```json
        {
            "first_name": string,
            "last_name": string,
            "phone": string,
            "email": string,
        }
        ```
    - response:
        - status code:
            - 200: success
            - 404: given user not found
            - 403: permission denied (the request is sent neither by the patient him/herself nor the doctor who's taking care of the given user)
            - 409: the given patient already has 3 emergency contacts
- `GET`
    - Get a list of emergency contacts of given user
    - Response
        ```json
        [
                {emergency_contact_1},
                {emergency_contact_2},
                ...
                {emergency_contact_3}
        ]
        ```
</p>
</details>

## Configuration
[comment]: # ("/api/config/<int:version>/")
<details><summary><code>/api/config/[int:version]/</code>
</summary>
<p>

- `GET`
    - Get the corresponding version of configuration
    - Response
        ```json
        {
            "config": [
                {
                    "id": int,
                    "name": String,
                    "version": int,
                    "compare": int,
                    "range_min": float,
                    "range_max": float,
                    "duration": int
                },
                {
                    "id": int,
                    "name": String,
                    "version": int,
                    "compare": int,
                    "range_min": float,
                    "range_max": float,
                    "duration": int
                },
                ...
            ]
        }
        ```
</p>
</details>

[comment]: # ("/api/latestconfig/")
<details><summary><code>/api/latestconfig/</code>
</summary>
<p>

- `GET`
    - Get the latest version of configuration
    - Response
        ```json
        {
            "config": [
                {
                    "id": int,
                    "name": String,
                    "version": int,
                    "compare": int,
                    "range_min": float,
                    "range_max": float,
                    "duration": int
                },
                {
                    "id": int,
                    "name": String,
                    "version": int,
                    "compare": int,
                    "range_min": float,
                    "range_max": float,
                    "duration": int
                },
                ...
            ]
        }
        ```
</p>
</details>