from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///portfolio.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    tech_stack = db.Column(db.Text)
    github_link = db.Column(db.String(500))
    image = db.Column(db.String(200))
    featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    author = db.relationship('User', backref='posts')

class NewsItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    source = db.Column(db.String(200))
    link = db.Column(db.String(500))
    image_url = db.Column(db.String(500))
    published_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Admin setup
admin = Admin(app, name='Portfolio Admin', template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Project, db.session))
admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(NewsItem, db.session))

# Routes
@app.route('/')
def index():
    # Initialize database on first request
    try:
        from init_db import init_database, start_news_updater
        init_database()
        # Start news updater if not already running
        if not hasattr(app, '_news_updater_started'):
            start_news_updater()
            app._news_updater_started = True
    except Exception as e:
        print(f"Init error: {e}")
    
    projects = Project.query.filter_by(featured=True).all()
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    news = NewsItem.query.order_by(NewsItem.published_at.desc()).limit(5).all()
    
    profile = {
        'name': 'Dhruvi Mittal',
        'degree': 'Second-Year BSc (Hons) Cloud Computing Student',
        'headline': '🌩️ Cybersecurity Enthusiast & Cloud Explorer',
        'about': (
            "Dhruvi Mittal is a passionate and dedicated learner focused on securing the digital world with cutting-edge cloud security practices, ethical hacking, and AI-driven security analytics.\n\n"
            "She continuously explores multi-cloud management (AWS, GCP, Azure), Infrastructure as Code (Terraform, CloudFormation), container security, Kubernetes hardening, and serverless security — combining innovation with practical implementation.\n\n"
            "💡 Personal Motto: 'Securing the digital world one line of code at a time.'\n\n"
            "Outside the tech world, Dhruvi loves music, gaming, traveling, and coding, bringing creativity and curiosity into everything she builds."
        )
    }
    
    return render_template('index.html', projects=projects, posts=posts, news=news, profile=profile)

@app.route('/portfolio')
def portfolio():
    projects = Project.query.all()
    return render_template('portfolio.html', projects=projects)

@app.route('/blog')
def blog():
    query = request.args.get('q', '').strip()
    page = request.args.get('page', 1, type=int)
    
    posts_query = Post.query.order_by(Post.created_at.desc())
    
    if query:
        posts_query = posts_query.filter(
            Post.title.contains(query) | Post.content.contains(query)
        )
    
    posts = posts_query.paginate(page=page, per_page=6, error_out=False)
    return render_template('blog.html', posts=posts, query=query)

@app.route('/news')
def news():
    news_items = NewsItem.query.order_by(NewsItem.published_at.desc()).all()
    return render_template('news.html', news=news_items)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST': 
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return render_template('register.html')
        
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('index'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/add_project', methods=['GET', 'POST'])
@login_required
def add_project():
    if request.method == 'POST':
        project = Project(
            title=request.form['title'],
            description=request.form['description'],
            tech_stack=request.form['tech_stack'],
            github_link=request.form['github_link'],
            featured=True
        )
        db.session.add(project)
        db.session.commit()
        flash('Project added successfully!')
        return redirect(url_for('index'))
    return render_template('add_project.html')

@app.route('/add_blog', methods=['GET', 'POST'])
@login_required
def add_blog():
    if request.method == 'POST':
        post = Post(
            title=request.form['title'],
            content=request.form['content'],
            author_id=current_user.id
        )
        db.session.add(post)
        db.session.commit()
        flash('Blog post added successfully!')
        return redirect(url_for('blog'))
    return render_template('add_blog.html')

@app.route('/project/<int:project_id>')
def project_detail(project_id):
    project = Project.query.get_or_404(project_id)
    return jsonify({
        'id': project.id,
        'title': project.title,
        'description': project.description,
        'tech_stack': project.tech_stack,
        'github_link': project.github_link,
        'image': project.image
    })

@app.route('/blog/<int:post_id>')
def blog_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return jsonify({
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'author': post.author.username if post.author else 'Dhruvi',
        'created_at': post.created_at.strftime('%B %d, %Y')
    })

@app.route('/news/<int:news_id>')
def news_detail(news_id):
    news = NewsItem.query.get_or_404(news_id)
    return jsonify({
        'id': news.id,
        'title': news.title,
        'source': news.source,
        'link': news.link,
        'image_url': news.image_url,
        'published_at': news.published_at.strftime('%B %d, %Y') if news.published_at else 'Recent'
    })

if __name__ == '__main__':
    app.run(debug=True)