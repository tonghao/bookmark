from flask import Flask,render_template,flash
from flask import redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data1.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev'

# ======================数据库==========================
db = SQLAlchemy(app)

class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80),nullable=False)
    url = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<Bookmark(id={self.id}, title={self.title})"

def init_db():
    with app.app_context():
        # 创建所有表
        db.create_all()    

# ======================路由==========================
  
@app.route('/')
def index():
    return redirect(url_for('bookmarks'))

@app.route("/bookmarks")
def bookmarks():
    bookmarks_data = Bookmark.query.all()    
    return render_template('bookmarks.html', bookmarks=bookmarks_data)

@app.route("/bookmarks/add", methods=['GET', 'POST'])
def add_bookmark():
    if request.method == 'POST':
        title = request.form.get("title")
        url = request.form.get("url")

        if not title or not url:
            flash('标题和URL都不能为空')
            return render_template('add_bookmark.html')
        bookmark = Bookmark(title = title, url=url)
        db.session.add(bookmark)
        db.session.commit()

        flash('书签添加成功!')
        return redirect(url_for('bookmarks'))
    return render_template('add_bookmark.html')

@app.route('/bookmarks/delete/<int:bookmark_id>')
def delete_bookmark(bookmark_id):
    """删除书签"""
    return "请实现相关功能"


if __name__ == '__main__':
    init_db()
    
    print("\n" + "="*50)
    print("📚 Bookmark Service")
    print("="*50)
    print("🌐 地址: http://localhost:5000")
    print("="*50 + "\n")

    app.run(debug=True)
