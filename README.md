# bea-model-template

A [copier](https://copier.readthedocs.io/) template for a **model package** for
[building-energy-analysis](https://c-energie.github.io/bea-docs/) (BEA): a Python package that
contributes models BEA can fit to any cohort's households, or wraps a team's existing modelling
code as one.

```bash
uvx copier copy gh:c-energie/bea-model-template my-models
cd my-models
pip install -e ".[test]"
TEST_TIER=fast python -m unittest discover -v
```

A render with no edits installs and passes its tests. The agent skill `bea-model-package`, shipped
with BEA, drives this template:
`gh skill install c-energie/building-energy-analysis --scope project`.

## Questions

| Question | Default | |
|---|---|---|
| `package_name` | `toy-htc-models` | the distribution name; suggested `<name>-models` |
| `import_name` | derived from `package_name` | `import <it>` |
| `class_name` | `ToyHTC` | the model class; its snake_case form is the model's name (`ToyHTC` → `toy_htc`) and the package's entry point names its manifest |
| `description` | | one line |
| `author_name`, `author_email` | | |
| `licence` | `MIT` | `MIT`, `BSD-3-Clause`, `Apache-2.0` or `proprietary`: no LICENSE, and the `Private :: Do Not Upload` classifier so PyPI refuses it |

Unattended: `--defaults`, and `--data <question>=<answer>` for each answer you change. The model
contract the code is written against (`contract_version`) is the template's, never asked.

## What it renders

- `pyproject.toml` - `uv_build`, the `bea.plugins` entry point, `building-energy-analysis>=1.0,<2`,
  `requires-python = ">=3.11.4, <3.14"`, and a `test` extra (emcee).
- `src/<import_name>/my_existing_code.py` - the physics, a plain function with no BEA imports.
- `src/<import_name>/model.py` - `<class_name>(StaticModel)`: the toy
  `power = H * (temp_int - temp_ext) + c`, its parameters declared in code with units, bounds and
  priors, calling the physics. Wrap by subclassing: the user's code stays as it is.
- `src/<import_name>/__init__.py` - the manifest, and `register_provenance_package`.
- `tests/` - a `ModelContractTests` subclass, and the toy's `H` and `c` recovered from BEA's
  `TestDataset` by least squares and by emcee, wired through project-configuration's `load_tests`.
- `README.md` (quickstart, then "replace the toy"), `AGENTS.md` + `CLAUDE.md`, `.gitignore`,
  `.github/workflows/tests.yml` (self-contained, PyPI only), `LICENSE` unless proprietary,
  `.copier-answers.yml`.

Never: a CHANGELOG, a docs folder, `.python-version`, data, or committed test fixtures.

## Versions

Template tags follow BEA's **model contract major**: template `v1.x` renders contract 1.x code
(`contract_version` in `copier.yml`). A contract major bump is a BEA ADR, a BEA major and a template
major, and a generated package moves with `uvx copier update`. Bump the `contract_version` default
when BEA's `MODEL_CONTRACT_VERSION` moves a minor.

## CI

`.github/workflows/template.yml` renders twice on every change - the default answers, and a
proprietary render with names of its own - checks the files rendered, installs each and runs its
tests, on ubuntu 3.11/3.13 and windows 3.13. Until BEA 1.0 is on PyPI it installs BEA and
project-configuration from git (`uv pip install --override`), which needs the
`C_ENERGIE_READ_TOKEN` secret while those repositories are private.

Locally:

```bash
uvx copier copy --defaults --vcs-ref HEAD . /tmp/rendered
uv pip install --override overrides.txt -e "/tmp/rendered[test]"   # overrides: BEA and PC from git
cd /tmp/rendered && TEST_TIER=fast python -m unittest discover -v
```
