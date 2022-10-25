# poetry-plugin-pycopy

<!--- These are examples. See https://shields.io for others or to customize this set of shields. You might want to include dependencies, project status and licence info here --->
![GitHub repo size](https://img.shields.io/github/repo-size/danielfajt/poetry-plugin-pycopy)
![GitHub contributors](https://img.shields.io/github/contributors/danielfajt/poetry-plugin-pycopy)
![GitHub stars](https://img.shields.io/github/stars/danielfajt/poetry-plugin-pycopy?style=social)
![GitHub forks](https://img.shields.io/github/forks/danielfajt/poetry-plugin-pycopy?style=social)
![Twitter Follow](https://img.shields.io/twitter/follow/danielfajt?style=social)

This plugin adds command `pycopy` to Poetry which will copy information from `pyproject.toml` to `source` directory. 

The goal is to have `pyproject.toml` as a single source of truth for app version, name, description etc. and to have these values available during a program runtime.

## Use case
FastAPI app in which you want to show application name or version in API docs.


## Installation

From Pypi:
```
$ poetry self add poetry-plugin-pycopy
```

## Usage

```
$ poetry pycopy
```

## Plugin configuration in `pyproject.toml`

```
[tool.poetry-plugin-pycopy]
keys = ["name", "version", "description"]
dest_dir = "<some_package_name>"
dest_file = "__init__.py"
```
- `keys` list tells which fields should by copied from `[tool.poetry]`
- `dest_dir` is package/module root
- `dest_file` is the name of an output file

Plugin also runs with `$poetry version` command automatically. So when you use version bump, e.g.: `$poetry version patch` the plugin will copy the new version value into the output file.

## Output file example
The `dest_file` is set to `__init__.py`. Thus the plugin will create or replace that file with current values for a given `keys`. For example:

```
pyproject_toml = {
    "name": "test-venv-1",
    "version": "0.1.0",
    "description": "dsa",
}
```

-> https://unlicense.org/