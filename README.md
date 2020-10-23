# jwt-auth-api
JSON Web Token Authentication with Django


## Endpoint:

- `Development`
  
  ```bash
  http://127.0.0.1:8000/api/v1/users/register/
  http://127.0.0.1:8000/api/v1/users/login/
  http://127.0.0.1:8000/api/v1/users/profile/
  http://127.0.0.1:8000/api/v1/users/token/refresh/
  ```
- `Production`

  ```bash
  http://[public_ip/domain]/api/v1/users/register/
  http://[public_ip/domain]/api/v1/users/login/
  http://[public_ip/domain]/api/v1/users/profile/
  http://[public_ip/domain]/api/v1/users/token/refresh/
  ```

## Setup:

- `Dev mode`

  ```bash
  $ viertualenv -p python3 venv
  $ source venv/bin/activate
  (venv)$ pip install -r requirements-dev.txt
  (venv)$ ./manage.py runserver --settings=jwt_auth.settings.devs
  ```

- `Prod mode` (Docker)
  
  ```bash
  $ docker-compose build
  $ docker-compose up
  ```
