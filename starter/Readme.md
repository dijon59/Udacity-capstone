# Full Stack Casting Agency API Backend

## Casting Agency Specifications

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process. 

## Motivation for project

This is the capstone project of Udacity fullstack nanodegree program, which demonstrate the skillset of
using Flask, SQLAlchemy, Auth0, gunicorn and heroku to develop and deploy a RESTful API. 

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### Setting up the database

To run the tests on the api, you must add atleast 3 movies and 3 actors in the database.

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip3 install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the file directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
python3 app.py
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

## Tasks

### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token
5. Create new API permissions:
    - `get:actors`
    - `post:actors`
    - `patch:actors`
    - `delete:actors`
    - `get:movies`
    - `post:movies`
    - `patch:movies`
    - `delete:movies`
6. Create new roles for:
    - Casting Assistant
        - Can view actors and movies`
    - Casting Director
        - All permissions a Casting Assistant has and ...
        - Add or delete an actor from the database 
        - Modify actors or movies
    - Executive Producer
        - All permissions a Casting Director has and ...
        - Add or delete a movie from the database
7. Test your endpoints with [Postman](https://getpostman.com). 
    - Register 3 users - assign the Casting Assistant role to one    and Casting Director role to another, and Executive Producer   to the other.
    - Sign into each account and make note of the JWT.
    - Test each endpoint and correct any errors.

## Test app Page  

https://udacity-capstone-final.herokuapp.com/

Test each endpoint with the link above ,and different role's Jwts. 
Please click on the below link in order to get the jwts token, you will be asked to enter your username and password number
https://udacity-capstone-project.auth0.com/authorize?audience=capstone-app&response_type=token&client_id=gXKxa4l3Lc2s35Y3etYL3RY1pJPgJqfX&redirect_uri=http://localhost:5000/

```
- Casting Assistant
    - UserName: assistant@mytest.com
    - Password: Udacity@456
- Casting Director
    - UserName: director@mytest.com
    - Password: Udacity@456
- Executive Producer
    - UserName: producer@mytest.com
    - Password: Udacity@456
```

## Endpoints documentation

#### `GET '/movies'`
- Fetches a dictionary of movies
- Returns: Returns Json data about movies 
- Success Response:
```
{
    "movies": [
        {
            "id": 1,
            "release_date": "Tue, 01 May 2020 00:00:00 GMT",
            "title": "The end",
            "cast": ["dijon", "nathan"]
        },
        {
            "id": 2,
            "release_date": "Wed, 12 Aug 2020 00:00:00 GMT",
            "title": "Anaconda 3",
            "cast": ["nathan", "fred"]
        }
    ],
    "status_code": 200,
    "status_message": "OK",
    "success": true
}
```

#### `GET '/actors'`
- Fetches a dictionary of actors
- Returns: Json data about actors
- sample:

```
  {
    "actors": [
        {
            "age": 10,
            "gender": "male",
            "id": 1,
            "name": "Fred",
            "movies": ["The end"]
        },
        {
            "age": 20,
            "gender": "other",
            "id": 2,
            "name": "Dijon",
            "movies": ["Anaconda 3"]
        },
        {
            "age": 35,
            "gender": "female",
            "id": 3,
            "name": "nathan",
            "movies": ["The end", "Anaconda 3"]
        }
    ],
    "status_code": 200,
    "status_message": "OK",
    "success": true
}
```

#### `DELETE '/movies/<int:movie_id>'`
- Deletes the `movie_id` of movie
- Required URL Arguments: `movie_id` 
- Returns: Json data
- sample:
```
{
    "id_deleted": 7,
    "status_code": 200,
    "status_message": "OK",
    "success": true
}
```

#### `DELETE '/actors/<int:actor_id>'`
- Deletes actor
- Required URL Arguments: `actor_id` 
- Returns: Json data 
- sample:
```
{
    "id_deleted": 4,
    "status_code": 200,
    "status_message": "OK",
    "success": true
}
```
#### `POST '/assign_movie_to_actor'`
- Deletes actor
- Returns: Json data 
- sample:
```
{
    "success": True,
    "status_code": 200,
    "status_message": "OK",

}
```

#### `POST '/movies'`
- Post a new movie in a database.
- Required Data Arguments:  Json data                
- sample:
```
{
    "movie": {
        "id": 6,
        "release_date": "Thu, 01 Aug 2002 00:00:00 GMT",
        "title": "Toy Story",
    },
    "status_code": 200,
    "status_message": "OK",
    "success": true
}
```

#### `POST '/actors'`
- Post a new actor in a database.
- Required Data Arguments:  Json data   
- sample:
```
{
    "actor": {
        "age": 25,
        "gender": "female",
        "id": 4,
        "name": "Sarah",
    },
    "status_code": 200,
    "status_message": "OK",
    "success": true
}
```


#### `PATCH '/movies/<int:movie_id>'`
- Updates movie
- Required URL Arguments: `movie_id` 
- Returns: Json data about the updated movie 
- sample:
```
{
    "movie": {
        "id": 5,
        "release_date": "Wed, 05 April 2020 00:00:00 GMT",
        "title": "Avenger"
    },
    "status_code": 200,
    "status_message": "OK",
    "success": true
}
```

#### `PATCH '/actors/<int:actor_id>'`
- Updates the actor
- Required URL Arguments: `actor_id` 
- Returns: Json data about the deleted actor's ID 
- sample:
```
{
    "actor": {
        "age": 28,
        "gender": "other",
        "id": 4,
        "name": "Penny"
    },
    "status_code": 200,
    "status_message": "OK",
    "success": true
}
```

### Tests
In order to run tests navigate to the backend folder and run the following commands: 

```
$ dropdb capstone_test
$ createdb capstone_test
$ python test_app.py
```

The first time you run the tests, omit the dropdb command and also uncomment `db.create_all()` which located in the 
`models.py` file of the project.

All tests are kept in that file and should be maintained as updates are made to app functionality. 
