FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get -yq --no-install-recommends install sqlite3=3.*

COPY . .

CMD [ "python", "./run.py" ]
