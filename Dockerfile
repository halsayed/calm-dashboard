FROM python:3.9

RUN mkdir /app
WORKDIR /app

# install requirements
COPY requirements.txt ./
RUN pip install -r requirements.txt

# copy application files
COPY run.py config.py constants.py gunicorn-cfg.py ./
COPY app app

# run application
ENV FLASK_APP run.py
EXPOSE 8080
CMD ["gunicorn", "--config", "gunicorn-cfg.py", "run:app"]