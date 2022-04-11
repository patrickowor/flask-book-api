from . import db

class books(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  name = db.Column(db.String, nullable = False)
  rating = db.Column(db.Integer, nullable = False)
  author = db.Column(db.String(50), nullable = True)
  detail = db.Column(db.String, nullable = True)
  chapters = db.relationship('chapter',backref = 'book' )
  
  def __repr__(self):
    return '<book_name %r>'% self.name
    
class chapter(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  # note when requesting from the form request for chapter with value as integer not page
  page = db.Column(db.Integer, nullable = False,)
  post = db.Column(db.String, nullable = False)
  book_id = db.Column(db.Integer, db.ForeignKey('books.id'))