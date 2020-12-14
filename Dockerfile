FROM python:3.8
RUN apt-get update && \
    apt-get install -y openjdk-11-jre
WORKDIR /usr/src/app
COPY src/. /usr/src/app/
RUN pip install -r requirements.txt
# As default command we run each test in turn.
CMD python3 project.py