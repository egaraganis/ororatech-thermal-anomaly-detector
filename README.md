# OroraTech Assignment

## Running

### Through terminal

From `code/src` folder

```sh
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
$ fastapi dev main.py
```

### Through container

From `code` folder

```sh
$ docker build -t myimage .
$ docker run -d --name mycontainer -p 8000:80 myimage
```

### Deploy whole infra

From `root` folder

```sh
$ docker-compose pull
$ docker-compose build
$ docker-compose up
```