from flask import Flask, render_template, send_from_directory  # ~/$ pip install flask
from flask_socketio import SocketIO, send, emit #~/$ pip install flask-socketio
from datetime import timedelta
import json
import time
import threading

app = Flask(__name__)
#app.config["SEND_FILE_MAX_AGE_DEFAULT"] = timedelta(seconds=1) # DEBUG ONLY - avoid cached shite confusion during development
# app.config["SECRET_KEY"] = 'secrets!'
sio = SocketIO(app)

class LData:
	def __init__( self,
	depth = 0.0,
	tension = 0.0,
	speed = 0.0,
	ccl = 0.0,
	gr = 0.0,
	temp = 0.0,
	press = 0.0,
	flowUp = 0.0,
	flowDn = 0.0,
	diffPress = 0.0,
	spinner = 0.0
	):
		self.depth = depth
		self.tension = tension
		self.speed = speed
		self.ccl = ccl
		self.gr = gr
		self.temp = temp
		self.press = press
		self.flowUp = flowUp
		self.flowDn = flowDn
		self.diffPress = diffPress
		self.spinner = spinner

def sendsimdata( ):
	f = open("pl-data-long.txt", "r")
	f.readline()
	count = 0
	for line in f:
		l = str(line.encode('utf-8').strip()).split("'")[1]
		d = LData( )
		d.depth = float(l.split()[0])
		d.tension =	float(l.split()[1])
		d.speed	= float(l.split()[2])
		d.ccl =	float(l.split()[3])
		d.gr =	float(l.split()[4])
		d.temp =	float(l.split()[5])
		d.press =	float(l.split()[6])
		d.flowUp =	float(l.split()[7])
		d.flowDn =	float(l.split()[8])
		d.diffPress = float(l.split()[9])
		d.spinner =	float(l.split()[10])
		djson= json.dumps(d.__dict__)
		# print(djson)
		emit('newdata', djson )
		time.sleep(0.05)
		count += 1
	f.close()
	print(f'\n[*** SENT DATA ***]\t {count} samples @ 20 / second...\n')

@sio.on('getsimdata')
def handle_getsimdata( msg ):
	print(f'\n[*** DATA REQUESTED ***]\n{ msg }\n')
	x = threading.Thread(target=sendsimdata( ))
	x.start()
	x.join()

# route to svelte page
@app.route("/")
def base():
	return send_from_directory('client/public', 'index.html')

# route to static files for svelte page (compiled js, css, media...)
@app.route('/<path:path>')
def home(path):
	return send_from_directory('client/public', path)

@app.route("/data")
def datago( ):
	f = open("pl-data-short.txt", "r")
	f.readline()
	l = str(f.readline().encode('utf-8').strip()).split("'")[1]
	data = LData(
		float(l.split()[0]),	#depth
		float(l.split()[1]),	# tension
		float(l.split()[2]),	#speed
		float(l.split()[3]),	#ccl
		float(l.split()[4]),	# gr
		float(l.split()[5]),	# temp
		float(l.split()[6]),	#press
		float(l.split()[7]),	#flowUp
		float(l.split()[8]),	# flowDn
		float(l.split()[9]),	# diffPress
		float(l.split()[10])	#spinner
	)
	print(data.__dict__)
	f.close()
	return render_template("data.html", data=data, title='Data')

if __name__ == "__main__":
	sio.run(app)

### Go Buttons ##
# ~/ $ source bin/activate
# ~/ $ cd src
# ~/src $ export FLASK_APP=app.py
# ~/src $ flask run

# 31-Jan-2021 - Added svelte
# https://cabreraalex.medium.com/svelte-js-flask-combining-svelte-with-a-simple-backend-server-d1bc46190ab9
# ~/src $ npx degit svelte/template client
# ~/src $ cd client
# ~/src/client $ npm install
# ~/src/client $ npm run build  (when changes are made to the svelte files)

# 31-Jan-2021 - Added svelte-speedometer
# https://www.npmjs.com/package/svelte-speedometer
# ~/src/client $ npm install svelte-speedometer
