# Student Template

This template was made to suggest a basic setup for student Python projects.

## Project Structure

The purpose of directories is to store:

- **artifacts** - any kind of ML experiment outputs (models, plots, segmentation masks, etc.),
- **data** - objects of experiments,
- **notebooks** - Jupyter notebooks (.ipynb files),
- **src** - source code (all .py files).

## Project Tools

In the repository, you can find a few Python tool suggestions.

### [Black](https://github.com/psf/black)

Python code formatter. You can find predefined configs in the `.black.cfg` file.

### [Flake8](https://github.com/PyCQA/flake8)

Linting tool that checks Python codebase for errors, styling issues, and complexity. It covers more use cases than `Black` but does not format code. You can find predefined configs in the `.flake8` file.

### [Isort](https://pycqa.github.io/isort/)

Python library imports sorter. You can find predefined configs in the `.isort.cfg` file.

### [PyTest](https://docs.pytest.org/en/)

Python testing framework.

### [MyPy](https://mypy.readthedocs.io/en/stable/getting_started.html)

Optional static type checker for Python that aims to combine the benefits of dynamic (or "duck") typing and static typing.
If you have problems with missing stubs for a certain library, add the following lines to `mypy.ini`:

```ini
[mypy-LIBRARY_NAME.*]
ignore_missing_imports = True
```

### [NumPy](https://numpy.org/)

Library for a wide variety of mathematical operations on arrays, essential for machine learning algorithms.

### [Make](https://www.tutorialspoint.com/unix_commands/make.htm)

In the context of this repo, `make` enables you to define aliases for more complex commands so you don't have to rewrite them every time.

## Usage

### First Steps

