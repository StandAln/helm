from flask import Flask
from flask import request
import psycopg2
import datetime
import os

conn = psycopg2.connect(database=os.environ.get('PG_DATABASE'), 
                        user=os.environ.get('PG_USER'), 
                        password=os.environ.get('PG_PASSWORD'),
                        host=os.environ.get('POSTGRES_SERVICE_SERVICE_HOST'), 
                        port=os.environ.get('POSTGRES_SERVICE_SERVICE_PORT')
                        )


def add_ip(ip_client):
    with conn:
        with conn.cursor() as cur:
            now = datetime.datetime.now().isoformat(sep=' ', timespec='seconds')
            cur.execute('insert into public.ips (ip, date) values (%s, %s)', (ip_client, now))

def get_ip_list():
    render=''
    with conn:
        with conn.cursor() as cur:
            cur.execute('select * from public.ips order by date desc limit 50')
            result = cur.fetchall()
            for i in result:
                render+=f'<div>{i[0]} - {i[1]}</div>'
    return render


app = Flask(__name__)

@app.route('/')
def index():
    add_ip(request.environ['REMOTE_ADDR'])
    return f"You have visited this website \
            at {datetime.datetime.now().isoformat(sep=' ', timespec='seconds')} \
            from ip {request.environ['REMOTE_ADDR']} \
            Previous visits:{get_ip_list()}"


app.run(host='0.0.0.0', port=80)
