import os
import pathlib
import typing as tp


def repo_find(workdir: tp.Union[str, pathlib.Path] = ".") -> pathlib.Path:
    # PUT YOUR CODE HERE
    ...


def repo_create(workdir: tp.Union[str, pathlib.Path]) -> pathlib.Path:
    git_dir = os.environ.get("GIT_DIR", ".git")
    os.system(f"cd {workdir}")
    os.system(f"mkdir {git_dir}")
    os.system(f"mkdir -p {git_dir}/refs/heads")
    os.system(f"mkdir -p {git_dir}/refs/tags")
    os.system(f"mkdir -p {git_dir}/objects")
    os.system(f'echo "ref: refs/heads/master\n" > {git_dir}/HEAD')
    os.system(f'echo "[core]\n\trepositoryformatversion = 0\n\tfilemode = true\n\tbare = false\n\tlogallrefupdates = false\n" >> .git/config')
    os.system(f'echo "Unnamed pyvcs repository" >> {git_dir}/description')
    return pathlib.Path(git_dir)
