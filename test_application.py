from pathlib import Path

import yaml

APPLICATION = Path(__file__).parent / "argocd" / "application.yaml"


def _application() -> dict:
    return yaml.safe_load(APPLICATION.read_text())


def test_application_tracks_main_and_the_freo_chart():
    spec = _application()["spec"]

    assert spec["source"]["repoURL"] == "git@github.com:johnsyweb/freo.git"
    assert spec["source"]["targetRevision"] == "main"
    assert spec["source"]["path"] == "charts/freo"


def test_application_lives_in_argocd_and_creates_the_freo_namespace():
    application = _application()
    spec = application["spec"]

    assert application["metadata"]["name"] == "freo"
    assert application["metadata"]["namespace"] == "argocd"
    assert spec["destination"]["server"] == "https://kubernetes.default.svc"
    assert spec["destination"]["namespace"] == "freo"
    assert "CreateNamespace=true" in spec["syncPolicy"]["syncOptions"]


def test_application_does_not_auto_sync():
    spec = _application()["spec"]

    assert "automated" not in spec.get("syncPolicy", {})
