import functools
from flask import (
  Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from collab_app.db import get_db
import sys

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
  if request.method == 'POST':
    email = request.form['email']
    username = request.form['user']
    password = request.form['password']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    class1 = request.form['class1']
    class2 = request.form['class2']
    class3 = request.form['class3']
    class4 = request.form['class4']
    class5 = request.form['class5']
    class6 = request.form['class6']
    class7 = request.form['class7']
    db = get_db()
    error = None
    email_end = email[-7:]

    class_list = [
      class1,
      class2,
      class3,
      class4,
      class5,
      class6,
      class7,
    ]

    if not username:
      error = 'Username is required.'
    elif not password:
      error = 'Password is required.'
    elif not email:
      error = 'Email is required.'
    elif email_end != 'unc.edu':
      error = 'Must be UNC email'
    elif db.execute(
      'SELECT id FROM user WHERE username = ?', (username,)
    ).fetchone() is not None:
      error = 'User {} is already registered.'.format(username)
    elif db.execute(
      'SELECT id FROM user WHERE email = ?', (email,)
    ).fetchone() is not None:
      error = 'Email {} is already registered.'.format(email)
    elif class1 == '' and class2 == '' and class3 == '' and class4 == '' and class5 == '' and class6 == '' and class7 == '':
      error = 'Must be  registered in at least one class'

    if error is None:
      db.execute(
        'INSERT INTO user (username, email, password, first_name, last_name) VALUES (?, ?, ?, ?, ?)',
        (username, email, generate_password_hash(password), first_name, last_name)
      )
      db.commit()
      for clss in class_list:
        if clss != "":
          
          class_id = db.execute(
          'SELECT id FROM classes WHERE name=?', (clss,)
          ).fetchone()

          if class_id is None:
            db.execute(
              'INSERT INTO classes (name) VALUES (?)', (clss,)
            )
            db.commit()
            db = get_db()

            class_id = db.execute(
            'SELECT id FROM classes WHERE name=?', (clss,)
            ).fetchone()

          user_id = db.execute(
            'SELECT id FROM user WHERE email=?', (email,)
          ).fetchone()
         

          db.execute(
            'INSERT INTO class_members (member_id, class_id) VALUES (?, ?)',
            (user_id[0], class_id[0],)
          )
          db.commit()

      return redirect(url_for('auth.login'))
    flash(error)

  return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    db = get_db()
    error = None
    user = db.execute(
      'SELECT * FROM user WHERE username = ?', (username,)
    ).fetchone()

    if user is None:
      error = 'Incorrect Username.'
    elif not check_password_hash(user['password'], password):
      error = 'Incorrect Password'

    if error is None:
      session.clear()
      session['user_id'] = user['id']
      return redirect(url_for('index'))
    
    flash(error)

  return render_template('auth/login.html')

@bp.route('/logout')
def logout():
  session.clear()
  return redirect(url_for('index'))

@bp.before_app_request
def load_logged_in_user():
  user_id = session.get('user_id')

  if user_id is None:
    g.user = None
  else:
    g.user = get_db().execute(
      'SELECT * FROM user WHERE id = ?', (user_id,)
    ).fetchone()

def login_required(view):
  @functools.wraps(view)
  def wrapped_view(**kwargs):
    if g.user is None:
      return redirect(url_for('auth.login'))
    
    return view(**kwargs)
  
  return wrapped_view