from flask import Flask, render_template, current_app, redirect, url_for, session
from flask_socketio import SocketIO, emit, join_room, leave_room
from forms import LoginForm
import json

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
	return current_app.send_static_file('index.html')

@app.route('/p2p', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		session['name'] = form.name.data
		session['room'] = 1
		return redirect(url_for('.chat'))
	form.name.data = session.get('name')
	return render_template('index.html', form=form)
	#return current_app.send_static_file('login.html')

@app.route('/chat')
def chat():
	name = session.get('name', '')
	room = session.get('room', '')
	print (name, room)
	if name == '' or room == '':
		return redirect(url_for('.index'))
	return render_template('chat.html', name=name, room=room)

@socketio.on('my event')
def handle_my_custom_event(json):
	print('received json: ' + str(json))
	msg = json['data']
	msg = msg[::-1]
	emit('message', msg)

@socketio.on('joined')
def initchat():
	room = session.get('room')
	join_room(room)
	res = {}
	res['msg'] = ' has entered the room.'
	res['sender'] = session.get('name')
	emit('connected', str(json.dumps(res)), room=room)
	emit('status', str(json.dumps(res)), room=room)

@socketio.on('outgoing')
def newsent(data):
	room = session.get('room')
	res = {}
	res['msg'] = data['msg']
	res['sender'] = session.get('name')
	print (res)
	emit('incoming', str(json.dumps(res)), room=room)

@socketio.on('exit')
def exiting():
	room = session.get('room')
	res = {}
	res['sender'] = session.get('name')
	res['url'] = url_for('.login')
	emit('close', str(json.dumps(res)), room=room)
	res['msg'] = ' has left the room'
	emit('status', str(json.dumps(res)), room=room)
	leave_room(room)

if __name__ == '__main__':
    socketio.run(app)
