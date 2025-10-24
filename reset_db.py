from app import app, db, Project, Post, NewsItem
from datetime import datetime
import os

def reset_database():
    with app.app_context():
        # Drop all tables
        db.drop_all()
        # Recreate all tables
        db.create_all()
        
        # Add 4 projects
        projects = [
            Project(title='Quote App', description='A simple web app displaying random quotes with Docker deployment', tech_stack='Docker, GCP, Python, Flask', github_link='https://github.com/Dhruvi-tech/Quote_app', image='Quote_app.png', featured=True),
            Project(title='File Encryption Tool', description='Advanced Python CLI tool for secure file encryption with AES-256', tech_stack='Python, Cryptography, Security, CLI', github_link='https://github.com/Dhruvi-tech/File-Encryption-Tool', image='File-Encryption-Tool.png', featured=True),
            Project(title='Firebase Chat App', description='Real-time chat application with React and Firebase authentication', tech_stack='React, Firebase, JavaScript, CSS, Authentication', github_link='https://github.com/Dhruvi-tech/firebase-chat-app', image='firebase-chat-app.png', featured=True),
            Project(title='Secure Distributed File Backup System', description='Enterprise-grade distributed file backup system with end-to-end encryption and redundancy', tech_stack='Python, Distributed Systems, Encryption, Cloud Storage, Blockchain', github_link='https://github.com/Dhruvi-tech/Secure-Distributed-File-Backup-System', image='Secure-Distributed-File-Backup-System.png', featured=True)
        ]
        for project in projects:
            db.session.add(project)
        
        # Add 5 blog posts
        posts = [
            Post(title='Multi-Cloud Security Best Practices', content='Comprehensive guide to securing workloads across AWS, GCP, and Azure with unified security approaches and automation.', author_id=None),
            Post(title='Container Security and Kubernetes Hardening', content='Deep dive into container security, Kubernetes hardening techniques, and implementing security policies in containerized environments.', author_id=None),
            Post(title='Zero Trust Architecture in Cloud', content='Implementing Zero Trust principles in modern cloud environments with practical examples and security frameworks.', author_id=None),
            Post(title='AI-Driven Security Analytics', content='Leveraging artificial intelligence and machine learning for advanced threat detection and security incident response.', author_id=None),
            Post(title='Infrastructure as Code Security', content='Securing Infrastructure as Code (IaC) with Terraform, CloudFormation, and automated security scanning in CI/CD pipelines.', author_id=None)
        ]
        for post in posts:
            db.session.add(post)
        
        # Add 5 news items
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
        print("Database reset complete! Added 4 projects, 5 blogs, 5 news items.")

if __name__ == '__main__':
    reset_database()