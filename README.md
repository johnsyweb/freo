# Freo

A Flask app that serves a Hello World page over HTTP.

## Prerequisites

- [mise](https://mise.en.dev/) for Python and project tasks
- Docker, for building and running the image

## Bootstrap

From the project root:

```bash
mise trust
mise run bootstrap
```

This installs Python 3.14 (matching the Docker image), creates `.venv`, and installs Flask plus pytest. Missing tools are installed when you run a task.

## Tasks

| Task | Command | What it does |
| --- | --- | --- |
| Bootstrap | `mise run bootstrap` | Install Python dependencies |
| Test | `mise run test` | Run the test suite |
| Local | `mise run local` | Run the app on the host |
| Build | `mise run build` | Build the `freo` image |
| Docker | `mise run docker` | Build the image (if needed) and run it |

The app listens on port 8080. Open [http://localhost:8080/](http://localhost:8080/). Set `PORT` to use another port locally. For Docker, set `PORT` on the container and publish it, for example `-e PORT=9090 -p 9090:9090`.
