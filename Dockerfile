FROM python:3.11.4-alpine

WORKDIR /app/rework

RUN pip3 install pipenv
COPY rework/Pipfile .
COPY rework/Pipfile.lock .
# RUN pipenv lock
RUN pipenv sync
RUN pipenv run pip3 freeze
# ENTRYPOINT [ "/bin/sh" ]

ENTRYPOINT [ "pipenv", "run", "python3" ]
CMD [ "rework.py" ]