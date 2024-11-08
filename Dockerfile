FROM python:3.8-slim
MAINTAINER abduladeneye@gmail.com

WORKDIR /app

EXPOSE 8000

COPY ./requirements /app/requirements
RUN python -m pip install pip --no-cache-dir --upgrade
RUN pip install --no-cache-dir -r requirements/prod.txt

COPY . /app

CMD ["uvicorn", "main:app", "--workers 1", "--host 0.0.0.0", "--port 8000"]