# Capstone project

the capstone project is a simple cloud application. It allows users to get, add, edit and delete actors or movies and also  assign/unassign an actor to/from a movie using movie_id and actor_id .
users can get all movies that an actor is assigned to or all actors assigned to  movie .
a user can be one of three role (RBAC):
- casting assistance
- casting director
- executif producer 

### Run the application locally

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install python version 3.7 for your platform in the [python docs](https://docs.python.org/3.7/using/unix.html#getting-and-installing-the-latest-version-of-python)
(ps: the specific version 3.7 is required to avoid errors with some packages)
#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

installing virtual enviroment
```bash
python -m venv env 
```
activating virtual enviroment
On macOS and Linux:
```bash
source env/bin/activate
```
On Windows:
```cmd
.\env\Scripts\activate
```
```bash
. ./env/Scripts/activate
```

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/capstone` directory and running:

```bash
cd capstone 
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.


## Running the server

From within the `/capstone` directory first ensure you are working using your created virtual environment.

create a postgres database for the project and export the Database path:

```bash
export DATABASE_URL=<your_database_path>;
```
the application uses auth0 as a third party authentication system, and it's already setup in auth0 
export the necessary env varsiables to let the app use it 

```bash
export AUTH0_DOMAIN=ta9i.auth0.com
export ALGORITHMS=RS256
export API_AUDIENCE=Capstone
```

run the migrations, execute:
```bash
python manage.py migrate
python manage.py upgrade
```

To run the server, execute:
```bash
python manage.py runserver
```


### (OPTIONAL) Setup your own Auth0 auth system for the application 

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token
5. Create new API permissions:
    - `add:actor`
    - `add:movie`
    - `delete:actor`
    - `delete:movie`
    - `modify:actor`
    - `modify:movie`
    - `get:actors_and_movies`
6. Create new roles for:
    - casting assistance
        - can `get:actors_and_movies`
    - casting director
        - can `add:actor`
        - can `modify:actor`
        - can `modify:movie`
        - can `get:actors_and_movies`
    - executif producer
        - can perform all actions
7. Test your endpoints with [Postman](https://getpostman.com). 
    - Register 3 users - assign each role to a user.
    - Sign into each account and make note of the JWT.

## Testing endpoints 

### getting the bearer token 
there are three registred user each has diffrent role :

export key_id and secret for the user with role "casting assistance" : 
- 
```bash
export CASTING_ASSISTANT_CID=kmK1TckHn29xdtr2b9M42IZsoQinxvUa
export CASTING_ASSISTANT_CSEC=r8QpWrMt6NqhPLZ-Y8MK8EtxHKvMUE8ZF81Fb2Y1VA6HEMn0SBgb0dvTTd72HaIk
```
export key_id and secret for the user with role "casting director" : 

```bash
export CASTING_DIRECTOR_CID=c1OtMNTgEKNErllV6T1RyrjxJUEnbwVJ
export CASTING_DIRECTOR_CSEC=Jsbemid1p8qzBFQ9mFyEnhkbmR1QahHNWImhJOCaZ8OxIn1BnMZNrTk7yHf4lGx7
```
export key_id and secret for the user with role "executif producer" : 
```bash
export EXECUTIVE_PRODUCER_CID=Yfv5eGbI3lkUCVNvmA2Zj8ybeWGiPRcN
export EXECUTIVE_PRODUCER_CSEC=SOgYFoeiiLpy2MILZNbas_cXZRu8tTmBlVE81N2vSo1Zu3DPj3ktmMFCZDukwOWS
```

copy the bearer token value from curl response 
```bash
curl --request POST \
  --url https://ta9i.auth0.com/oauth/token \
  --header 'content-type: application/json' \
  --data '{"client_id":<role_id>,"client_secret":<role_secret>,"audience":$API_AUDIENCE,"grant_type":"client_credentials"}`
  ```
  exemple :
```bash
curl --request POST \
  --url https://ta9i.auth0.com/oauth/token \
  --header 'content-type: application/json' \
  --data '{"client_id":CASTING_ASSISTANT_CID,"client_secret":CASTING_ASSISTANT_CSEC,"audience":$API_AUDIENCE,"grant_type":"client_credentials"}
  ```
### test with [Postman](https://getpostman.com).
- import the 'Capstone.postman_collection.json 
- Right-clicking the capstone folder ,navigate to the variables tab, change host value to the http://localhost:5000 as your app is running
- Right-clicking the each subfolder (casting assistance,casting director,executif producer)  ,navigate to the authorization tab,
- change type to bearer token and past value obtained earilyer then click save   
## Deploying your system
the applicaton is going to be deployed as a microservice in AWS EKS service , for that a cluser need to be created with a computing node group 
- allow travis to access this project repository on github
- set the enviroment variable from travis console :
```bash
    export AUTH0_DOMAIN=<your_own_setup>
    export ALGORITHMS=<your_own_setup>
    export API_AUDIENCE=<your_own_setup>
    export DATABASE_URL=<your_own_setup>
    export DOCKER_HUB_REPO=<your_own_setup>
    export DOCKER_PASSWORD=<your_own_setup>
    export DOCKER_USERNAME=<your_own_setup>
    export AWS_ACCESS_KEY_ID=<your_own_setup>
    export AWS_SECRET_ACCESS_KEY=<your_own_setup>
    export REGION=<your_own_setup>
    export CLUSTER_NAME=<your_own_setup> 
``` 
- git push to trigger Travis-ci  pipeline 