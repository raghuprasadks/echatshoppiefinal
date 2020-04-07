from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_socketio import SocketIO
from db import get_user, save_user

app = Flask(__name__)
app.secret_key = "eshoppie2020"
socketio = SocketIO(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


@app.route('/')
def index():
    print('inside index')
    return render_template("index.html")


@app.route('/home')
def home():
    print('inside home')
    rooms = []
    #if current_user.is_authenticated():
    if current_user.is_authenticated:
        pass
        #rooms = get_rooms_for_user(current_user.username)
    return render_template("home.html", rooms=rooms)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    message = ''
    if request.method == 'POST':
        username = request.form.get('username')
        password_input = request.form.get('password')
        user = get_user(username)
        print('user :',user)
        #print('user name :',user.username)

        if user and user.check_password(password_input):
            login_user(user)
            return redirect(url_for('home'))
        else:
            message = 'Failed to login!'
    return render_template('login.html', message=message)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    message = ''
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        mobile = request.form.get('mobile')
        password = request.form.get('password')
        try:
            isUserPresent = save_user(username, email,mobile, password)
            print('isuser present ',isUserPresent)
            if (isUserPresent):
                message = "User already exists!"                
            else:
                return redirect(url_for('login'))
                
        except:
            print('exception ::')
            message = "User already exists!"
    return render_template('signup.html', message=message)


@app.route("/logout/")
@login_required
def logout():
    print('logout')
    logout_user()
    #return redirect(url_for('home'))
    return render_template("index.html")


@login_manager.user_loader
def load_user(username):
    return get_user(username)

'''
Anup code
'''

class WebSocketSender:

    ''' Wrap send_message with a class to use with watson.handle_conversation()
     '''

    def __init__(self):

        pass

    def send_message(self,message):
        ''' Function to send a message to the web ui via Flask Socket IO'''
        lines=message.split('\n')
        for line in lines:
            image = None





sender=WebSocketSender()

#We NEED user who logs in dynamically passed here..


'''
you have to use 
current_user.username to get the current user
'''


user={
 #   'name': 'shyam'
    'type':'customer'
}

@socketio.on('my_event',namespace=None)
def do_message(message):

    ''' this is the message from web ui user''' 
        
    if not watson:

        sender.send_message("Sorry. (failed to initialise)")

    elif message['data']:

        message=message['data']

        watson.handle_conversation(message,sender,user)

#we need user who logs in to be used here
        
'''
you have to use 
current_user.username to get the current user
'''

@socketio.on('connect',namespace=None)
def do_connect():
      
    print ("connected to db for every other user")

    print ("hello")

    pass


@socketio.on('disconnect',namespace=None)

def do_disconnect():
    '''On disconnect, '''
    
    pass
    print ('Client Disconnected')




if __name__ == '__main__':
    #watson=WatsonEnv.get_AMQ_online_store()
    watson=None
    socketio.run(app, debug=True)
