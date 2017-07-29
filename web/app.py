from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return 'hey! this is running inside the stack!'


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)