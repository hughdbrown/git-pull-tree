#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "click",
# ]
# ///

from pathlib import Path

skippable = {
    '.pytest_cache',
    '__pycache__',
    'env',
    'venv',
    '.cache',
    'node_modules',
    '.fingerprint',
    'target',
}

def main(root: Path, traverse_len: int) -> None:
    # print(f"# {'-' * 20} {traverse_len} {str(root)}")
    paths = [p for p in root.glob('*') if p.is_dir()]
    if not paths:
        return

    pathnames = {p.name for p in paths}
    if ".git" in pathnames:
         # Current directory is a git repo
         print(f"# {'-' * 20} {traverse_len} {str(root)}")
         print(f"(cd '{str(root)}' && git pull && cd -)")
         return

    traverse_len += 1
    for p in paths:
        if p.stem not in skippable:
            main(p, traverse_len)


if __name__ == '__main__':
    main(Path().cwd(), 0)
