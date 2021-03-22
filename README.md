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
                    "since": DateTime,
                    "user_type": int,
                    "gender": int  
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
            id: UUID,
            first_name: String, 
            last_name: String, 
            user_type: int
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
                    "since": DateTime,
                    "user_type": int ,
                    "facility": <Facility>
                },
                {
                    "id": UUID,
                    "first_name": String,
                    "last_name": String,
                    "since": DateTime,
                    "user_type": int ,
                    "facility": <Facility>
                }
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
                    'id': UUID, 
                    'first_name': String, 
                    'last_name': String, 
                    'user_type': int, 
                    'gender': int, 
                    'belongs_to': UUID
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
                'id': UUID, 
                'first_name': String, 
                'last_name': String, 
                'user_type': int, 
                'gender': int, 
                'belongs_to': UUID
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
        {
          "message": string
        }
      ```
    - Response:
        - 200: the request is sent or the TakeCareOf is created
        - 404: either the requestor or the owner doesn't exist
        - 409: the request already exist in the database and the post is sent by the reqeustor not the owner
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
                    "since": DateTime,
                    "user_type": int,
                    "gender": int  
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