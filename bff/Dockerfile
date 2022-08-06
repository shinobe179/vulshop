FROM python:3.10.4

WORKDIR /tmp
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get -y upgrade && \
    #apt-get install -y wget gcc g++ make sqlite3 && \
    #wget -q https://dev.mysql.com/get/mysql-apt-config_0.8.22-1_all.deb && \
    #apt-get -y install ./mysql-apt-config_*_all.deb && \
    #apt-get -y update && \
    apt-get -y install build-essential libssl-dev libffi-dev python3-dev

RUN useradd --uid=1001 --create-home bff
USER bff

RUN mkdir -p /home/bff/
WORKDIR /home/bff/

COPY --chown=bff:bff ./ /home/bff/
RUN pip install -U pip && \
    pip install --user poetry && \
    /home/bff/.local/bin/poetry install

#COPY --chown=bff:bff ./ /home/bff/

CMD ["/home/bff/.local/bin/poetry", "run", "python", "bff.py"]