# Git Bash and Git Command Notes

This document covers general Bash and Git commands. Paths in Git Bash use forward slashes (/) instead of backslashes (\), as opposed to CMD.

## Git Bash Basics
This section includes general commands for navigation, file management, and managing virtual environments.

### Navigation
- Clear window: `clear`
- List directories: `ls`
- Change directory: `cd <directory_name>`
  - Back one directory: `cd ..`
  - Switch to previous directory: `cd -`
  - Return to home directory: `cd`

### File Management
Commands to create, move, and delete files or directories.

- Create directory: `mkdir <directory_name>`
  - Create directory with parent directories: `mkdir -p <parent_directory>/<directory_name>`
- Delete directory: `rmdir <directory_name>`
- Create empty file(s): `touch file1.txt file2.html`
- Create file with content:
  - Overwrite file: `echo "some text" > filename`
  - Append to file: `echo "some text" >> filename`
- Open file in Notepad: `notepad <filename>`
- Open file in VS Code: `code <filename>`
- View file in Bash: `cat <filename>`
- Delete file: `rm <filename>`
- Rename file: `mv <old_filename> <new_filename>`
- Move file(s):
  - Move file: `mv <source_file> <destination_directory>`
  - Move and rename: `mv <source_file> <destination_directory>/new_filename`
  - Move file: `mv myfile.txt ~/Desktop/Documents/` (example if the Documents folder is in another directory (e.g., ~/Desktop), use the full or relative path)
  - Move file: `mv file1.txt file2.txt file3.txt Documents/` (move multiple files)

## Managing Virtual Environments

### Python venv Virtual Environments setup
- Set up virtual environment: `python -m venv <environment_name>`
- Activate environment: `source <environment_name>/Scripts/activate`
- Install requirements: `pip install -r requirements.txt`
- Check installed packages: `pip list`
- Deactivate environment: `deactivate`

### Conda Virtual Environment setup
Pip can also be used as above, but consider pip the secondary option for installing packages.
- Set up Conda environment: `conda create --name <env_name> python=<version>`
- Initialize Conda in Git Bash: `conda init bash` (only required if not done before)
- Activate Conda environment: `conda activate <env_name>`
- Install packages from requirements file: `pip install -r requirements.txt`
- Install specific package(s): `conda install <package_name1> <package_name2>`
  - From specific channel: `conda install -c conda-forge <package_name>==<version>`
- Check installed packages: `conda list`
- Deactivate environment: `conda deactivate`

### Managing environments with Conda
- Export environment to requirements file: `conda list --export > requirements.txt`
- Export environment to .yml file: `conda env export > environment.yml`
- Create environment from .yml file: `conda env create -f environment.yml`
- Update environment from .yml file: `conda env update -f environment.yml`
- Delete environment: `conda env remove --name <env_name>`
- List available environments: `conda env list`

### Managing packages directly
- Search for available package versions: `conda search <package>`
- Version of package: `<package> --version`
- Version of package: `conda list <package>`
- Version of package: `pip show <package>`
- Install packages: `conda install <package>`
  - Specify channel: `conda install -c conda-forge stable-baselines3[extra]`
- Install packages: `pip install <package>`

---

# Git Version Control Commands

## Git Configuration
Relevant for association with commits.
- Set username (local): `git config user.name "Your Name"`
- Set username (global): `git config --global user.name "Your Name"`
- Check username: `git config user.name`
- Check global username: `git config --global user.name`
The above also applies for email. Simply substitute `<name>` for `<email>`.
- Unset local username: `git config --unset user.name`
- Unset local email: `git config --unset user.email`
- Check configuration: `git config --list`


## Standard Procedural Commands
- Initialize git repository: `git init`
- Stage file(s): 
  - Single file: `git add <filename>`
  - All files: `git add .`
- Commit changes: `git commit -m "<commit_message>"`
- View commit history: `git log`
- Remove all currently tracked files that should be ignored: `git rm -r --cached .`
  - Stage, commit, and push again to make Github reflect the .gitignore file

## Branching and Merging
- Create new branch: `git checkout -b <branch_name>`
- Switch branches: `git checkout <branch_name>`
- View all branches: `git branch`
- Merge branches: `git merge <branch_name>`
- Rebase branch: `git rebase <branch_name>`

## Working with Savepoints
- Go to specific commit: `git checkout <commit_hash>`
  - Note: To save new commits from this point, create a new branch first (see above)

## Remote Repository Management
- Clone repository: `git clone <repository_url>`
- View current remote URLs: `git remote -v`
- Set or change remote URL: `git remote set-url origin <new_url>` (example url: git@github.com:username/repo.git) 
- Add new remote: `git remote add <remote_name> <url>`
- Remove remote: `git remote remove <remote_name>`

### Setting Up SSH with GitHub
1. Generate SSH Key (if one does not already exist): `ssh-keygen -t ed25519 -C "your_email@example.com"`
2. Add SSH Key to SSH Agent:
   - `eval "$(ssh-agent -s)"`
   - `ssh-add ~/.ssh/id_ed25519`
3. Copy SSH Key to clipboard:
   - Windows: `clip < ~/.ssh/id_ed25519.pub`
   - Macbook: `pbcopy < ~/.ssh/id_ed25519.pub`
4. Add key to GitHub:
   - Go to GitHub settings → SSH and GPG keys → New SSH key, and paste the copied key.
Set or change remote url (see above).

## Pushing and Pulling to GitHub
- Set default upstream branch: `git branch --set-upstream-to=origin/main <branch_name>`
- Push to remote repository:
  - First-time push: `git push -u origin <branch_name>`
  - Standard push (after upstream set): `git push`
- Pull updates from remote: `git pull origin <branch_name>`

---

# Tips&Tricks

- Open chrome: `start chrome`
  - Specify webpage: `start chrome "youtube.com"`
- Check path: `which python`
- Check version: `python --version`
- Verify installation:
  - Installed using conda: `conda list <package>`
  - Installed using pip: `pip show <package>`
- Open working directory in file explorer: `explorer .`
  - Open specific folder: `explorer <folder_name>`

---
