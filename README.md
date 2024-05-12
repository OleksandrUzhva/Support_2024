Support web applecation


Working with "pipenv" and useing framework Django

# Creat a new virtual enviroment 
pipenv shell

# Creating a .lock file frome Pipenv file
pipenv lock

# Installing dependencies from .lock file
pipenv sync


# Deploy with Docker compose
cp .env.default .env
docker compose build && docker compose up -d 