from flask_sqlalchemy import SQLAlchemy
from flask.cli import FlaskGroup
from app import app, db
from flask_migrate import Migrate, MigrateCommand

migrate = Migrate(app, db)

cli = FlaskGroup(app)

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=True)

    def __repr__(self):
        return f'<User {self.email}>'

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name
        }

@cli.command('db')
def db():
    pass

if __name__ == '__main__':
    cli()
