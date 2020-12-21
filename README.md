# Casting Agency Project

The casting agency is an application for movie producer, directer and casting assiestent to view, add, delete and update movies and actors.

There are three roles in this application.

1) Executive Producer: can add movies & actors, delete movies & actors, update movies & actors, view movies & actors.
2) Casting Director:  can add actors, delete actors, update movies & actors, view movies & actors.
3) Casting Assistant: can view movies & actors.

Motivation: This is the final project in Full Stack Nanodegree. In this project I have used all the techniques I learned from this course in creating the casting agency project.

Heroku URL: https://castingagencyfarah.herokuapp.com/

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies  
for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/starter` directory and running:

```bash
pip install -r requirements.txt   
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the `./starter` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=app.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Testing
for testing the endpoint using postman.

import the postman collection in
```bash
./starter/agency.postman_collection.json
```
for testing the database run:
```bash
python test_app.py
```


## API Documentation
### Roles
    - Casting Assistant
        - Can view actors and movies
          - `get:actors`
          - `get:movies`
    - Casting Director
        - All permissions a Casting Assistant has and…
        - Add or delete an actor from the database
        - Modify actors or movies
          - `get:actors`
          - `get:movies`
          - `post:actors`
          - `patch:actors`
          - `patch:movies`
          - `delete:actors`
    - Executive Producer
        - All permissions a Casting Director has and…
        - Add or delete a movie from the database
            - `get:actors`
            - `get:movies`
            - `post:actors`
            - `post:movies`
            - `patch:actors`
            - `patch:movies`
            - `delete:actors`
            - `delete:movies`
### Endpoints
#### GET ./actors
    - Fetches all the actors in the database.
    - Request Argument: None
    - Response: Success message & all the actors
    Example response
    {
  "actors": [
    {
      "name": "jane",
      "age": 36,
      "gender": "Female",
      "id": 1,
    },
    {
      "name": "noura",
      "age": 24,
      "gender": "female",
      "id": 2,
    }
  ],
  "success": true
}
#### GET ./movies
    - Fetches all the movies in the database.
    - Request Argument: None
    - Response: Success message & all the movies
    Example response
    {
  "movies": [
    {
      "title": "nona",
      "release_date": 2014
    },
    {
      "title": "Harry Potter and the Sorcerer's Stone",
      "release_date": 2001
    }
  ],
  "success": true
}

#### POST ./actors
    - Fetches all the fields which are the name age and gender of the actor and check if the fields are empty or not.
       If empty abort(422) will happen, Else it will be added to the database.
    - Request Argument: Name, Age, Gender
    - Response: Success message & return the new actor.
    Example response
    {
  "actors": [
    {
      "name": "farah",
      "age": 22,
      "gender": "Female",
    }
  ],
  "success": true
}

#### POST ./movies
    - Fetches all the fields which are the title and release_date of the movie and check if the fields are empty or not.
       If empty abort(422) will happen, Else it will be added to the database.
    - Request Argument: title, release_date
    - Response: Success message & return the new movie.
    Example response
    {
  "actors": [
    {
      "title": "Harry Potter and the Sorcerer's Stone",
      "release_date": 2001
    }
  ],
  "success": true
}

#### PATCH ./actors
    - Fetches the age field of the actor based on the actor id then it will be updated on the database.
    - Request Argument:  new Age
    - Response: Success message & Id &  the updated actor age.
    Example response
    {
  "age": 22,
  "id": 1,
  "success": true
}

#### PATCH ./movies
    - Fetches the title field of the movie based on the movie id then it will be updated on the database.
    - Request Argument:  new title
    - Response: Success message & Id &  the updated actor age.
    Example response
    {
  "title": "Harry Potter and the Chamber of Secrets",
  "id": 1,
  "success": true
}

#### DELETE ./actors
    - Check the id if actor id exist on the database. if it does it will be delete it else abort(404) will happen
    - Request Argument: nothing
    - Response: Success message & Id of the deleted actor.
    Example response
    {
  "success": true,
  "actor_id": 1
}

#### DELETE ./movies
    - Check the id if movie id exist on the database. if it does it will be delete it else abort(404) will happen
    - Request Argument: nothing
    - Response: Success message & Id of the deleted movie.
    Example response
    {
  "success": true,
  "movie_id": 1
}