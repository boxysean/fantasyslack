from flask import Flask

app = Flask(__name__)

@app.route('/')  
def index():  
    return "Hello, world (and cats)!", 200

@app.route('/api/v1/slack-event')
def slack_event():
    return "What?"

# We only need this for local development.  
if __name__ == '__main__':  
    app.run()
