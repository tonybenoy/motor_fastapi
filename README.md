# MongoMotorFastapi

## How to run server

I have the images tagged to my local registry so run a local registry as shown below. In case you don't want to run your own registry do change the image name to a non registry tag.

`docker run -d -p 5000:5000 --name registry registry:2`

## To run the server

Create .env with MONGODB_URL

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
