FROM python:3.9.13-alpine3.15

RUN pip install pyyaml
RUN pip3 install APScheduler
RUN pip3 install six
RUN pip3 install environs
RUN pip3 install wheel
RUN pip3 install discord-webhook

RUN mkdir /yaml
RUN mkdir /entry

ADD configInit.py /entry/
ADD main.py /entry/
ADD util.py /entry/

WORKDIR /entry/
CMD [ "python", "-u", "main.py" ]