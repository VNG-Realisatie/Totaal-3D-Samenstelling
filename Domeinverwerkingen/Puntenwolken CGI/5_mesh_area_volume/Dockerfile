FROM python:3.8
WORKDIR /usr/src/app
RUN apt-get update && apt-get install -y libgl1
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY meshlab.py .
ENTRYPOINT [ "python3", "meshlab.py" ]