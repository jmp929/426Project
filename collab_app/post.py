from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, json
)
from werkzeug.exceptions import abort
from collab_app.auth import login_required
from collab_app.db import get_db
from datetime import date
import datetime



bp = Blueprint('post', __name__)



@bp.route('/')
@bp.route('/<clss>')
def index(clss=None):

  if clss is not None:
    db = get_db()
    posts = db.execute(
    'SELECT p.id, title, created, author_id, first_name, last_name, description, start_time, location, type, p.class_id, c.name'
        ' FROM ((posts p JOIN user u ON p.author_id = u.id) JOIN classes c ON p.class_id=c.id)'
        ' WHERE c.name=?'
        ' ORDER BY created DESC', (clss,)
    ).fetchall()



    if g.user:
      db = get_db()
      classes = db.execute(
        'SELECT class_id FROM class_members WHERE member_id = ?', (g.user['id'],)
      ).fetchall()
    else:
      classes=[]

    return render_template('post/indexSearch.html', posts=posts, classes=classes, clss=clss)

  db = get_db()
  posts = db.execute(
    'SELECT p.id, title, created, author_id, first_name, last_name, description, start_time, location, type, p.class_id'
        ' FROM posts p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()


  if g.user:
    classes = db.execute(
      'SELECT class_id FROM class_members WHERE member_id = ?', (g.user['id'],)
    ).fetchall()
  else:
    classes=[]

  return render_template('post/index.html', posts=posts, classes=classes)

@bp.route('/<int:id>/profile')
@login_required
def profile(id):
  db = get_db()
  user_classes = db.execute(
    'SELECT *'
    ' FROM class_members cm JOIN classes c ON c.id=cm.class_id'
    ' WHERE cm.member_id=?', (id,)
  ).fetchall()

  user_events = db.execute(
    'SELECT p.id, title, created, p.author_id, first_name, last_name, description, start_time, location, type, p.class_id'
    ' FROM (event e JOIN posts p ON e.post_id=p.id) JOIN user u ON e.member_id=u.id' 
    ' WHERE e.member_id=?', (id,)
  ).fetchall()

  return render_template('post/profile.html', classes=user_classes, posts=user_events)

  

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():

  db = get_db()
  user_classes = db.execute(
    'SELECT c.name '
    ' FROM classes c JOIN  class_members cm ON c.id=cm.class_id'
    ' WHERE cm.member_id=?', (g.user['id'],)
  ).fetchall()

  if request.method == 'POST':

    title = request.form['title']
    clss = request.form['class']
    description = request.form['description']
    dt_str = str(request.form['datetime'])
    dt = datetime.datetime(*[int(v) for v in dt_str.replace('T', '-').replace(':', '-').split('-')])
    duration = request.form['duration']
    type_ = request.form['type']
    location = request.form['location']
    x_cord = request.form['x_cord']
    y_cord = request.form['y_cord']
    reason = request.form['reason']
    error = None
    duration = int(duration)

    if not title:
      error = 'Title is required.'
    elif not clss:
      error = 'Class is required.'
    if not description:
      error = 'Description is required.'
    elif not type_:
      error = 'Type is required.'
    elif not dt:
      error = 'Date and time is required.'
    elif not duration:
      error = 'duration is required.'
    elif duration <=  0:
      error = 'duration must be greater than zero.'
    if not location:
      error = 'Location is required.'
    elif not reason:
      error = 'Reason is required.'
    elif type_ != 'In Person' and type_ != "Zoom":
      error = "Incorrect meeting type"

    error = "Not registered in this class"
    for i in range(len(user_classes)):
      if clss ==  user_classes[i][0]:
        error = None
      

    if error is not None:
      flash(error)
    else:
      db = get_db()
      class_id = db.execute(
        'SELECT id FROM classes WHERE name=?',(clss,)
      ).fetchone()[0]
      db.execute(
      'INSERT INTO posts (title, author_id, class_id, description, type, reason, location, start_time, duration, x_cord, y_cord)'
      ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
      (title, g.user['id'], class_id, description, type_, reason, location, dt, duration, x_cord, y_cord)
      )
      post_id = db.execute(
        'SELECT id FROM posts WHERE author_id=? AND start_time=? AND class_id=?', (g.user['id'], dt, class_id)
      ).fetchone()[0]
      db.execute(
        'INSERT INTO event (author_id, class_id, member_id, post_id)'
        ' VALUES (?, ?, ?, ?)',
        (g.user['id'], class_id, g.user['id'], post_id)
      )
      db.commit()
      return redirect(url_for('post.index'))
    
    

  return render_template('post/create.html', classes=user_classes)

def get_post(id):
  
  post = get_db().execute(
      'SELECT p.id, p.author_id, p.class_id, p.title, c.name as name, p.description, p.type, p.reason, p.location, p.start_time, p.duration as duration'
      ' FROM (posts p JOIN user u ON p.author_id = u.id) z JOIN classes c ON c.id = z.class_id'
      ' WHERE p.id = ?',
      (id,)
  ).fetchone()
  if post is None:
      abort(404, "Post id {0} doesn't exist.".format(id))

  return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
      title = request.form['title']
      clss = request.form['class']
      description = request.form['description']
      dt_str = str(request.form['datetime'])
      dt = datetime.datetime(*[int(v) for v in dt_str.replace('T', '-').replace(':', '-').split('-')])
      duration = request.form['duration']
      type_ = request.form['type']
      location = request.form['location']
      x_cord = request.form['x_cord']
      y_cord = request.form['y_cord']
      reason = request.form['reason']

      db = get_db()
      user_classes = db.execute(
        'SELECT c.name '
        ' FROM classes c JOIN  class_members cm ON c.id=cm.class_id'
        ' WHERE cm.member_id=?', (g.user['id'],)
      ).fetchall()
      if not title:
        error = 'Title is required.'
      elif not clss:
        error = 'Class is required.'
      if not description:
        error = 'Description is required.'
      elif not type_:
        error = 'Type is required.'
      elif not dt:
        error = 'Date and time is required.'
      elif not duration:
        error = 'duration is required.'
      elif int(duration) <=  0:
        error = 'duration must be greater than zero.'
      if not location:
        error = 'Location is required.'
      elif not reason:
        error = 'Reason is required.'
      elif type_ != 'In Person' and type_ != "Zoom":
        error = "Incorrect meeting type"

      error = "Not registered in this class"
      for i in range(len(user_classes)):
        if clss ==  user_classes[i][0]:
          error = None

        if error is not None:
            flash(error)
        else:
            db = get_db()
            class_id = db.execute(
            'SELECT id FROM classes WHERE name=?',(clss,)
            ).fetchone()[0]
            db.execute(
                'UPDATE posts SET title = ?, class_id = ?, description = ?, type = ?, location = ?, reason = ?'
                ' WHERE id = ?',
                (title, class_id, description, type_, location, reason, id)
            )

            db.execute(
              'UPDATE event set author_id=?, class_id=?, member_id=?, post_id=?',
              (g.user['id'], class_id, g.user['id'], id)
            )
            db.commit()
            return redirect(url_for('post.index'))

    return render_template('post/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM posts WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('post.index'))


@bp.route('/<int:id>/info', methods=('GET', 'POST'))
def info(id):
  post = get_post(id)

  db = get_db()
  members = db.execute(
    'SELECT u.first_name, u.last_name, e.member_id'
    ' FROM event e JOIN user u ON e.member_id=u.id'
    ' WHERE e.post_id=?',(id,)
  ).fetchall()

  is_member = ["False"]
  mem = False
  for member in members:
    if g.user['id'] == member['member_id']:
      mem = True
      is_member = ["True"]

  if request.method == 'POST':
    if not mem:
      db.execute(
        'INSERT INTO event (class_id, post_id, member_id, author_id)'
        ' VALUES (?, ?, ?, ?)', (post['class_id'], post['id'], g.user['id'], post['author_id'])
      )
      db.commit()
      return redirect(url_for('post.index'))
    else:
      db.execute(
        'DELETE FROM event WHERE member_id=? AND post_id=?', (g.user['id'], post['id'])
      )
      db.commit()
      return redirect(url_for('post.index'))
  
  return render_template('post/info.html', post=post, members=members, test=is_member)

@bp.route('/getCoords/<clss>') 
@bp.route('/getCoords/') 
def get_coords(clss=None): 
  
  if clss is not None:
    db = get_db()
    coords = db.execute(
      'SELECT * FROM posts p JOIN classes c ON p.class_id=c.id WHERE c.name=? AND p.type=?', (clss, "In Person")
    ).fetchall()
    coords = [list(i) for i in coords]

    return json.jsonify({ 
        'posts': coords 
    })

  db = get_db()
  coords = db.execute(
    'SELECT * FROM posts WHERE type = ?', ("In Person",)
  ).fetchall()

  coords = [list(i) for i in coords]

  return json.jsonify({ 
      'posts': coords 
  })


@bp.route('/get_classes/<clss>') 
def get_classes(clss): 
  db = get_db()
  classes = db.execute(
    'SELECT name FROM classes WHERE name LIKE ? LIMIT 5', (clss+'%',)
  ).fetchall()
  classes = [list(i) for i in classes]

  return json.jsonify({ 
      'posts': classes 
  })

@bp.route('/getProfileCoords/<int:id>')
@login_required
def get_profile_coords(id): 
  db = get_db()
  coords = db.execute(
      'SELECT * FROM posts p JOIN event e ON p.id=e.post_id WHERE e.member_id=? AND p.type=?', (id, "In Person")
  ).fetchall()
  coords = [list(i) for i in coords]
  

  return json.jsonify({ 
      'posts': coords 
  })

@bp.route('/getUserId/<user>')
def get_user_id(user): 
  
  db = get_db()
  user_id = db.execute(
    'SELECT id FROM user WHERE user.username=?',(user,)
  ).fetchone()[0]
  

  return json.jsonify({ 
      'id': user_id 
  })



@bp.route('/getInfo/<int:post_id>')
def get_members_info(post_id):
  post = get_post(post_id)
  db = get_db()
  members = db.execute(
    'SELECT u.first_name, u.last_name, e.member_id'
    ' FROM event e JOIN user u ON e.member_id=u.id'
    ' WHERE e.post_id=?',(post_id,)
  ).fetchall()
  members = [list(i) for i in members]
 

  return json.jsonify({
      'members': members,
      'post': list(post)
  })



  