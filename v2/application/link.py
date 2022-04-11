from flask import (Blueprint, render_template, request, url_for, jsonify)
from . import db 
from .models import books

link = Blueprint('link', __name__)

@link.route('/', methods = ['GET'])
def book_list():
  results  = books.query.all()
  datas =[]
  for result in results:
    data={'name':result.name,
      'author':result.author,
      'rating':result.rating,
      'detail':result.detail,
      'id':result.id
    }
    datas.append(data)
  return jsonify(datas)



@link.route('/<int:id>', methods = ['GET'])
def book_data(id):
  result = books.query.filter_by(id=id).first()
  if result == None:
    data = {'message':'book doesn\'t exist'}
  else:
   data={'name':result.name,
        'author':result.author,
        'detail':result.detail,
        'rating':result.rating,
        'id':result.id,
        'chapters':len(result.chapters)
      }
  return jsonify(data)



@link.route('/<int:id>/delete', methods = ['DELETE'])
def book_remove(id):
  result = books.query.filter_by(id=id).first()
  if result == None:
    return {'message':str(id) + ' doesn\'t exist'}
  else:
    db.session.delete(result)
    db.session.commit()
    return jsonify({'message':str(id) + ' removed'})


@link.route('/<int:id>/update', methods = ['POST'])
def book_update(id):
  result = books.query.filter_by(id=id).first()
  if result == None:
      return jsonify({'message':str(id) + ' doesn\'t exist'})
  elif request.method == 'POST':
    if request.form.get('name') is not None:
        result.name = request.form.get('name')
        db.session.commit()
    if request.form.get('rating') is not None:
        result.rating = int(request.form.get('rating'))
        db.session.commit()
    if request.form.get('author') is not None:
        result.author = request.form.get('author')
        db.session.commit()
    if request.form.get('detail') is not None:
        result.detail = request.form.get('detail')
        db.session.commit()
    return jsonify({'message':'book_updated'})

@link.route('/add', methods = ['POST'])
def book_add():
  if request.method == 'POST':
    name = request.form.get('name')
    rating = int(request.form.get('rating'))
    author = request.form.get('author')
    detail = request.form.get('detail')

    new = books(name=name,rating=rating,author=author,detail=detail)
    db.session.add(new)
    db.session.commit()
    return jsonify({'message':'book_added'})

    
