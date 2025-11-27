from flask import Flask,render_template,flash
from flask import redirect,url_for,request, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data1.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev'

# ======================数据库==========================
db = SQLAlchemy(app)

class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(80),nullable=False)
    url = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Bookmark(id={self.id}, title={self.title})"
    
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=True)
    password_hash = db.Column(db.String(255), nullable=True)

    bookmarks = db.relationship('Bookmark', backref='user',lazy=True,cascade='all, delete-orphan')

    def set_password(self, raw_password):
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        return check_password_hash(self.password_hash, raw_password)


def init_db():
    with app.app_context():
        # 创建所有表
        db.create_all()

        if not User.query.filter_by(username='zhangsan').first():
            user1 = User(username='zhangsan')
            user1.set_password('123456')
            db.session.add(user1)
            db.session.commit()
            print('创建用户zhangsan,密码（123456）')
        if not User.query.filter_by(username='lisi').first():
            user2 = User(username='lisi')
            user2.set_password('123456')
            db.session.add(user2)
            db.session.commit()
            print('创建用户lisi,密码（123456）')

# ======================路由==========================

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        user_id = session.get('user_id')
        if not user_id:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrapper


  
@app.route('/')
def index():
    return redirect(url_for('bookmarks'))

@app.route("/bookmarks")
@login_required
def bookmarks():
    user_id = session.get('user_id')
    bookmarks_data = Bookmark.query.filter_by(user_id=user_id).all()
    return render_template('bookmarks.html', bookmarks=bookmarks_data)

@app.route("/bookmarks/add", methods=['GET', 'POST'])
@login_required
def add_bookmark():
    if request.method == 'POST':
        title = request.form.get("title")
        url = request.form.get("url")

        if not title or not url:
            flash('标题和URL都不能为空')
            return render_template('add_bookmark.html')
        user_id = session.get('user_id')
        bookmark = Bookmark(title=title, url=url, user_id=user_id)
        db.session.add(bookmark)
        db.session.commit()

        flash('书签添加成功!')
        return redirect(url_for('bookmarks'))
    return render_template('add_bookmark.html')

@app.route('/bookmarks/delete/<int:bookmark_id>')
@login_required
def delete_bookmark(bookmark_id):
    """删除书签"""
    bm = Bookmark.query.get(bookmark_id)
    if bm:
        db.session.delete(bm)
        db.session.commit()
        flash("书签已删除")
    else:
        flash("书签不存在！")
    return redirect(url_for("bookmarks"))

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username','')
        password = request.form.get('password','')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('bookmarks'))
        
        flash('用户名或密码不正确')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    init_db()
    
    print("\n" + "="*50)
    print("📚 Bookmark Service")
    print("="*50)
    print("🌐 地址: http://localhost:5000")
    print("="*50 + "\n")

    app.run(debug=True)
