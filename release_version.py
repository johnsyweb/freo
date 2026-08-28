import argparse
import sys
from pathlib import Path

import yaml

DEFAULT_CHART_DIR = Path("charts/freo")


class VersionMismatch(ValueError):
    pass


def image_tag_from_git_tag(git_tag: str) -> str:
    if not git_tag.startswith("v") or git_tag == "v":
        raise VersionMismatch(f"git tag {git_tag!r} must look like v1.2.3")
    return git_tag.removeprefix("v")


def versions_from_chart(chart_dir: Path) -> tuple[str, str, str]:
    chart = yaml.safe_load((chart_dir / "Chart.yaml").read_text())
    values = yaml.safe_load((chart_dir / "values.yaml").read_text())
    return str(chart["version"]), str(chart["appVersion"]), str(values["image"]["tag"])


def image_tag_for_git_tag(git_tag: str, chart_dir: Path) -> str:
    image_tag = image_tag_from_git_tag(git_tag)
    version, app_version, values_tag = versions_from_chart(chart_dir)
    if image_tag == version == app_version == values_tag:
        return image_tag
    raise VersionMismatch(
        f"git tag {git_tag!r} must match Chart version {version!r}, "
        f"appVersion {app_version!r}, and image.tag {values_tag!r}"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Print the image tag when the git tag matches the chart version."
    )
    parser.add_argument("--git-tag", required=True)
    parser.add_argument("--chart-dir", type=Path, default=DEFAULT_CHART_DIR)
    args = parser.parse_args(argv)
    try:
        print(image_tag_for_git_tag(args.git_tag, args.chart_dir))
    except VersionMismatch as error:
        print(error, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
