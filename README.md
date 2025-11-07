# HOPE Control Manager


[![Test](https://github.com/unicef/hope-control-manager/actions/workflows/test.yml/badge.svg)](https://github.com/unicef/hope-control-manager/actions/workflows/test.yml)
[![Lint](https://github.com/unicef/hope-control-manager/actions/workflows/lint.yml/badge.svg)](https://github.com/unicef/hope-control-manager/actions/workflows/lint.yml)
[![codecov](https://codecov.io/github/unicef/hope-control-manager/graph/badge.svg?token=FBUB7HML5S)](https://codecov.io/github/unicef/hope-control-manager)
[![Documentation](https://github.com/unicef/hope-control-manager/actions/workflows/docs.yml/badge.svg)](https://unicef.github.io/hope-control-manager/)
[![Pypi](https://badge.fury.io/py/unicef-hope-control-manager.svg)](https://badge.fury.io/py/unicef-hope-control-manager)
[![Docker Pulls](https://img.shields.io/docker/pulls/unicef/hope-control-manager)](https://hub.docker.com/repository/docker/unicef/hope-control-manager/tags)


## Translations

You can contribute to the Portal translation at https://app.transifex.com///dashboard/


## Contributing

### Requirements

- [uv](https://docs.astral.sh/uv/)
- [direnv](https://direnv.net/)

### Checkout and configure development environment

```shell

    git checkout https://github.com/unicef/hope-control-manager.git
    cd hope-control-manager
    uv venv .venv
    uv sync

    ./manage.py env --develop > .envrc  # create initial development configuration
    direnv allow .  # enable enviroment
    createdb hope_control_manager  # create postgres database on localhost

```
