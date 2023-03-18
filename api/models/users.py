from ..utils import db
from datetime import datetime




class User(db.Model):
  __tablename__='users'

  id = db.Column(db.Integer(), primary_key=True)

  full_name = db.Column(db.String(60), nullable=False)
  username = db.Column(db.String(60), nullable=False, unique=True)
  email = db.Column(db.String(60), nullable=False, unique=True)
  password_hash = db.Column(db.String(), nullable=False)
  role = db.Column(db.String())
  created_on = db.Column(db.DateTime(), default=datetime.utcnow)

  __mapper_args__ = {
      'polymorphic_on': role,
      'polymorphic_identity': 'user'
  }
  
  def __repr__(self):
    return f'<{User.username}>'

  def save(self):
    db.session.add(self)
    db.session.commit()

  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  @classmethod
  def get_user_by_id(cls, id):
    return cls.query.get_or_404(id)