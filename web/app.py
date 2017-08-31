from flask import Flask
import time

app = Flask(__name__)


@app.route('/')
def index():
    return 'hey! this is running inside the stack! latest!!!'


@app.route('/slow')
def slow():
    time.sleep(3)
    return 'finally ready!'


if __name__ == '__main__':
    app.run(host='0.0.0.0')
