from .app import socketio

@socketio.on('my event')
def handle_my_custom_event(json):
	print('received json: ' + str(json))
	msg = json['data']
	msg = msg[::-1]
	emit('message', msg)

@socketio.on('connecting')
def initsession(name):
    print (name)
