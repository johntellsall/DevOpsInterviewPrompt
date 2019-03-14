FROM python:3.6-alpine
ADD . /code
WORKDIR /code
RUN pip install -qr requirements.txt
CMD ["python", "app.py"]
