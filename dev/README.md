# dev

This directory contains tools and utilities to support the development life cycle.

## Environment Setup

Install prerequisites and tools:

```sh
sudo apt update
sudo apt install -y git python python3 python3-pip python3-venv npm
# Upgrade pip and awscli to latest
python3.7 -m pip install --upgrade pip awscli #--trusted-host=pypi.python.org --trusted-host=pypi.org --trusted-host=files.pythonhosted.org
# Upgrade npm to latest
sudo npm install -g npm
# Install aws cdk
sudo npm install -g aws-cdk
```

Initialise a python virtual environment and install the required packages.

```sh
python3.7 -m virtualenv .env
source .env/bin/activate
pip install --upgrade pip #--trusted-host=pypi.python.org --trusted-host=pypi.org --trusted-host=files.pythonhosted.org
pip install -r requirements.txt #--trusted-host=pypi.python.org --trusted-host=pypi.org --trusted-host=files.pythonhosted.org
```

Check that the `cdk` can be executed in the project

```sh
cdk ls
```
