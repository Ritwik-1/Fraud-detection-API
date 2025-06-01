1) What is an API?

API is an application program interface, it is sort of a function through which
a user or a application backend can interact with another application 
In case of ML, this application is your model, by creating an API, we can let users 
pass their data to our model to get predictions 

2) What is GET and POST 
POST is a HTTP request to send data to the server

2) What is a RestfulAPI?
REST : Representational state transfer

When you build a REST API in FastAPI, you're basically:

Defining endpoints (URLs)
Accepting inputs (from users or frontend)
Returning outputs (model predictions or messages)

endpoint : URL path that handles a specific request
eg. GET /status → check if the server is running

input / output : JSON format

