# adapted from https://docs.docker.com/compose/gettingstarted/
# 
import json
import time

import redis
from flask import Flask, request


app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)


# TODO: move retry logic to decorator, add to do_get_count
def do_increment_count():
    "increment count in Redis, return value"
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

def do_get_count():
    "fetch count from Redis"
    return cache.get('hits')

def format_count_json(value):
    return json.dumps({'count': int(value)})

# --- ROUTES

@app.route('/count', methods=['GET', 'POST'])
def increment_count():
    if request.method == 'POST':
        value = do_increment_count()
    else:
        value = do_get_count()
    return format_count_json(value)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)