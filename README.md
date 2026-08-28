# Freo

A Flask app that serves a Hello World page over HTTP.

Freo is a Hello World example: one HTML page, one route, runnable on the host, in Docker, or as a Helm chart synced by Argo CD onto local minikube.

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

Python 3.14 is pinned in `mise.toml`. Docker is required only for image tasks. Helm is pinned for chart tests and linting.

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
| Install Argo CD | `mise run k8s-argocd` |
| Apply the Argo CD Application | `mise run k8s-application` |
| Forward port 8081 to the Argo CD UI | `mise run k8s-ui` |
| Forward port 8080 to the Freo Service | `mise run k8s-forward` |
| Delete the Application and namespace | `mise run k8s-delete` |

The app listens on port 8080. Set `PORT` to use another port locally. `mise run docker` publishes 8080. To use another port with Docker, run the container yourself with matching `-e PORT` and `-p` flags. The local Docker tag remains `freo:local`. Images for minikube are `ghcr.io/johnsyweb/freo:<appVersion>`, published by GitHub Actions.

## minikube and Argo CD

You need a running minikube cluster and `kubectl` pointed at it (`kubectl get nodes` must succeed). Start the cluster yourself if it is not up. This GitHub repository is public, so Argo CD clones it over HTTPS with no credentials. Images on `ghcr.io/johnsyweb/freo` are public because they are published from this public repository.

Do not `kubectl apply` the chart's resources. Argo CD owns the live objects.

If you previously created a deploy-key Secret (`repo-freo`) or a GitHub deploy key, delete them. They are no longer used.

### 1. Install Argo CD

```bash
mise run k8s-argocd
kubectl wait --for=condition=Ready pods --all -n argocd --timeout=300s
```

This applies the [official stable install manifest](https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml).

```bash
mise run k8s-ui
```

Open [https://localhost:8081/](https://localhost:8081/) (the certificate is self-signed). Sign in as `admin`. The initial password is:

```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
echo
```

Leave the UI port-forward running in its own terminal.

### 2. Publish the image

GitHub Actions builds `linux/amd64` and `linux/arm64` and pushes `ghcr.io/johnsyweb/freo:<version>` when you push a git tag `v<version>` that matches Chart `version`, `appVersion`, and `image.tag`. Pull requests and pushes to `main` run tests only.

### 3. Apply the Application and sync

`argocd/application.yaml` must already be on `main` (push this repository if it is not). Then:

```bash
mise run k8s-application
```

In the Argo CD UI, open the `freo` Application and **Sync** it by hand. Auto-sync is off until you choose to turn it on.

```bash
mise run k8s-forward
```

Open [http://localhost:8080/](http://localhost:8080/). Leave the Freo port-forward running while you use the page.

Inspect with:

```bash
kubectl get deploy,rs,po,svc -n freo
kubectl logs -n freo -l app=freo
```

When you are finished:

```bash
mise run k8s-delete
```

Delete the Application **before** you expect the namespace to stay gone. Once you enable auto-sync and self-heal, Argo CD will recreate anything you delete in `freo` until the Application itself is removed.

### Version bumps

One version string: Chart `version`, Chart `appVersion`, `values.yaml` `image.tag`, git tag `v<version>`, and the GHCR tag. Start at `0.1.0`. Current is `0.1.1`.

1. Set all three files to the new version (for example `0.1.1`).
2. Commit, tag `v0.1.1`, and push `main` plus the tag.
3. Wait for the **CI** workflow on that tag to push the image.
4. Sync the Application in the Argo CD UI.

### Optional Ingress

Ingress is off by default. On macOS with the minikube docker driver it needs the ingress addon, `minikube tunnel` (leave that terminal open; it may ask for your password), and an `/etc/hosts` entry mapping `freo.test` to `127.0.0.1` — not the address from `minikube ip`. Set `ingress.enabled: true` in `charts/freo/values.yaml`, commit, push, and sync. Then open [http://freo.test/](http://freo.test/).

```bash
minikube addons enable ingress
minikube tunnel
```

## Contributing

Commits follow [Conventional Commits](https://www.conventionalcommits.org/).
