# Freo

A Flask app that serves a Hello World page over HTTP.

Freo is a Hello World example: one HTML page, one route, runnable on the host, in Docker, or as a Deployment on local minikube.

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
| Build the image in minikube | `mise run k8s-build` |
| Apply namespace, Deployment and Service | `mise run k8s-apply` |
| Forward port 8080 to the Service | `mise run k8s-forward` |
| Delete the minikube namespace | `mise run k8s-delete` |

The app listens on port 8080. Set `PORT` to use another port locally. `mise run docker` publishes 8080. To use another port with Docker, run the container yourself with matching `-e PORT` and `-p` flags. The image is tagged `freo:local`.

## minikube

You need a running minikube cluster and `kubectl` pointed at it (`kubectl get nodes` must succeed). Start the cluster yourself if it is not up.

```bash
mise run k8s-build
mise run k8s-apply
mise run k8s-forward
```

Open [http://localhost:8080/](http://localhost:8080/). Leave the port-forward running while you use the page.

The Deployment runs two replicas. Inspect with:

```bash
kubectl get deploy,rs,po,svc -n freo
kubectl logs -n freo -l app=freo
```

When you are finished:

```bash
mise run k8s-delete
```

`k8s/ingress.yaml` is not part of the happy path. On macOS with the minikube docker driver, Ingress needs the ingress addon, `minikube tunnel` (leave that terminal open; it may ask for your password), and an `/etc/hosts` entry mapping `freo.test` to `127.0.0.1` — not the address from `minikube ip`. Then apply the Ingress and open [http://freo.test/](http://freo.test/).

```bash
minikube addons enable ingress
minikube tunnel
kubectl apply -f k8s/ingress.yaml
```

## Contributing

Commits follow [Conventional Commits](https://www.conventionalcommits.org/).
