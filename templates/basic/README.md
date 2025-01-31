# my_package

A basic template for a Python package. Copy it "as is" to a new repository
(make sure not to miss the hidden files/folders starting with `.`),
rename `my_package` -> `<your_project_name>` and commit it.

---

### Installation

```bash
conda create --name my_package python=3.11 -y
conda activate my_package
```

```bash
pip install -r requirements/requirements.txt
```

---
## Usage

```bash
python src/hello_world.py
```


---
## Development
### Extra requirements for development
```bash
pip install -r requirements/requirements_development.txt
```

### Run tests
```bash
python -m pytest
```


### pre-commit hooks
It is highly recommended to use the provided pre-commit hooks, as the CI pipeline enforces all checks therein to
pass in order to merge a branch.

The hooks need to be installed once by
```bash
pre-commit install
```
You can run the checks yourself using:
```bash
pre-commit run --all-files
```

If you feel a rule not fitting to your project (e.g. `D100`), disable it globally
by adding it to
`pyproject.toml`->`[tool.ruff.lint]`->`ignore`. Alternatively and preferably,
deactivate it for a specific line only by adding a comment `# noqa: D100`
