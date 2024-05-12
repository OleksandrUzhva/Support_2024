FROM python:3.11.6-slim

# ENV PYTHONUNBUFFERED=1

# Update the system and install packages
RUN apt-get update -y \
    && pip install --upgrade pip \
    # dependencies for Python packages
    && pip install --upgrade setuptools \
    && apt-get install -y build-essential \
    # install dependencies manager
    && pip install pipenv watchdog\
    # cleaning up unused fiels
    && rm -rf /var/lib/apt/lists/* 

# Install progect dependencies

COPY ./Pipfile ./Pipfile.lock /
RUN pipenv sync --system

# cd /app (get or create)
WORKDIR /app
COPY ./ ./

EXPOSE 8000

# CMD sleep 2 && python src/manage.py runserver

ENTRYPOINT ["python"]
CMD ["src/manage.py", "runserver", "0.0.0.0:8000"]
