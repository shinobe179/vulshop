FROM python:3.10.4

WORKDIR /tmp
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get -y upgrade && \
    #apt-get install -y wget gcc g++ make sqlite3 && \
    wget -q https://dev.mysql.com/get/mysql-apt-config_0.8.22-1_all.deb && \
    apt-get -y install ./mysql-apt-config_*_all.deb && \
    apt-get -y update && \
    apt-get -y install mysql-client build-essential libssl-dev libffi-dev python3-dev

RUN useradd --uid=1001 --create-home api
USER api

RUN mkdir -p /home/api/
WORKDIR /home/api/

COPY --chown=api:api ./ /home/api/
RUN pip install -U pip && \
    pip install --user poetry && \
    /home/api/.local/bin/poetry install

#COPY --chown=api:api ./ /home/api/

CMD ["/home/api/.local/bin/poetry", "run", "python", "api.py"]