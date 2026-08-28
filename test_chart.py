import subprocess
from pathlib import Path

import yaml

CHART = Path(__file__).parent / "charts" / "freo"


def _helm(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["helm", *args],
        capture_output=True,
        text=True,
        check=False,
    )


def _template(*extra: str) -> list[dict]:
    result = _helm("template", "freo", str(CHART), *extra)
    assert result.returncode == 0, result.stderr or result.stdout
    return [doc for doc in yaml.safe_load_all(result.stdout) if doc]


def _docs_of_kind(documents: list[dict], kind: str) -> list[dict]:
    return [doc for doc in documents if doc.get("kind") == kind]


def test_chart_lints():
    result = _helm("lint", str(CHART))

    assert result.returncode == 0, result.stdout + result.stderr


def test_chart_version_app_version_and_image_tag_match():
    chart = yaml.safe_load((CHART / "Chart.yaml").read_text())
    values = yaml.safe_load((CHART / "values.yaml").read_text())

    assert chart["version"] == chart["appVersion"] == values["image"]["tag"]


def test_default_render_deploys_two_replicas_of_the_ghcr_image():
    documents = _template()
    deployments = _docs_of_kind(documents, "Deployment")

    assert len(deployments) == 1
    container = deployments[0]["spec"]["template"]["spec"]["containers"][0]
    assert deployments[0]["spec"]["replicas"] == 2
    assert container["image"] == "ghcr.io/johnsyweb/freo:0.1.1"
    assert container["imagePullPolicy"] == "IfNotPresent"


def test_default_render_exposes_a_cluster_ip_service_on_port_8080():
    documents = _template()
    services = _docs_of_kind(documents, "Service")

    assert len(services) == 1
    assert services[0]["spec"]["type"] == "ClusterIP"
    assert services[0]["spec"]["ports"][0]["port"] == 8080


def test_default_render_does_not_include_an_ingress():
    documents = _template()

    assert _docs_of_kind(documents, "Ingress") == []


def test_ingress_can_be_enabled_for_freo_test():
    documents = _template("--set", "ingress.enabled=true")
    ingresses = _docs_of_kind(documents, "Ingress")

    assert len(ingresses) == 1
    assert ingresses[0]["spec"]["ingressClassName"] == "nginx"
    assert ingresses[0]["spec"]["rules"][0]["host"] == "freo.test"
