from pathlib import Path

import pytest

import release_version


def _write_chart(chart_dir: Path, version: str, app_version: str, image_tag: str) -> None:
    chart_dir.mkdir(parents=True, exist_ok=True)
    (chart_dir / "Chart.yaml").write_text(
        f'version: "{version}"\nappVersion: "{app_version}"\n'
    )
    (chart_dir / "values.yaml").write_text(
        f'image:\n  tag: "{image_tag}"\n'
    )


def test_image_tag_for_git_tag_returns_the_shared_version(tmp_path):
    _write_chart(tmp_path, "0.2.0", "0.2.0", "0.2.0")

    assert release_version.image_tag_for_git_tag("v0.2.0", tmp_path) == "0.2.0"


def test_image_tag_for_git_tag_rejects_a_tag_that_does_not_match_the_chart(
    tmp_path,
):
    _write_chart(tmp_path, "0.1.0", "0.1.0", "0.1.0")

    with pytest.raises(release_version.VersionMismatch, match="v0.2.0"):
        release_version.image_tag_for_git_tag("v0.2.0", tmp_path)


def test_image_tag_for_git_tag_rejects_a_chart_that_is_not_one_version(
    tmp_path,
):
    _write_chart(tmp_path, "0.1.0", "0.1.0", "0.1.1")

    with pytest.raises(release_version.VersionMismatch, match="0.1.1"):
        release_version.image_tag_for_git_tag("v0.1.0", tmp_path)


def test_image_tag_from_git_tag_requires_a_v_prefix():
    with pytest.raises(release_version.VersionMismatch, match="v"):
        release_version.image_tag_from_git_tag("0.1.0")
