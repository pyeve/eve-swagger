Changelog
=========

Here you can see the full list of changes between each Eve-Swagger release.

In Development
--------------

- Query parameters: where; sort; page; max_results (`#86`_)
- Basic and Token authorization support (`#86`_)
- Allow use of SWAGGER_HOST https server (`#86`_)
- Add support for API_VERSION and URL_PREFIX (`#86`_)
- GET response now correctly returns ``_items`` as an array (`#86`_)
- Adopt Black code formatting style (`#82`_)
- Add Python 3.6 and 3.7 to CI matrix (`#81`_)
- Drop Python 2.6, 3.3, and 3.4 support (`#80`_)
- Support for OpenAPI 3 (`#70`_, `#79`_)
- Add support for resource-level ``example`` definition (`#69`_)
- Add a stale-bot to automatically close stale issues and pull requests (`#68`_)

.. _`#86`: https://github.com/pyeve/eve-swagger/pull/86
.. _`#82`: https://github.com/pyeve/eve-swagger/issues/82
.. _`#81`: https://github.com/pyeve/eve-swagger/issues/81
.. _`#80`: https://github.com/pyeve/eve-swagger/issues/80
.. _`#79`: https://github.com/pyeve/eve-swagger/pull/79
.. _`#70`: https://github.com/pyeve/eve-swagger/pull/70
.. _`#69`: https://github.com/pyeve/eve-swagger/issues/69
.. _`#68`: https://github.com/pyeve/eve-swagger/pull/68

Released
--------

Version 0.0.11
~~~~~~~~~~~~~~

Released on June 19, 2018.

- Remove regexes from urls and resource titles (`#66`_)
- Changelog is now in .rst format (`#65`_)
- Add support for `nullable` property (`#61`_)
- Fix: tests fail on flask_pymongo import (`#63`_)

.. _`#66`: https://github.com/pyeve/eve-swagger/issues/66
.. _`#65`: https://github.com/pyeve/eve-swagger/issues/65
.. _`#63`: https://github.com/pyeve/eve-swagger/issues/63
.. _`#61`: https://github.com/pyeve/eve-swagger/pull/61

Version 0.0.10
~~~~~~~~~~~~~~

Released on April 10, 2018.

- New: Add support for adding schema examples. Closes #59 (Nils Verheyen).

Version 0.0.9
~~~~~~~~~~~~~

Released on 6 March, 2018

- Fix: Override schemes in SWAGGER_INFO does not work (Cuong Manh Le).

Version 0.0.8
~~~~~~~~~~~~~

Released on 2 October, 2017

- Fix: `If-Match` header required when concurrency control is disabled. Closes
  #49 (Aleksi Pekkala).
- Fix: If the user provides a 'schemes' configuration value use that instead of
  auto-discovering the value. This is useful in the scenario where Eve is
  running on http behind a proxy running https, so auto-discovery would yield
  the wrong value (Jim Kennedy).
- New: add support for geometric data types `point`, `linestring`,
  `multilinestring', `polygon` and `multipolygon`. Closes #44 (Damien Aboss).

Version 0.0.7
~~~~~~~~~~~~~

Released on 13 March, 2017

- Fix: All responses claim to return a status code of 200 (Alexander
  Dietmüller).
- Fix: tests failure since jsonschema dropped Python 2.6. Closes #40.

Version 0.0.6
~~~~~~~~~~~~~

Released on 3 January, 2017

- New: support for swagger 2.0/openAPI 'readOnly' and 'pattern' rules
  (hermannsblum).
- Fix: crash if no docstring is available for hook (hermannsblum).
- Fix: support for data_relation nested in lists (Patrick Decat).
- Fix: handle missing fields and settings. Closes #31 (otibsa).

Version 0.0.5
~~~~~~~~~~~~~

Released on 25 October, 2016

- Fix: float type are not p:Groperly defined. Closes #13.
- Fix: README: fix comma that causes a validation error in example script (Luis
  Fernando Gomes).

- New: Ability to generate Swagger tags (Stratos Gerakakis).
- New: add CORS support (otibsa).
- New: Python 2.6 compatibility (otibsa).
- New: Add a proper test suite. Closes #8 (otibsa).
- New: Move the path parameters (`/people/{personId}`) to their own section of
  the swagger doc. That cleans up the parameters entries in the paths sections
  by referencing the parameters (otibsa).
- New: Option to enable event hooks description to swagger documentation
  (otibsa).
- New: Support for data relations (otibsa).
- New: Option to disable resource documentation via `disable_documentation` in
  `settings.py` (otibsa).
- New: Ability to include description fields. Just add a `description` field in
  the schema definitions in `settings.py` (Stratos Gerakakis).
- New: Add support for more eve features: `allowed`, `default`, `minlength`,
  `maxlength`, `min`, `max` (otibsa).
- New: Enable additional documentation to be injected at runtime (otibsa).
- New: Add tox and build server configuration (Peter Bittner). Addresses #8.
- New: Support for endpoint fields (swagger parameters). WIP. Closes #5.

Version 0.0.4
~~~~~~~~~~~~~

Released on 12 June, 2016

- New: Python 3 compatibility. Closes #6 (Naoko Reeves).

Version 0.0.3
~~~~~~~~~~~~~

Released on 7 June, 2016

- Fix: Crash on pip install. Closes #4.

Version 0.0.2
~~~~~~~~~~~~~

Released on 6 June, 2016

- Fix: AttributeError: 'module' object has no attribute 'name' when trying to
  register the Blueprint. Closes #3.

Version 0.0.1
~~~~~~~~~~~~~

Released on 4 June, 2016
