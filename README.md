# Freo

A Flask app that serves a Hello World page over HTTP.

Freo is a Hello World example: one HTML page, one route, runnable on the host or in Docker.

## Getting started

Install [mise](https://mise.en.dev/), then from the project root:

```bash
mise trust
mise run local
```

Open [http://localhost:8080/](http://localhost:8080/).

## Help

This project is unsupported.

## Maintainers

[johnsyweb](https://github.com/johnsyweb)

## Development status

Experimental.

## Local development

Python 3.14 is pinned in `mise.toml`. Docker is required only for image tasks.

```bash
mise run bootstrap
```

| Task | Command |
| --- | --- |
| Install dependencies | `mise run bootstrap` |
| Run tests | `mise run test` |
| Run locally | `mise run local` |
| Build the image | `mise run build` |
| Run in Docker | `mise run docker` |

The app listens on port 8080. Set `PORT` to use another port locally. `mise run docker` publishes 8080. To use another port with Docker, run the container yourself with matching `-e PORT` and `-p` flags.

## Contributing

Commits follow [Conventional Commits](https://www.conventionalcommits.org/).
