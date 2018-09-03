from flask import Flask, session, redirect, url_for, escape, request
from flask import render_template
from DarkTowerWeb import darktower
from seckret_key import sk

def convert_str(string):
#removes apostrophes and upper case letters
#used to simplify user input
	lst = string.split("'")
	sumstr = ''
	for word in lst:
		sumstr += word
	return sumstr.lower()

application = Flask(__name__)

@application.route("/")
def index():
	#this is used to setup the session
	#with starting values
	session['room_name'] = darktower.START
	return redirect(url_for('game'))

@application.route('/game', methods = ['GET', 'POST'])
def game():
	#gets darktower.START and puts it into room_name
	room_name = session.get('room_name')
	if request.method == 'GET':
		if room_name:
			#returns the current room object and makes a page for it
			room = darktower.load_room(room_name)
			if room.room_type() == 'continue':
				#continue only has a continue button
				return render_template("continue_room.html", room=room)
			elif room.room_type() == 'yesno':
				#yesno pages have yes and no buttons
				return render_template("yn_room.html", room=room)
			elif room.room_type() == 'combat1':
				#combat1 rooms have buttons for all player moves
				#or a continue button is the player or enemy died
				return render_template("combat.html", room=room)
			elif room.room_type() == 'combat2':
				#combat2 rooms show the results of player and
				#enemy moves. These rooms have a continue button
				return render_template("combat2.html", room=room)
			else:
				#show_room s have an input field so the player can
				#type in an answer
				return render_template("show_room.html", room=room)

	else:
		#action is the input to the form if the method was POST
		action = request.form.get('action')
		#done to handle capitalizations by the user
		if type(action) == str:
			action = convert_str(action)

		if room_name and action:
			#load the current room given the stored name
			#and find the room that the inputted action lead to
			room = darktower.load_room(room_name)
			next_room = room.go(action)
			if not next_room:
				#if there is no room that corresponds to action, return the same room
				session['room_name'] = room.name_room()
			else:
				#if the action is valid, return the room the object links to
				session['room_name'] = next_room.name_room()
			return redirect(url_for('game'))
		elif room_name and not action:
			#if action isn't valid, return the same room
			room = darktower.load_room(room_name)
			session['room_name'] = room.name_room()
			return redirect(url_for('game'))
			
#CHANGE THIS IF YOU PUT THIS ON THE INTERNET
application.secret_key = sk

if __name__ == "__main__":
	application.run()
