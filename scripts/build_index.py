"""Build a static PEP 503 package index from wheel files.

Usage: build_index.py <wheels-dir> <site-dir>

Writes <site-dir>/files/<wheel> and <site-dir>/simple/<project>/index.html,
each link carrying #sha256=<digest> so installers can check the download.
"""
import hashlib
import html
import re
import shutil
import sys
from pathlib import Path


def normalize(name: str) -> str:
    # PEP 503 project name normalisation.
    return re.sub(r"[-_.]+", "-", name).lower()


def main() -> None:
    wheels_dir, site_dir = Path(sys.argv[1]), Path(sys.argv[2])
    files_dir = site_dir / "files"
    simple_dir = site_dir / "simple"
    files_dir.mkdir(parents=True, exist_ok=True)
    simple_dir.mkdir(parents=True, exist_ok=True)

    projects: dict[str, list[tuple[str, str]]] = {}
    for wheel in sorted(wheels_dir.glob("*.whl")):
        digest = hashlib.sha256(wheel.read_bytes()).hexdigest()
        shutil.copy2(wheel, files_dir / wheel.name)
        project = normalize(wheel.name.split("-", 1)[0])
        projects.setdefault(project, []).append((wheel.name, digest))

    if not projects:
        sys.exit("no wheels found")

    for project, files in projects.items():
        page = simple_dir / project / "index.html"
        page.parent.mkdir(exist_ok=True)
        links = "\n".join(
            f'<a href="../../files/{html.escape(name.replace("+", "%2B"))}'
            f'#sha256={digest}">{html.escape(name)}</a><br>'
            for name, digest in files
        )
        page.write_text(
            "<!DOCTYPE html>\n<html><head><meta name=\"pypi:repository-version\" "
            f"content=\"1.0\"><title>Links for {project}</title></head>\n"
            f"<body><h1>Links for {project}</h1>\n{links}\n</body></html>\n"
        )

    root = "\n".join(
        f'<a href="{p}/">{p}</a><br>' for p in sorted(projects)
    )
    (simple_dir / "index.html").write_text(
        "<!DOCTYPE html>\n<html><head><meta name=\"pypi:repository-version\" "
        "content=\"1.0\"><title>Simple index</title></head>\n"
        f"<body>\n{root}\n</body></html>\n"
    )
    print(f"{sum(len(f) for f in projects.values())} wheels, "
          f"{len(projects)} projects")


if __name__ == "__main__":
    main()
