## wallet system

A wallet system with three user types (noob, elite and admin)

## Installation process

Download Docker to your machine

`https://docs.docker.com/get-docker/`

## BUILD 

`docker-compose build`

## Usage

`docker-compose up`

To start a local instance on your machine. 

Navigate to `127.0.0.1:5000/api/v1/signup` on postman 

Select body menu 

choose raw parameter

add this seed data

`
{
        'email': 'john@yahoo.com',
        'password': 'helloworld123',
        'currency': 'NGN',
        'user_type': 'noob',
        'access': {
            "noob": True,
            "elite": False,
            "admin": False
}
`

Server address = http://https://walletsys.herokuapp.com/api/v1



