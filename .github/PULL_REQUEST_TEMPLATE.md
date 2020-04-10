Please make sure that you:

- [ ] Have read [Contributing.md](../CONTRIBUTING.md)
- [ ] Include a link to the issue this pull request is associated to.
- [ ] Have ran the linter at the root level of the project: `black .`
- [ ] Have ran the tests and made sure they are all passing: `python -m pytest --verbose --cov=./` 

For new modules, also make sure that you:

- [ ] Have exported the new module function in `turf/<your-module>/__init__.py` and `turf/__init__.py`.
- [ ] have added the new module under the `Available Modules` section.
