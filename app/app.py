from flask import Flask,render_template

app = Flask(__name__)

@app.route('/')
def index():
    app_title = "我的云书签"
    return render_template("index.html",title=app_title)

if __name__ == '__main__':
    app.run(debug=True)
