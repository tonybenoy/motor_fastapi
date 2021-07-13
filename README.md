# MongoMotorFastapi

## How to run server

I have the images tagged to my local registry so run a local registry as shown below. In case you don't want to run your own registry do change the image name to a non registry tag.

`docker run -d -p 5000:5000 --name registry registry:2`

## To run the server

### Using docker

```
docker-compose build
docker-compose push
docker-compose up
```

### Without Docker

```
python -m venv venv
source venv/bin/activate
pip install -r requirement.txt
gunicorn -b 0.0.0.0:8000 src.main:app -w 1 -k uvicorn.workers.UvicornWorker --preload
```

Access the server [here](http://127.0.0.1:8000)

## Running testcases

### Using docker

```
docker run -it localhost:5000/tony/studentep  python -m pytest -s test
```

### Locally

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m pytest -s test
```

### Github actions

See the test case status [here](https://github.com/tonybenoy/_/actions/workflows/python-app.yml)
