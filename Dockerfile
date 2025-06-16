FROM python:3.12.11-bookworm

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY ./public ./public
COPY ./kb ./kb
COPY app.py  ./
COPY ./models ./models
COPY ./pipeline ./pipeline
COPY ./utils ./utils

EXPOSE 8080

CMD [ "python", "app.py"]