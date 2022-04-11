from flask import (Blueprint, render_template, request, url_for, jsonify)
from . import db 
from .models import books, chapter

chap_link = Blueprint('chap_link', __name__)


@chap_link.route('/<int:id>/chapter', methods = ['GET'])
def book_chapters_list(id):
  # querying database for data with the said id
  results  = books.query.filter_by(id=id).first()
  datas =[]
  #looping through the relational data of the said id of the table
  for result in results.chapters:
    data={'book name':results.name,
        'chapter':result.page,
        'post':result.post,
        'id':result.id
      }
    datas.append(data)
  return jsonify(datas)




@chap_link.route('/<int:id>/chapter/<int:page>', methods = ['GET'])
def book_chapters_chapter(id, page):
  # due to list indexing I remove one from page variable to get the right page
  page -=1
  results  = books.query.filter_by(id=id).first()
  result = results.chapters[page]
  data={'book name':results.name,
        'chapter':result.page,
        'post':result.post,
        'id':result.id
      }
  return jsonify(data)



@chap_link.route('/<int:id>/chapter/<int:page>/delete', methods = ['DELETE'])
def delete_chapter(id, page):
  # query for data through id
  result = books.query.filter_by(id=id).first()
  # if I'd doesn't exist
  if result == None:
    return {'message':str(id) + ' doesn\'t exist'}
  elif result.chapters == None:
    #if Id exists but chapter doesn't 
    return {'message':'no chapter found'}
  else:
    # reducing page because list start at 0 not 1
    page -=1
    #querying for id
    page_=result.chapters[page].id
    # querying the chapter data table with the ID of the book chapter
    chapter_result = chapter.query.filter_by(id=page_).first()
    db.session.delete(chapter_result)
    db.session.commit()
    return jsonify({'message':'deleted'})

@chap_link.route('/<int:id>/chapter/<int:page>/update', methods = ['POST'])
def update_chapter(id, page):
  result = books.query.filter_by(id=id).first()
  if result == None:
    return {'message':str(id) + ' doesn\'t exist'}
  elif result.chapters == None:
    return {'message':'no chapter found'}
  elif request.method == 'POST':
    page -=1
    chap=result.chapters[page].id
    if chap is not None:
      chap_query = chapter.query.filter_by(id =chap).first()
      if request.form.get('page') is not None:
        chap_query.name = request.form.get('page')
        db.session.commit()
      if request.form.get('post') is not None:
        chap_query.post = request.form.get('post')
        db.session.commit()
      return jsonify({'message':'book_updated'})
    else:
      return jsonify({'message':'book chapter does not exist'})




@chap_link.route('/<int:id>/chapter/add', methods = ['POST'])
def add_new_chapter(id):
  book = books.query.filter_by(id=id).first()
  if request.method == 'POST':
    # note when requesting from the form request for chapter with value as integer not page
    page = request.form.get('chapter')
    post = request.form.get('post')
  
    new = chapter(page=page,post=post,book=book)
    db.session.add(new)
    db.session.commit()
    return jsonify({'message':'new chapter added'})