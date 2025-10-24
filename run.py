#!/usr/bin/env python3
from app import app, db, Project, Post, NewsItem
from datetime import datetime

def create_sample_data():
    from app import db, Project, Post, NewsItem
    from datetime import datetime
    
    # Create all tables
    db.create_all()
    
    # Check if data already exists
    try:
        if Project.query.first():
            return
    except:
        pass  # Table doesn't exist yet

if __name__ == '__main__':
    with app.app_context():
        create_sample_data()
        
        print("Creating sample projects...")
        projects = [
            Project(
                title='Quote App',
                description='A simple web app displaying random quotes from various categories, deployed using Docker and Google Cloud Platform.',
                tech_stack='Docker, GCP, Python, Flask',
                github_link='https://github.com/Dhruvi-tech/Quote_app',
                image='Quote_app.png',
                featured=True
            ),
            Project(
                title='File Encryption Tool',
                description='A Python CLI tool enabling robust file encryption and decryption using the Fernet algorithm.',
                tech_stack='Python, Cryptography, Security',
                github_link='https://github.com/Dhruvi-tech/File-Encryption-Tool',
                image='File-Encryption-Tool.png',
                featured=True
            ),
            Project(
                title='Secure Distributed File Backup System',
                description='A secure, decentralized system for file backup with encryption and redundancy.',
                tech_stack='Python, AWS, Docker, Security',
                github_link='https://github.com/Dhruvi-tech/Secure-Distributed-File-Backup-System',
                image='Secure-Distributed-File-Backup-System.png',
                featured=True
            ),
            Project(
                title='Firebase Chat App',
                description='A real-time chat application built with React and Firebase featuring user authentication, Firestore integration, and a sleek responsive UI.',
                tech_stack='React, Firebase, JavaScript, CSS',
                github_link='https://github.com/Dhruvi-tech/firebase-chat-app',
                image='firebase-chat-app.png',
                featured=True
            ),

        ]
        
        for project in projects:
            db.session.add(project)
        
        print("Creating sample blog posts...")
        posts = [
            Post(
                title='Multi-Cloud Security: Best Practices for AWS, GCP, and Azure',
                content='As organizations adopt multi-cloud strategies, securing workloads across different cloud providers becomes critical. This post explores unified security approaches, identity federation, cross-cloud monitoring, and compliance strategies.',
                author_id=None
            ),
            Post(
                title='Container Security and Kubernetes Hardening',
                content='Container orchestration with Kubernetes introduces new security challenges. This comprehensive guide covers container image scanning, runtime security, network policies, RBAC implementation, and secrets management.',
                author_id=None
            ),
            Post(
                title='Infrastructure as Code Security with Terraform',
                content='Infrastructure as Code (IaC) revolutionizes cloud deployment but introduces security considerations. Learn how to implement secure Terraform practices, policy as code with Sentinel, state file security.',
                author_id=None
            ),
            Post(
                title='Zero Trust Architecture in Cloud Environments',
                content='Zero Trust security model is becoming essential for modern cloud architectures. This article explores implementing Zero Trust principles in cloud environments, including identity verification and least privilege access.',
                author_id=None
            ),
            Post(
                title='AI-Powered Cybersecurity: The Future of Threat Detection',
                content='Artificial Intelligence is transforming cybersecurity with advanced threat detection and response capabilities. This post covers machine learning algorithms for anomaly detection and behavioral analysis.',
                author_id=None
            )
        ]
        
        for post in posts:
            db.session.add(post)
        
        print("Creating sample news...")
        news_items = [
            NewsItem(
                title='AI-Powered Cybersecurity Tools Transform Threat Detection',
                source='TechCrunch',
                link='https://techcrunch.com/ai-cybersecurity',
                image_url='https://images.unsplash.com/photo-1555949963-aa79dcee981c?w=350&h=200&fit=crop',
                published_at=datetime.utcnow()
            ),
            NewsItem(
                title='Cloud Security Spending Reaches Record High in 2024',
                source='Security Week',
                link='https://securityweek.com/cloud-security-2024',
                image_url='https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=350&h=200&fit=crop',
                published_at=datetime.utcnow()
            ),
            NewsItem(
                title='Kubernetes Security: New Vulnerabilities Discovered',
                source='The Hacker News',
                link='https://thehackernews.com/kubernetes-security',
                image_url='https://images.unsplash.com/photo-1667372393119-3d4c48d07fc9?w=350&h=200&fit=crop',
                published_at=datetime.utcnow()
            ),
            NewsItem(
                title='Zero-Day Exploits Target Enterprise Networks Worldwide',
                source='CyberScoop',
                link='https://cyberscoop.com/zero-day-exploits',
                image_url='https://images.unsplash.com/photo-1563013544-824ae1b704d3?w=350&h=200&fit=crop',
                published_at=datetime.utcnow()
            ),
            NewsItem(
                title='Quantum Computing Threatens Current Encryption Standards',
                source='MIT Technology Review',
                link='https://technologyreview.com/quantum-encryption',
                image_url='https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=350&h=200&fit=crop',
                published_at=datetime.utcnow()
            )
        ]
        
        for news in news_items:
            db.session.add(news)
        
        db.session.commit()
        print("Database created with sample data!")
        print("Starting Flask app...")
        print("Visit: http://localhost:5000")
    
    app.run(host='0.0.0.0', port=5000, debug=True)

# Make create_sample_data available for import
__all__ = ['create_sample_data']