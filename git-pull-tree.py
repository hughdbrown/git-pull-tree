#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "click",
# ]
# ///

from enum import Enum
from pathlib import Path

import click

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

class Action(Enum):
    GIT_PULL = 1
    GIT_LOG = 2


def pull_action(root: Path):
    print(f"(echo '{str(root)}' && cd '{str(root)}' && git pull && cd -)")


def log_action(root: Path):
    git_log = 'git --no-pager log -n 1 --date=iso --pretty=format:"%ad %h %an %ae | %s\n"'
    print(f"(echo '{str(root)}' && cd '{str(root)}' > /dev/null && {git_log} && cd - > /dev/null )")


do_action = {
    Action.GIT_PULL: pull_action,
    Action.GIT_LOG: log_action,
}

def arg_main(action: Action, root: Path, traverse_len: int):
    # print(f"# {'-' * 20} {traverse_len} {str(root)}")
    paths = [p for p in root.glob('*') if p.is_dir()]
    if not paths:
        return

    pathnames = {p.name for p in paths}
    if ".git" in pathnames:
         # Current directory is a git repo
         print(f"# {'-' * 20} {traverse_len} {str(root)}")
         do_action[action](root)
         return

    traverse_len += 1
    for p in sorted(paths):
        if p.stem not in skippable:
            arg_main(action, p, traverse_len)


@click.command()
@click.option(
    '-a', '--action',
    required=False,
    type=click.Choice(Action), default=Action.GIT_PULL
)
def main(
    action,
) -> None:
    arg_main(action, Path().cwd(), 0)


if __name__ == '__main__':
    main()
