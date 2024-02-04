# What this repo contains?
This repository contains client and server apps. I do not have much experience in building such apps, but did my best and took aim to improve them! If you have any suggestions or advices make shure to share them with me!
## Server
Server is a django-based app used to store and send data to endpoints.
Server app includes:
1. Custom OAuth2 implemetnation for the client
2. REST API to work with the client
3. Simple app to show DB's content
   
You can see all the API endpoints on localhost:8000/api/swagger or download .yaml file localhost:8000/api/schema

## Client
Client is a Flask-based app used for authorizing user with OAuth2 on the server side and use recieved token to display some info.
