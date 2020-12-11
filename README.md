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

- Assign `doctor` to take care of `patient`. Only doctors, admins, and patients him/herselves can do the post.
- Patients cannot POST for other patients.
- `POST`
    - Request
        ```json
        {} - empty request
        ```
    - Response
        ```json
        {
            "id": int,
            "doctor" : {
                "id": UUID,
                "first_name": String,
                "last_name": String,
                "since": DateTime,
                "user_type": int    
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
                    "status": List<int> 
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
                    "status": List<int> 
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
- `PUT`
    - Update the doctor user takeCareOf relationship of given patient. 
    - Request
        ```json
        {
            doctor_id: UUID/String * 
        }
        ```
    - Response
        ```json
        {
            "id": int,
            "doctor" : {
                "id": UUID,
                "first_name": String,
                "last_name": String,
                "since": DateTime,
                "user_type": int    
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


[comment]: # ("/api/vs/<uuid:owner>/")
<details><summary><code>/api/vs/[uuid:owner]/</code>
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
    - Get all vital signs owned by the `owner` in the request URL
    - Response
        ```json
        {
            "query": "bracelet"
            "data": [
                {
                    "id": int,
                    "owner": UUID,
                    "bracelet": UUID,
                    "bracelet": UUID,
                    "temp": float,
                    "spo2": float,
                    "hr": float,
                    "rr": float,
                    "time": String
                },
                {
                    "id": int,
                    "owner": UUID,
                    "bracelet": UUID,
                    "bracelet": UUID,
                    "temp": float,
                    "spo2": float,
                    "hr": float,
                    "rr": float,
                    "time": String
                },
                ...
            ]
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