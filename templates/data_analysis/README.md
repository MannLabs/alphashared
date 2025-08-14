# Data analysis template

> {Replace} Simple template for reproducible data analysis workflows of -omics data.


## Install

1. In your command line interface, go to a directory of your choice.

2. Execute the following command

```shell
git clone ...
```

3. Open the newly generated directory in your favorite code editor.

4. Update license, `environment.yaml`, README.md, etc.


## Structure

> {Update}

```shell
├── README.md
├── LICENSE
├── .gitignore
├── config
│   ├── README.md
│   └── config.yaml
├── scripts
│   ├── step1.py
│   ├── step1.sbatch.sh 
│   ├── step2.R
│   ├── step2.sbatch.sh
│   └── src (optional)
│       └── module.py
├── notebooks
│   └── my-notebook1.py.ipynb
│   └── my-notebook2.r.ipynb
├── data
└── results
```

Document your project and configurations in READMEs. A short sentence often suffices. Document all parameters of your `config.yaml` files (purpose and allowed data types). 


## Suggestions
> {Remove}

### Automated + linear processing

- Implement analysis scripts so that they can be run with a single command. Document utilized configuration parameters. Assure that every jupyter  notebook can be run in a single step

- Do not manipulate data manually (e.g. in excel between analysis steps) or make analysis steps non-linear (e.g. run jupyter notebook cells not in order). 

### Environment management 

- Manage your environment with a suitable package manager and make it accessible for other users 

```shell
# conda 
conda env export -n <environment> > environment.yaml

# mamba 
conda env export -n <environment> > environment.yaml

# pip 
pip freeze > requirements.txt 
```

Use `session_info2` in jupyter notebooks
```python
# end of notebook
from session_info2 import session_info
session_info()
> <environment info>
```

### (Manual) Sanity checks Look at your data

- Check intermediate results and think about whether they make sense.

- Do not just accept the output of your pipeline

### Project Tracking

- Track your project with git. Share it on github.

- Avoid ambiguous or confusing file naming 

### Documentation

- Explain your analysis, document parameters, variables, and rationales (why did you do this?) to your future self and others.



## About
> {Update}

Created in the Mann Lab, Department of Proteomics and Signal Transduction, Max Planck Institute for Biochemistry.

> MIT License
