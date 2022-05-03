# Malawi Commons

Library of various things to do with Malawi that one may run into when
programming.

TODO: Provide a better description!!!

## Installation

If using pip do:

```sh
pip install git+https://github.com/GeekQuest/mw-commons-py.git
```

If using [poetry](https://python-poetry.org), add the following
under `[tool.poetry.dependencies]` in pyproject.toml:

```toml
mw_commons = { git = "https://github.com/GeekQuest/mw-commons-py.git" }
```

Then run:

```sh
poetry install
```

## USAGE

The following is a basic overview of what you can do with the library. For more
details please browse the documentation [here](##).

```python
>>> from mw_commons import phone_numbers
>>> phone_numbers.is_valid_phone_number('0888800900')
True
>>> phone_number = phone_numbers.PhoneNumber('0888800900')
>>> phone_number.to_internationalized(humanize=True)
'+265-88-880-0900'
```

## Development

- Fork this repository
- Install [poetry](https://python-poetry.org)
- Setup dependencies:

    ```bash
    poetry install
    ```

- Make changes
- Run tests

    ```bash
    poetry run python -m unittest discover tests/
    ```

- Commit and push then make a pull request