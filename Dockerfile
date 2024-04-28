FROM --platform=linux/amd64 python:3.11.6-slim


# Update the system and install packages
RUN apt-get update -y \
    && pip install --upgrade pip \
    # dependencies for Python packages
    && pip install --upgrade setuptools \
    && apt-get install -y build-essential \
    # install dependencies manager
    && pip install pipenv \
    # cleaning up unused fiels
    && rm -rf /var/lib/apt/lists/* 

# Install progect dependencies

COPY ./Pipfile ./Pipfile.lock /
RUN pipenv sync --dev --system

# cd /app (get or create)
WORKDIR /app
COPY ./ ./

EXPOSE 8000

CMD sleep 2 && python src/manage.py runserver

# ENTRYPOINT ["python"]
# CMD ["src/manage.py", "runserver"]
