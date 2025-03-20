FROM python:3.8-slim-buster

# Set environment variables
ENV PYTHONUNBUFFERED 1
WORKDIR /SuccessAir
COPY requirements.txt /SuccessAir/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /SuccessAir/
EXPOSE 8100
CMD ["python", "manage.py", "runserver", "0.0.0.0:8100"]


