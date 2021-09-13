FROM python:3.9

RUN mkdir /app
WORKDIR /app

COPY run.py config.py constants.py gunicorn-cfg.py requirements.txt ./
COPY app app

RUN pip install -r requirements.txt
ENV FLASK_APP run.py
EXPOSE 8080
CMD ["gunicorn", "--config", "gunicorn-cfg.py", "run:app"]