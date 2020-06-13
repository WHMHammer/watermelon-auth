FROM python

WORKDIR /app

EXPOSE 80

COPY ./requirements.txt /app/requirements.txt

RUN pip3 install -r requirements.txt

COPY . /app

CMD uwsgi --http :80 --master --enable-threads --wsgi-file __init__.py --callable app
