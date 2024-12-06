# Environment
```
python=3.8
pandas=2.0.3
pytrends=4.9.2
```

# Conda Environment
Makesure you are already install Anaconda or Miniconda and conda command is available in terminal.
```
conda create -n <env_name> python=3.8
conda activate <env_name>
pip install -r requirements.txt
```

# Modification
1. Locate to `'[Miniconda/Anaconda Path]/envs/<env_name>/Lib/site-packages/pytrends/request.py'`
2. Replaced `'method_whitelist'` by `'allowed_methods'`

# Code Description
* `keywords`: [https://pypi.org/project/pytrends/](https://pypi.org/project/pytrends/)
* `geo`: Two letter country abbreviation
* `start_date` and `end_date`: Specify the range of date in 'YYYY-MM-DD' format. Leaves it empty if you want overall information.