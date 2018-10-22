FROM       python:3.6-slim-stretch
RUN        pip install kubernetes==6.0.0
COPY       scripts /scripts/
ENV         PYTHONUNBUFFERED=1
CMD [ "python", "-u", "/scripts/pull_configmaps.py" ]
