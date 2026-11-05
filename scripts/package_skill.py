#!/usr/bin/env python3
"""Package only the runtime resources for uploading or installing the skill."""

import argparse
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

RUNTIME_FILES = (
    "SKILL.md", "examples/sample-guide.json", "assets/template.html",
    "references/claude-setup.md", "references/daily-itinerary-spec.md",
    "references/design-spec.md", "references/guide-schema.json",
    "scripts/amap_route.py", "scripts/build_guide.py", "scripts/export_guide.py",
    "scripts/guide_utils.py", "scripts/package_skill.py", "scripts/render_guide.py", "scripts/route_estimator.py",
    "scripts/search_guide.py", "scripts/season_advisor.py", "scripts/validate_guide.py",
)

def package_skill(root, output):
    root = Path(root).resolve()
    output = Path(output).resolve()
    paths = [root / name for name in RUNTIME_FILES]
    for path in paths:
        if not path.is_file() or path.is_symlink() or root not in path.resolve().parents:
            raise ValueError("Missing or unsafe runtime file: {}".format(path))
    if output.exists():
        raise FileExistsError("Output already exists; choose another --output path")
    output.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(output, "x", compression=ZIP_DEFLATED) as archive:
        for path in paths:
            archive.write(path, "travel-guide-generator/" + path.relative_to(root).as_posix())
    return output, len(paths)


def main():
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=root / "dist" / "travel-guide-generator.zip")
    args = parser.parse_args()
    output, count = package_skill(root, args.output)
    print("Packaged {} files: {}".format(count, output))


if __name__ == "__main__":
    main()
