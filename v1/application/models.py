from . import db

class books(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  name = db.Column(db.String, nullable = False)
  rating = db.Column(db.Integer, nullable = False)
  author = db.Column(db.String(50), nullable = True)
  
  def __repr__(self):
    return '<book_name %r>'% self.name