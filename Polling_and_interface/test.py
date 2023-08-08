from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hello')
def hello_world2():
   return 'hello world2'
if __name__ == '__main__':
   app.run()

