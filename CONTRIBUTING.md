# How To Contribute

As the library follows a modular structure, it is fairly easy to contribute by working on a subpackage and
submit a pull request of those atomic changes.

For this, first you should check this repo's issues and check which modules are being worked on by filtering by the
`in-progress` label. Then, you can check [turf.js](https://github.com/Turfjs/turf) github repo, choose a module
that you'd like to implement, making sure that it hasn't been already implemented or is currently being worked by
someone else.

When you're ready, open a new issue on this repo outlining the module you'll be working on,
so that subsequent contributors can follow the same logic outlined here.

Please attend to the following guidelines:

- Open an issue in `diogomatoschaves/pyturf` outlining your plan.
- Always include tests. [pytest](https://docs.pytest.org/en/latest/) is used in this project.
- `pyturf` modules are small, containing a single exported function. See below for a typical module structure.
- Export your module function by including it in `turf/<your-module>/__init__.py` and `turf/__init__.py`. See below for details.
- GeoJSON is the _lingua franca_ of `pyturf`. It should be used as the data structure for anything that can be represented as geography.
- Keep your commits atomic and each of them passing all checks (linter and tests).
- Add your new module under the `Available Modules` section.
- Add your new module under its appropriate section in [docs/source/modules](docs/source/modules).
- Avoid extra dependencies if you can.
- Run the linter before submitting changes (see below for more details).
- Run `python -m pytest --verbose --cov=./` from the project root folder to run all the tests and make
sure they pass with a sufficiently high coverage.
- Rebase your branch with the upstream master before opening the PR: `git rebase upstream/master`

After you open the PR, make sure that the CI pipeline passes all checks (on the `Checks` tab of the PR).

## Code Style

To ensure consistent code style, [black](https://black.readthedocs.io/en/stable/) is used in this project. At the root level run:

```
$ black .
```

This will automatically reformat all files according to `black`'s specification.

## Structure of a `pyturf` module

For a new module named `new_module`, the following structure should be adhered to.

```
turf
|
├── ...
├── __init__.py
├── new_module
    ├── __init__.py
    ├── _new_module.py
    |
    ├── tests
        ├── test_new_module.py
        ├── in
        │   ├── points.geojson
        |   ├── ...
        │
        ├── out
            ├── points.geojson
            ├── ...
```

## Importing modules in `__init__.py` files

In order for the module function to be imported directly from `turf`, we need to import them on the `__init__.py` files
on both the module and at the root level. So for example, for a new module named `new_module`,
on `turf/new_module/__init__.py` we would include:

```python
from turf.new_module._new_module import new_module
```

The same logic can be applied to `turf/__init__.py`:

```python
...
from turf.new_module import new_module
...
```

## Adding Tests

Tests setup in this project follows a certain pattern that, even if not being a _one size fits all_, if followed should
ensure a good test flow in most cases.

The pattern consists of importing the tests input and output through files in `turf/new_module/tests/in`
and `turf/new_module/tests/out` respectively, and then parameterizing these fixtures to be used in individual tests as required.

These guidelines should be followed:

- The file where tests are executed should be under the directory `tests`.
- The directory `tests` should have sub directories `in` and `out`, where input and output files should be kept respectively.
- Files in both `in` and `out` for a specific test must have the same name, although they can have
different file extensions (eg: `.json` or `.geojson`).

Fixtures and expected outputs can then be imported by means of the function `get_fixtures` defined in
`turf/utils/test_setup.py`, by providing the test file path as input:

```python
import os
from turf.utils.test_setup import get_fixtures

current_path = os.path.dirname(os.path.realpath(__file__))

fixtures = get_fixtures(current_path)
```

The returned value `fixtures` becomes a dictionary of fixtures, with the file names in `in` and `out` as keys,
and in turn each fixture is a dictionary containing keys `"in"` and `"out"`, representing the input and
output of the tests respectively.

If for some reason you only have either `in` or `out` fixtures, then in order to avoid errors running the tests
you should pass the argument `keys` to `get_fixtures` as shown below:

```python
import os
from turf.utils.test_setup import get_fixtures

current_path = os.path.dirname(os.path.realpath(__file__))

fixtures = get_fixtures(current_path, keys=["in"]) # Only retrieve input fixtures
```

These fixtures can then be parameterized as individual tests, allowing for only one test definition to be used
in multiple test cases. This would follow a structure of the kind:

```python
import pytest
from turf.new_module import new_module # Don't import your function directly from turf

@pytest.mark.parametrize(
    "fixture",
    [
        pytest.param(fixture, id=fixture_name)
        for fixture_name, fixture in fixtures.items()
    ],
)
def test_new_module(self, fixture):

    # This is an example function call
    assert new_module(fixture["in"]) == fixture["out"]
```

In order to run the tests, from the root directory run:

```
$ python -m pytest --verbose --cov=./
```

## Updating The Documentation

In case you add a new module, please update also the documentation. The structure
for the documentation follows the `turf` structure. You can check [turf.js documentation](https://turfjs.org/).
According to the `turf.js documentation`, you can pick the same `block` name and update it with your addition.

```
turf
|
├── ...
├── __init__.py
├── docs
    ├── ...
    ├── conf.py
    |
    ├── modules
        ├── aggregation.rst
        ├── assertion.rst
        ├── booleans.rst
        ├── ...
```

As an example, for adding the `length module` you would have to add the following lines to  `measurements.rst`. 

```
Length
------

.. autofunction:: turf.length
```
