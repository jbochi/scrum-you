from flask import Flask
app = Flask(__name__)

from datetime import datetime
import time

from flask import abort, redirect, render_template, request, url_for, \
                  flash, get_flashed_messages
from google.appengine.ext import db
from google.appengine.api import users


class Task(db.Model): 
    user = db.UserProperty()
    path = db.StringProperty()
    name = db.StringProperty(required=True)
    created_on = db.DateTimeProperty(auto_now_add=True)
    completed_on = db.DateTimeProperty()
    order = db.DateTimeProperty(auto_now_add=True)
    points = db.IntegerProperty(default=1)

    
@app.template_filter('epoch')
def epoch(value):
    if value:
        return int(time.mktime(value.timetuple())*1000)
    else:
        return None

@app.route('/')
def list():
    user = users.get_current_user()
    tasks = Task.all().filter('user =', user).order('order')
    return render_template('list.html', 
                           user=user, 
                           logout_url=users.create_logout_url("/"), 
                           tasks=tasks, 
                           flashes=get_flashed_messages());

@app.route('/', methods=['POST'])
def task_post():
    name = request.form['name']
    if not name:
        flash("Task name is mandatory.")
        return redirect(url_for('list'))
    task = Task(name = request.form['name'])
    task.user = users.get_current_user()
    task.put()
    return redirect(url_for('list'))

@app.route('/complete/', methods=['POST'])
def complete():
    id = int(request.form['id'])
    task = Task.get_by_id(id)
    if task and task.user == users.get_current_user():
        completed = request.form['completed']
        if completed == 'true':
            task.completed_on = datetime.now()
        else:
            task.completed_on = None
        task.save()
        return "1"
    else:
        abort(404)

@app.route('/edit/', methods=['POST'])
def edit():
    id = int(request.form['id'])
    task = Task.get_by_id(id)
    if task and task.user == users.get_current_user():
        name = request.form['name']
        if name:
            task.name = name
            task.save()
            return "1"
    else:
        abort(404)

@app.route('/update_order/', methods=['POST'])
def update_order():
    id = int(request.form['id'])
    task = Task.get_by_id(id)
    if task and task.user == users.get_current_user():
        order = request.form['order']
        task.order = datetime.fromtimestamp(long(order)/1000)
        task.save()
        return "1"
    else:
        abort(404)

@app.route('/delete/', methods=['POST'])
def delete():
    id = int(request.form['id'])
    task = Task.get_by_id(id)
    if task and task.user == users.get_current_user():
        task.delete()
        return "1"
    else:
        abort(404)

# set the secret key.  keep this really secret:
app.secret_key = 'the secret key'

if __name__ == '__main__':
    app.run(debug=True)
