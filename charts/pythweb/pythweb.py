from flask import Flask
from flask import request
import psycopg2
import datetime

conn = psycopg2.connect(database='postgres', user='postgres', password='postgres',
                        host='10.96.100.100', port='5432')


def add_ip(ip_client):
    with conn:
        with conn.cursor() as cur:
            now = datetime.datetime.now().isoformat(sep=' ', timespec='seconds')
            cur.execute('INSERT INTO public.ips (ip, date) VALUES (%s, %s)', (ip_client, now))

def get_ip_list():
    render=''
    with conn:
        with conn.cursor() as cur:
            cur.execute('select * from public.ips')
            result = cur.fetchall()
            for i in result:
                render+=f'<div>{i[0]} - {i[1]}</div>'
    return render


app = Flask(__name__)

@app.route('/')
def index():
    add_ip(request.environ['REMOTE_ADDR'])
    return f"You have visited a restricted website! \
            Your IP {request.environ['REMOTE_ADDR']} \
            has been saved at {datetime.datetime.now().isoformat(sep=' ', timespec='seconds')}!\
            {get_ip_list()}"

app.run(host='0.0.0.0', port=80)
