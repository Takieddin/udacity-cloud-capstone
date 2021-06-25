# Capstone project

the capstone project is a simple cloud application. It allows users to get, add, edit and delete actors or movies and also  assign/unassign an actor to/from a movie using movie_id and actor_id .
users can get all movies that an actor is assigned to or all actors assigned to  movie .
a user can be one of three role (RBAC):
- casting assistance
- casting director
- executif producer 

### Run the application locally
- Python 3.7 is required
- postgres Database is recommended 
- create virtual enviroment and activate it 
- install requirements using `pip install -r requirements.txt`
- export enviroment variables from setup.sh file : ./setup.sh
- modify the database_path in models.py file with your own database_path 
- run flask db migrations with `python manage.py db  migrate'
- run flask db upgrade `python manage.py db upgrade'
- run server `python manage.py runserver`
- get bearer token using `curl --request POST \
  --url https://ta9i.auth0.com/oauth/token \
  --header 'content-type: application/json' \
  --data '{"client_id":<role_id>,"client_secret":<role_secret>,"audience":$API_AUDIENCE,"grant_type":"client_credentials"}' 

  exemple :
`curl --request POST \
  --url https://ta9i.auth0.com/oauth/token \
  --header 'content-type: application/json' \
  --data '{"client_id":CASTING_ASSISTANT_CID,"client_secret":CASTING_ASSISTANT_CSEC,"audience":$API_AUDIENCE,"grant_type":"client_credentials"}' 

- in postman import the Capstone.postman_collection.json file and change the variable host to the app host and the authorization header to the obtained bearer token 
### Deploying your system
the applicaton is going to be deployed as a microservice in AWS EKS service , for that a cluser need to be created with a computing node group 
- allow travis to access this project repository on github
- set the enviroment variable from travis console :
    AUTH0_DOMAIN
    ALGORITHMS
    API_AUDIENCE
    DATABASE_URL
    DOCKER_HUB_REPO
    DOCKER_PASSWORD
    DOCKER_USERNAME
    AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY
    REGION
    CLUSTER_NAME 
- git push to trigger Travis-ci  pipeline 