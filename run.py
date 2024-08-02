from app import create_app, create_celery_app, db

app = create_app()
celery = create_celery_app(app)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run()
