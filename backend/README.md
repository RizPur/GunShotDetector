Below are the instructions converted into Markdown language:

## Steps to run the backend server

### Django Setup

1. Create a python virtual environment using python 3.10
2. Activate the virtual environment that was created
3. Install the python packages by running the command `pip install -r requirements.txt` in the root of the project
4. After the packages have been installed. Navigate to the `gun_shot_detector` folder and run the command `python manage.py makemigrations` to create the migration file if it does not exist. The file should already exist in most cases.
5. To apply the migration changes run the command `python manage.py migrate`

### Redis Setup

1. Download the redis server for your respective environment

**macOS**

- You may run the command `brew install redis`

**Windows**

- You may follow the instructions outlined in this article [https://redis.io/docs/getting-started/installation/install-redis-on-windows/](https://redis.io/docs/getting-started/installation/install-redis-on-windows/) or install using docker

**Ubuntu**

1. Run the commands below
2. `sudo apt install lsb-release curl gpg`
3. `curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg`
4. `echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list`
5. `sudo apt-get update`
6. `sudo apt-get install redis`

### Running the Applications

1. Start the redis server and allow it to listen on port 6379 by running the command `redis-server --port 6379`
2. Navigate to the `gun_shot_detector` folder and ensure the virtual environment is activated
3. Run the command `python manage.py runserver` to start the Django application
