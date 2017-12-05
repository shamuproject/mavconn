# Contributing

When contributing to this repository, please first discuss the change you wish
to make via issue, email, or any other method with the owners of this repository
before making a change. 


## Pull Request Process

1. Create a pull request early in development processes with a checkbox list of
   features/changes you plan to make along with a description of what you intend
   to do.  Prepend (WIP:) for "work in progress" to the title of this pull request
   until you are ready for review and merging.
2. Update README.rst and the Sphinx documentation with detains of any changes to
   the interface, this includes new environment variables, exposed ports, and
   useful file locations.
3. Ensure test coverage did not drop below 90% and that all unit tests pass.
4. Ensure the package builds, installs, and runs using `pip install .` in
   a clean `virtualenv`.  List any new external dependencies in the README.rst
   file.
5. Increase the version numbers in any examples files and the README.rst to the
   new version that this Pull Request would represent. The versioning scheme we
   use is [SemVer](http://semver.org/).
5. You may merge the Pull Request in once you have the sign-off of a core
   developer, or if you do not have permission to do that, you may request the
   reviewer merge it for you.


## Git Etiquette

* Do not work on the main repository unless you are merging in changes, 
  preparing for a version bump, or other repository management.
  * Create a fork, make a new branch and work on your changes there.  Merge
    these changes in using the _Pull Request Process_ above.
* Do not commit IDE/Editor specific files or any generated files.  You should
  add these files to the `.gitignore` file to ensure you do not accidentally
  commit them.
* Do not commit application specific configuration files.  If you wish to submit
  an example place it in the examples directory.
* Do not commit assets such as pictures or videos.  The exception is small
  (under 300 kB) images used in the documentation.
* Do not commit other project's documentation such as PDF files.
  * Link to that projects documentation instead.
* Do not commit another project's source code.
  * Use a [Git submodule](https://git-scm.com/docs/git-submodule) instead.


## Programming Style

* All Python code must follow the
  [PEP8](https://www.python.org/dev/peps/pep-0008/) style guide.  It is highly
  recommended to use tools such as `pylint`, `pycodestyle`, and `pydocstyle` to
  help you maintain proper Python style.
* Classes should be `CamelCased`.
* Functions and variables should be `underscore_case`.
* All public functions and classes should contain [Sphinx style
  docstrings](https://pythonhosted.org/an_example_pypi_project/sphinx.html) and
  have an `autodoc` entry in the Sphinx documentation.


