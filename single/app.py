from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 


app = Flask(__name__)
app. config['SQLALCHEMY_DATABASE_URI']='sqlite:///book.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class books(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  name = db.Column(db.String, nullable = False)
  rating = db.Column(db.Integer, nullable = False)
  author = db.Column(db.String(50), nullable = True)
  
  def __repr__(self):
      return '<book_name %r>' % self.name




@app.route('/', methods = ['GET'])
def book_list():
  results  = books.query.all()
  datas =[]
  for result in results:
    data={'name':result.name,
      'author':result.author,
      'rating':result.rating,
      'id':resul
    }
    datas.append(data)
  return jsonify(datas)



@app.route('/<int:id>', methods = ['GET'])
def book_data(id):
  result = books.query.filter_by(id=id).first()
  if result == None:
    data = {'message':'book doesn\'t exist'}
  else:
   data={'name':result.name,
        'author':result.author,
        'rating':result.rating,
        'id':result.id
      }
  return jsonify(data)



@app.route('/<int:id>/delete', methods = ['DELETE'])
def book_remove(id):
  result = books.query.filter_by(id=id).first()
  if result == None:
    return {'message':str(id) + ' doesn\'t exist'}
  else:
    db.session.delete(result)
    db.session.commit()
    return {'message':str(id) + ' removed'}


@app.route('/<int:id>/update', methods = ['POST'])
def book_update(id):
  result = books.query.filter_by(id=id).first()
  if result == None:
      return {'message':str(id) + ' doesn\'t exist'}
  elif request.method == 'POST':
    if request.form.get('name') is not None:
        result.name = request.form.get('name')
        db.session.commit()
    if request.form.get('rating') is not None:
        result.rating = int(request.form.get('rating'))
        db.session.commit()
    if request.form.get('author') is not None:
        result.author = request.form.get('author')
        db.session.comm
    return {'message':'book_updated'}

@app.route('/add', methods = ['POST'])
def book_add():
  if request.method == 'POST':
    name = request.form.get('name')
    rating = int(request.form.get('rating'))
    author = request.form.get('author')

    new = books(name=name,rating=rating,author=author)
    db.session.add(new)
    db.session.commit()
    return jsonify({'message':'book_added'})

    

  

if __name__ =='__main__':
  app.run(debug=True)