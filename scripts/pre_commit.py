# pylint: skip-file
# type: ignore
# fmt: off
# flake8: noqa

"""
Execute this script to run all code-checks.
Might be added as RUN service in PyCharm or tasks.json in VSCode

- Check that required dev-tools are installed in the running environment
- Run them one by one with output to STDOUT
"""

if __name__ == "__main__":

    import importlib.util
    import subprocess
    import sys
    from pathlib import Path

    # Try to import colorama dev package for colored terminal output.
    try:
        from colorama import Fore, init

        init(autoreset=True)

        # Colors
        color_heading = Fore.LIGHTYELLOW_EX
        color_ok = Fore.LIGHTGREEN_EX
        color_finished = Fore.LIGHTMAGENTA_EX

    except ModuleNotFoundError:
        # No colors
        color_heading = ""
        color_ok = ""
        color_finished = ""

    # Exceptions
    class MissingDevTool(Exception):
        """Missing DevTool"""

    # Project root
    app_root_directory = Path(__file__).parent.parent.absolute()

    # Check DevTools
    dev_tools = ["isort", "black", "mypy", "flake8"]

    print(f"\n{color_heading}>> Checking dev tools in venv:")
    for tool in dev_tools:
        spam_spec = importlib.util.find_spec(tool)  # type: ignore
        if spam_spec is None:
            raise MissingDevTool(tool)
        else:
            print(f'{color_ok}OK - {spam_spec.name}')

    # iSort
    print(f"\n{color_heading}>> Running iSort:")
    subprocess.run(["poetry", "--quiet", "run", "isort", "poetry_plugin_pycopy", "--show-files"], stdout=sys.stdout, stderr=subprocess.STDOUT, cwd=app_root_directory)
    subprocess.run(["poetry", "--quiet", "run", "isort", "poetry_plugin_pycopy"], stdout=sys.stdout, stderr=subprocess.STDOUT, cwd=app_root_directory)
    print(f"{color_heading}>> iSort done")

    # Black
    print(f"\n{color_heading}>> Running Black:")
    subprocess.run(["poetry", "--quiet", "run", "black", "poetry_plugin_pycopy"], stdout=sys.stdout, stderr=subprocess.STDOUT, cwd=app_root_directory)
    print(f"{color_heading}>> Black done")

    # Mypy
    print(f"\n{color_heading}>> Running Mypy:")
    subprocess.run(["poetry", "--quiet", "run", "mypy", "poetry_plugin_pycopy"], stdout=sys.stdout, stderr=subprocess.STDOUT, cwd=app_root_directory)
    print(f"{color_heading}>> Mypy done")

    # Flake8
    print(f"\n{color_heading}>> Running Flake8:")
    subprocess.run(["poetry", "--quiet", "run", "flake8", "poetry_plugin_pycopy"], stdout=sys.stdout, stderr=subprocess.STDOUT, cwd=app_root_directory)
    print(f"{color_heading}>> Flake8 done")

    # Pylint
    # print(f"\n{color_heading}>> Running Pylint:")
    # subprocess.run(["poetry", "run", "pylint", "src"], stdout=sys.stdout, stderr=subprocess.STDOUT, cwd=app_root_directory)
    # print(f"{color_heading}>> Pylint done")

    # DONE
    print(f'\n{color_finished}PRE-COMMIT FINISHED\n')
