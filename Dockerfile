FROM python:3.10-slim

RUN apt-get update \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /home
COPY ./requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY / .

EXPOSE 80

CMD ["python3", "main.py"]