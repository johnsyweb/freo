# Freo

A Flask app that serves a Hello World page over HTTP.

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open [http://localhost:8080/](http://localhost:8080/). The port defaults to 8080; set `PORT` to use another.

## Run with Docker

```bash
docker build -t freo . && docker run --rm -p 8080:8080 freo
```

To use a different port, set `PORT` on the container and publish it, for example `-e PORT=9090 -p 9090:9090`.

## Tests

```bash
pip install pytest
pytest
```
