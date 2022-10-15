FROM python:3.10.7

WORKDIR /tmp
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get install -y wget gcc g++ make sqlite3 && \
    wget -q https://dev.mysql.com/get/mysql-apt-config_0.8.22-1_all.deb && \
    apt-get -y install ./mysql-apt-config_*_all.deb && \
    apt-get -y update && \
    apt-get -y install mysql-client build-essential libssl-dev libffi-dev python3-dev

RUN useradd --uid=1001 --create-home app
USER app

RUN mkdir -p /home/app/
WORKDIR /home/app/

COPY --chown=app:app ./ /home/app/
RUN pip install -U pip && \
    pip install --user poetry && \
    /home/app/.local/bin/poetry install

#COPY --chown=app:app ./ /home/app/

CMD ["/home/app/.local/bin/poetry", "run", "python", "app.py"]