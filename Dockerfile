FROM python:3.8-slim
MAINTAINER abduladeneye@gmail.com

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

WORKDIR /app

EXPOSE 8000

COPY ./requirements /app/requirements
RUN python -m pip install pip --no-cache-dir --upgrade
RUN pip install --no-cache-dir -r requirements/prod.txt

COPY . /app

ENTRYPOINT ["/entrypoint.sh"]
CMD ["gunicorn", "posts.wsgi", "-b 0.0.0.0:8000"]
