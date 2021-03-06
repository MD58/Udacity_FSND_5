## Casting Agency
### Overview & Motivation
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

I have developed this project to practice my knowledge in python obtained from the Udacity full stack developer nanodegree.

Please note that some of the functions are reused from my previous FSND projects.

#### Live Heroku URL
`https://md58-udacity-fsnd-capstone.herokuapp.com/`

#### Roles & Permissions
##### Casting Assistant
- get:actors
- get:movies

##### Casting Director
- get:actors
- get:movies
- patch:actors
- patch:movies
- post:actor
- delete:actor

##### Executive Producer
- get:actors
- get:movies
- patch:actors
- patch:movies
- post:actor
- delete:actor
- post:movies
- delete:movies


## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

##### Export the variables as environment variables
```bash
source setup.sh
```


## Database Setup

##### Update Connection String
[`config.py`](config.py)

##### Run the migrations
```bash
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```

## Running the server
From within the directory, simply execute:

```bash
python app.py
```

## Testing
##### Run the tests
```
python test_app.py
```

## Api Reference
### Error Handling
Error are returned as JSON objects in the following format:
```json
{
  "success" : False,
  "error" : 400,
  "message" : "bad request"
}
```
The API will return four error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 405: Method Not Allowed
- 422: Unprocessable
- 500: Internal Server Error

### Endpoints
#### GET /movies
- Returns a list of movies object as key:value pairs, success value and the total number of movies
- Sample curl:
```bash
curl -i -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" https://md58-udacity-fsnd-capstone.herokuapp.com/movies
```
- Sample response output:
```json
{
    "movies": [
        {
            "id": 1,
            "release_date": "Fri, 23 Apr 2004 00:00:00 GMT",
            "title": "Man on Fire"
        },
        {
            "id": 3,
            "release_date": "Fri, 04 Oct 2019 00:00:00 GMT",
            "title": "Joker"
        }
    ],
    "success": true,
    "total_movies": 2
}
```
#### POST /movies
- Returns the new posted movie with a success value
- Sample curl:
```bash
curl https://md58-udacity-fsnd-capstone.herokuapp.com/movies -X POST -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" -d '{"title":"The Boss", "release_date": "2016-04-08"}'
```
- Sample response output:
```json
{
    "movie": {
        "id": 7,
        "release_date": "Fri, 08 Apr 2016 00:00:00 GMT",
        "title": "The Boss"
    },
    "success": true
}
```

#### PATCH /movies
- Returns the updated movie with a success value
- Sample curl:
```bash
curl https://md58-udacity-fsnd-capstone.herokuapp.com/movies/7 -X PATCH -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" -d '{"title":"The Boss", "release_date": "2016-04-08"}'
```
- Sample response output:
```json
{
    "movie": {
        "id": 7,
        "release_date": "Fri, 08 Apr 2016 00:00:00 GMT",
        "title": "The Boss II"
    },
    "success": true
}
```

#### DELETE /movies
- Returns the id of the deleted movie with a success value
- Sample curl:
```bash
curl https://md58-udacity-fsnd-capstone.herokuapp.com/movies/7 -X DELETE -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}"
```
- Sample response output:
```json
{
    "delete": 7,
    "success": true
}
```

#### GET /actors
- Returns a list of actor object as key:value pairs, success value and the total number of actors
- Sample curl:
```bash
curl -i -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" https://md58-udacity-fsnd-capstone.herokuapp.com/actors
```
- Sample response output:
```json
{
    "actors": [
        {
            "age": 66,
            "gender": "male",
            "id": 5,
            "name": "Denzel Washington"
        },
        {
            "age": 50,
            "gender": "female",
            "id": 8,
            "name": "Melissa McCarthy"
        }
    ],
    "success": true,
    "total_actors": 2
}
```

#### POST /actors
- Returns the new posted actor with a success value
- Sample curl:
```bash
curl https://md58-udacity-fsnd-capstone.herokuapp.com/actors -X POST -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" -d '{"name":"James Robinson", "gender": "male", "date_of_birth": "1983-09-06"}'
```
- Sample response output:
```json
{
    "actor": {
        "age": 37,
        "gender": "male",
        "id": 2,
        "name": "James Robinson"
    },
    "success": true
}
```

#### PATCH /actors
- Returns the updated actor with a success value
- Sample curl:
```bash
curl https://md58-udacity-fsnd-capstone.herokuapp.com/actors/2 -X PATCH -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" -d '{"name":"James D", "gender": "male", "date_of_birth": "1982-09-06"}'
```
- Sample response output:
```json
{
    "actor": {
        "age": 36,
        "gender": "male",
        "id": 2,
        "name": "James D"
    },
    "success": true
}
```

#### DELETE /actors
- Returns the id of the deleted actor with a success value
- Sample curl:
```bash
curl https://md58-udacity-fsnd-capstone.herokuapp.com/actors/2 -X DELETE -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}"
```
- Sample response output:
```json
{
    "delete": 2,
    "success": true
}
```
