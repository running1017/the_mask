FROM python:3.9-slim-buster

WORKDIR /workdir

RUN apt-get update \
   && apt-get install -y --no-install-recommends \
      libgl1-mesa-dev \
      libglib2.0-0 \
   && apt-get -y clean \
   && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt ./config/requirements.txt
RUN pip install -r ./config/requirements.txt

CMD ["python", "main.py"]
