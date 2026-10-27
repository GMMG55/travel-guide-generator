#!/usr/bin/env python3
"""Package only the runtime resources for uploading or installing the skill."""

import argparse
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


def package_skill(root, output):
    root = Path(root).resolve()
    output = Path(output).resolve()
    paths = [root / "SKILL.md", root / "examples" / "sample-guide.json"]
    for folder in ("scripts", "references", "assets"):
        for path in sorted((root / folder).rglob("*")):
            if path.is_file() and not path.is_symlink() and "__pycache__" not in path.parts:
                if path.suffix in {".py", ".md", ".json", ".html", ".css", ".js"}:
                    paths.append(path)
    if not paths[0].is_file():
        raise ValueError("SKILL.md is required")
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
