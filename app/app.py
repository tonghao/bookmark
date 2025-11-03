from flask import Flask,render_template

app = Flask(__name__)

bookmarks_data = [
    {'name': 'Bilibili', 'url': 'https://www.bilibili.com'},
    {'name': '成都东软学院', 'url': 'https://www.nsu.edu.cn'},
    {'name': '百度', 'url': 'https://www.baidu.com'},
    {'name': 'GitHub', 'url': 'https://github.com'},
]

@app.route('/')
def index():
    app_title = "我的云书签"
    return render_template("index.html",title=app_title,bookmarks=bookmarks_data)

if __name__ == '__main__':
    app.run(debug=True)
