Please make sure that:

- [ ] You have read [CONTRIBUTING.md](../CONTRIBUTING.md)
- [ ] You Include a link to the issue this pull request is associated to.
- [ ] The linter has been run at the root level of the project: `black .`
- [ ] All tests are passing: `python -m pytest --verbose --cov=./` 
- [ ] Your branch is up to date with master: `git rebase upstream/master`

For new modules, also make sure that:

- [ ] The new module function is exported in `turf/<your-module>/__init__.py` and `turf/__init__.py`.
- [ ] The new module has been added under the `Available Modules` section on the [README](../README.md).
