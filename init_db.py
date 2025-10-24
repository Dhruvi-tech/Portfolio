from app import app, db, Project, Post, NewsItem
from datetime import datetime, timedelta
import requests
import threading
import time

def fetch_tech_news():
    """Fetch latest tech news from NewsAPI"""
    try:
        # Using free NewsAPI - replace with your API key
        api_key = "demo"  # Get free key from newsapi.org
        url = f"https://newsapi.org/v2/everything?q=cybersecurity OR cloud computing OR AI security&sortBy=publishedAt&pageSize=5&apiKey={api_key}"
        
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            articles = response.json().get('articles', [])
            
            with app.app_context():
                # Clear old news (keep only last 10)
                old_news = NewsItem.query.order_by(NewsItem.created_at.desc()).offset(10).all()
                for item in old_news:
                    db.session.delete(item)
                
                # Add new articles
                for article in articles[:5]:
                    existing = NewsItem.query.filter_by(title=article['title']).first()
                    if not existing:
                        news_item = NewsItem(
                            title=article['title'][:300],
                            source=article['source']['name'],
                            link=article['url'],
                            image_url=article.get('urlToImage', 'https://images.unsplash.com/photo-1555949963-aa79dcee981c?w=350&h=200&fit=crop'),
                            published_at=datetime.fromisoformat(article['publishedAt'].replace('Z', '+00:00'))
                        )
                        db.session.add(news_item)
                
                db.session.commit()
                print("Tech news updated successfully!")
    except Exception as e:
        print(f"Error fetching news: {e}")

def start_news_updater():
    """Start background thread to update news daily"""
    def update_loop():
        while True:
            fetch_tech_news()
            time.sleep(86400)  # 24 hours
    
    thread = threading.Thread(target=update_loop, daemon=True)
    thread.start()

def init_database():
    with app.app_context():
        db.create_all()
        
        # Add projects if none exist
        if not Project.query.first():
            projects = [
                Project(title='Quote App', description='A simple web app displaying random quotes with Docker deployment', tech_stack='Docker, GCP, Python, Flask', github_link='https://github.com/Dhruvi-tech/Quote_app', image='Quote_app.png', featured=True),
                Project(title='File Encryption Tool', description='Advanced Python CLI tool for secure file encryption with AES-256', tech_stack='Python, Cryptography, Security, CLI', github_link='https://github.com/Dhruvi-tech/File-Encryption-Tool', image='File-Encryption-Tool.png', featured=True),
                Project(title='Firebase Chat App', description='Real-time chat application with React and Firebase authentication', tech_stack='React, Firebase, JavaScript, CSS, Authentication', github_link='https://github.com/Dhruvi-tech/firebase-chat-app', image='firebase-chat-app.png', featured=True),
                Project(title='Secure Distributed File Backup System', description='Enterprise-grade distributed file backup system with end-to-end encryption and redundancy', tech_stack='Python, Distributed Systems, Encryption, Cloud Storage, Blockchain', github_link='https://github.com/Dhruvi-tech/Secure-Distributed-File-Backup-System', image='Secure-Distributed-File-Backup-System.png', featured=True)
            ]
            for project in projects:
                db.session.add(project)
        
        # Add blogs if none exist
        if not Post.query.first():
            posts = [
                Post(title='Multi-Cloud Security Best Practices', content='Comprehensive guide to securing workloads across AWS, GCP, and Azure with unified security approaches and automation.', author_id=None),
                Post(title='Container Security and Kubernetes Hardening', content='Deep dive into container security, Kubernetes hardening techniques, and implementing security policies in containerized environments.', author_id=None),
                Post(title='Zero Trust Architecture in Cloud', content='Implementing Zero Trust principles in modern cloud environments with practical examples and security frameworks.', author_id=None),
                Post(title='AI-Driven Security Analytics', content='Leveraging artificial intelligence and machine learning for advanced threat detection and security incident response.', author_id=None),
                Post(title='Infrastructure as Code Security', content='Securing Infrastructure as Code (IaC) with Terraform, CloudFormation, and automated security scanning in CI/CD pipelines.', author_id=None)
            ]
            for post in posts:
                db.session.add(post)
        
        # Add initial news if none exist
        if not NewsItem.query.first():
            news = [
                NewsItem(title='AI-Powered Cybersecurity Tools Transform Threat Detection', source='TechCrunch', link='#', image_url='https://images.unsplash.com/photo-1555949963-aa79dcee981c?w=350&h=200&fit=crop', published_at=datetime.utcnow()),
                NewsItem(title='Cloud Security Spending Reaches Record High in 2024', source='Security Week', link='#', image_url='https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=350&h=200&fit=crop', published_at=datetime.utcnow()),
                NewsItem(title='Zero Trust Architecture Adoption Accelerates', source='CyberNews', link='#', image_url='https://images.unsplash.com/photo-1563986768609-322da13575f3?w=350&h=200&fit=crop', published_at=datetime.utcnow()),
                NewsItem(title='Kubernetes Security Vulnerabilities on the Rise', source='InfoSec', link='#', image_url='https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=350&h=200&fit=crop', published_at=datetime.utcnow()),
                NewsItem(title='Multi-Cloud Management Tools See Major Updates', source='Cloud Computing', link='#', image_url='https://images.unsplash.com/photo-1544197150-b99a580bb7a8?w=350&h=200&fit=crop', published_at=datetime.utcnow())
            ]
            for item in news:
                db.session.add(item)
        
        db.session.commit()
        print("Database initialized successfully!")
        
        # Start news updater
        start_news_updater()

if __name__ == '__main__':
    init_database()