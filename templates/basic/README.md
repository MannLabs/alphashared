# Basic template for small-size python project

(!) Work in progress

A basic template for a Python package.

1a. Set up a new GitHub repository and `git clone` it to `/path/to/new/repo`

OR

1b. Create a local repository:
```
mkdir /path/to/new/repo
cd /path/to/new/repo
git init
```

2. Download this template:
```bash
cd /path/to/new/repo

curl -L https://github.com/MannLabs/alphashared/archive/add_template.zip -o template.zip
unzip template.zip
cp -r alphashared-add_template/templates/basic/. .
rm -r template.zip alphashared-add_template
```

3. Create the initial commit:
```bash
git add * .*
git commit -a -m "initialize from template"
```

4. Remove everything above and including this line.


# my_package
A python package that does <nothing>.

## Python setup

### Using uv (preferred)
If not available on your system, [install uv](https://docs.astral.sh/uv/getting-started/installation/)
first.
```bash
uv sync
source .venv/bin/activate
uv pip install -e .
````

### Using conda
```bash
conda create --name my_package_env python=3.11 -y
conda activate my_package_env
uv pip install -e .
```

---
## Usage

```bash
python src/hello_world.py
```
or

```bash
uv run src/hello_world.py
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

The hooks need to be installed once, then they will run before every commit:
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