1. **Create a virtual environment.**
   If you have never done it before, you may want to read about one of the following tools: [Python venv](https://docs.python.org/3/tutorial/venv.html#creating-virtual-environments), [Conda](https://conda.io/projects/conda/en/latest/index.html), or [Poetry](https://python-poetry.org/docs/managing-environments/) (more advanced). For switching between Python versions, read about [Pyenv](https://github.com/pyenv/pyenv?tab=readme-ov-file#unixmacos). It's recommended to choose a Python version available on the [scientific cluster](https://www.sc.uni-leipzig.de/02_Resources/Software/Categories/lang_modules/#python) as you may train models there.

2. **Install dependencies.**
   Development tools like `flake8` are listed in `requirements.txt`. Install them using the tool chosen in the previous step.

### Makefile Predefined Commands

Run:

- `make flake8` to check your source code quality,
- `make black` to format code,
- `make isort` to order imports,
- `make format` to run `isort` and `black` commands together,
- `make mypy` to check type hints,
- `make test` to run tests,
- `make build` to sequentially run `isort`, `black`, `flake8`, `mypy`, and `test`.

Feel free to define your custom commands if you want.

## Pro Tips

1. Write your code in Python scripts, not in notebooks; otherwise, you'll produce spaghetti code. The only exception can (but doesn't have to) be Exploratory Data Analysis (EDA) and visualizations.
2. Write [type hints](https://docs.python.org/3/library/typing.html). You can check them with `mypy`.
3. Commit often, probably more often than you usually do. Before committing, format and check your code (`make build`).
4. Refactor your code every time you finish implementing a new feature.
5. Use a code debugger.
6. Create a branch when introducing a new feature and keep the main branch bug-free. Merge the main branch with the feature branch only when you are sure there are no bugs.
7. Don't be afraid to use typical Python constructs like [list comprehensions](https://docs.python.org/3/library/typing.html). In most cases, they make your code more readable.
8. Write tests for crucial components; you'll find bugs much quicker. Don't spend too much time on them; you should stay focused on experiments. Keep your tests in the `src/tests` directory.
9. Use experiment tracking tools like [TensorBoard](https://www.tensorflow.org/tensorboard), [W&B](https://wandb.ai/site), etc.
10. Check if there is already an existing solution for your problem. A good example is a training/test loop implementation. If you use [TensorFlow](https://www.tensorflow.org/tutorials), add [Keras](https://www.tensorflow.org/guide/keras) to your code, and if you use [PyTorch](https://pytorch.org/tutorials/beginner/basics/intro.html), add [FastAI](https://docs.fast.ai/examples/migrating_pytorch_verbose.html) or [Lightning](https://lightning.ai/docs/pytorch/stable/starter/introduction.html) to train and evaluate your model. These frameworks provide boilerplate code for deep learning experiments.

## HPC Cluster

You're going to write your code and test it on your PC. Nevertheless to train your NN models you want to use faster and more capacious devices. One of the solution is to use university [high performence computing (HPC)](https://www.sc.uni-leipzig.de/) cluster.

### Registration

To use it, first, [apply](https://service.rz.uni-leipzig.de/scientific-computing/sc-infrastruktur-beantragen-en/) for scientific cluster account (latter we will refer to that as *SC account*). After receiving a confirmation mail your can go to the next step.

### Project setup

Before running your experiments you have to setup your project on the cluster. To do it follow the steps:

1. **[Log in]**(https://lab.sc.uni-leipzig.de/jupyter/hub/spawn)
After you get permission, log in to university jupyter lab server and select the machine you want to use. Choose minimal hardware requirements (single cpu, no gpu) as you won't need computational power to set up your project.
2. **Clone your repository**
Open the terminal, clone your repository (`git clone <your_repo_link>`).
3. **Load python**
Check available python versions using command `module avail python` and choose same as you work with on your local machine (e.g. 3.12.3). Then load it using command `module load`. Example: `module load Python/3.12.3-GCCcore-13.3.0`.
4. **Create a virtual environment**
There are two scenarios:
   1. All libraries that you're using in your project are preinstalled on the cluster.
   Check it using command `module avail <package_name>`. If all libraries are on the list,then just load them using command `module load <package_name>`.
   Tips:
      1. Follow the [link](https://www.sc.uni-leipzig.de/02_Resources/Software/#using-software-modules) for more informations about preinstalled libraries.
      2. Run your experiment scripts to make sure that libraries work well together. Otherwise use other scenario.
   2. Some libraries aren't preinstalled or you get compatibility errors.
   Go to your work directory `cd <directory_name>`. Then create your virtual environment: `python -m venv .venv`, activate it `source .venv/bin/activate` and install libraries: `pip install -r requirements.txt`.
5. **Exit cluster**
Go to `File -> Hub Control Panel` and click `Stop My Server`.
Now your session is over.

Congratulations! You're project setup is finished.
To run your experiments you need to transfer the data to the cluster. Before you do it, you may want to setup ssh client.

### SSH client

Jupyter lab isn't efficient with interacting with cluster. You have to wait until you're logged in, sometimes you can get kicked out or simply jupyter server doesn't respond.
Instead you can use terminal to interact with cluster via SSH client. The best case scenario is that you log in with simple command without passing password or typing complex url addres. To achieave this follow the [instruction](https://www.sc.uni-leipzig.de/03_System_access/Cluster/).
Focus on the following steps:

1. Log in to university [VPN](https://www.urz.uni-leipzig.de/en/service-catalogue/servicedetail/service/vpn-access-to-the-university-network).
1. Test you connection.
`ssh <uni_login>@login01.sc.uni-leipzig.de`
1. [Generate ssh key](https://www.sc.uni-leipzig.de/03_System_access/Cluster/#generating-an-ssh-key).
1. [Add ssh key](https://www.sc.uni-leipzig.de/03_System_access/Cluster/#add-ssh-key-to-your-sc-account) to your SC account.
1. Create [config file](https://www.sc.uni-leipzig.de/03_System_access/Cluster/#ssh-config-file).
Pay attention to the `IdentityFile` path.
1. Test connection with your new setup.
`ssh <your_host_name>`

Now you're ready to use cluster via ssh client.

### Data upload

HPC enables you to keep your data in few ways. However all of them have some limitions, mostly memory.
Previously you upload your project to `Home Quota`. However, it has some memory limitations. Instead of that you want to use `Work Quota`.

#### Create workspace directory

To create such space you need to log in to the cluster (via ssh or jupyter lab) and allocate memory use command: `ws_allocate <workspace_name> <number_of_days>`. It will create directory `/work/<uni_login><workspace_name>`.

#### Transfer between PC and Cluster

To transfer data between your PC and Cluster run terminal on your local PC and use command: `scp <source> <target>`.To copy file from your PC to cluster run:
`scp path/to/PC/file <your_host_name>:/path/to/cluster/directory`.
To copy file from your SC account to local PC run:
`scp <your_host_name>:/path/to/cluster/file path/to/PC/directory`.
Use flag `-r` to transfer directories.

#### Workspace lifespan

<span style="color:red">Workspaces have limited lifespan of maximum 30 days</span>. To keep them, you have to extend it using command `ws_extend <workspace_name> <number_of_days>`. Otherwise you'll lose all of your data. Therefore it's recomended not to use work directory as a storage, rather as a copy space for the data and aftifacts.

### Code integration

Running scripts both on the local PC and in the cluster can lead to errors. E.g. path to the dataset on your local PC is `data/taxi.csv`, on your SC account `/work/<uni_login><workspace_dir>/data/taxi.csv`. Providing the fixed path would lead to `FileNotFoundError`.
Similar problem can appear when you test training scrips. Typically you want to test your code locally before pushing to the cluster. Because of hardware limitations you minimize training requirements including batch size and number of workers. Every time you switch between PC and cluster you would have to change these numbers. Therefore these values have to be set dinamically.

#### Dotenv

One of the sollutions is to use `.env` file. In this file you define all the variables that need to be change depending on the platform you use. Then, whenever you have to provide path or memory related value you load it from .env. The key of this technique is:

- to create customized `.env` files on each platform,
- to keep `.env` file excluded from git repository so it doesn't update every time you push changes.

##### Example

Let's go back to the example of `taxi.csv` file. Previously to define the path to this file you would use fixed value:

```python
dataset_path = Path("data/taxi.csv")
```

which would lead to the `FileNotFoundError` on the cluster.
To avoid it, create separate `.env` files on you PC and on SC account based on the example files in this template:  `.env_local_example` and `.env_cluster_example`.
Then refactor your code in following way:

```python
import os

from dotenv import load_env

load_dotenv()  # loads variables defined in .env file as environment variables
DATA_DIR = os.getenv("DATA_DIR", default="data/")  

path = Path(DATA_DIR + "taxi.csv")
```

### Submitting SLURM jobs

Next to you there are plenty of people who want to use cluster at the same time. To overcome the problem of limited resources cluster has to somehow prioritize requests and put them in the queue. And here with help comes job scheduler called SLURM. Instead of logging to jupyter lab, choosing the partition, selecting the devices and wishing for not being rejected you can can simply schedule the job to do to SLURM. This app will prioritize you request based on the requirements, estimate when the system will be ready to handle it and run your script in the right moment.
To define the job you have to create bash script containing:

- slurm setup - informations like how many cpus and gpus your job require, maximum time for running it and ect.
- module loading - all commands loading preinstalled libraries or activating your virtual enviroment,
- python script execusion - which script to execute and how.

You can find example script in `scripts/slurm/training_example.sh`.
**WARNING**: the more resources and usage time you apply for the lower priority will get your job.
There are few basic commands you need to know while using SLURM. To schedule the job run:
`sbatch path/to/slurm/script.sh`
SLURM will assign ID to created job. To see all scheduled job and their IDs run:
`squeue -u $USER`
To check job status run:
`scontrol show job <job_ID>`
You're mostly interested in two postions: *StartTime* indicating when your experiment will start and *JobState* describing if your job is pending, run, was cancelled or failed.
To cancel the job run:
`scancel <job_ID>`.

### Protips

1. Sometimes you need to change single line in your code after pulling it on the cluster. Use *vim* to quickly change it using terminal.
1. To prevent any conflicts and mistakes, commit only on your local PC and on SC accout only pull.
1. If due to manual changes on the cluster there were some conflicts, don't panic, reset your code to last commit using `git reset --hard` command. As long as you commit only on your local PC, nothing will happen.
1. Minimize your job requirements to get earlier in the queue.

## Git

Git is a version control system that helps you maintain your repository. More than 50% of your work time you'll refactor your code. A lot of things may happen. To keep track of the changes, create a checkpoints, test different configurations of code, rollback to previous checkpoint and prevent a lot of mistakes you should use git (even in solo projects).
There are few basic commands that you should learn by heart:

`git clone <url>` - Creates a local copy of a remote repository.

4 following commands are the most crucial for maintaining your repository. Use them in the following order every time you implement minor changes:

`git status` - Displays the current state of the working directory and staging area.
`git add <file>` - Stages changes in a file for the next commit.
`git commit -m "<message>"` - Saves staged changes with a descriptive message.
`git push` - Uploads local commits to a remote repository.

Commands that you're going to use mostly on the cluster:

`git pull` - Fetches updates from a remote repository and merges them into the current branch.
`git reset <file>` - Unstages a file while retaining its changes in the working directory.

Commands creating and managing branches (good practice for introduceing new features):

`git branch` - Lists, creates, or deletes branches in the repository.
`git checkout <branch>` - Switches to a different branch or commit.
`git merge <branch>` - Integrates changes from one branch into the current branch.

To check last commits use:

`git log` - Shows the history of commits in the repository.

Alternatively you can use gui version like [gitkraken](https://www.gitkraken.com/).

## Extras

### VSCode extensions

If you use VSCode as your IDE, consider following extensions as supporting tool in your programming:

- Pylance
- Flake8
- auoDocstring
- Prettify JSON
- Python Test Explorer
