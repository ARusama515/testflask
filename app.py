from flask_socketio import SocketIO, emit
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import asyncio
import websockets
import os

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default_secret_key')
socketio = SocketIO(app, cors_allowed_origins="*")

# In-memory user storage (replace with database in production)
users = {}

DEEPGRAM_API_KEY = os.getenv('DEEPGRAM_API_KEY', 'your_deepgram_api_key')

@socketio.on('start_audio_stream')
async def handle_audio_stream(data):
    try:
        # Connect to Deepgram WebSocket
        async with websockets.connect(f"wss://agent.deepgram.com/agent?access_token={DEEPGRAM_API_KEY}") as dg_socket:
            # Send audio data to Deepgram
            await dg_socket.send(data['audio_chunk'])
            
            # Receive response from Deepgram
            response = await dg_socket.recv()
            
            # Send response back to the browser
            emit('agent_response', {'response': response})
    except Exception as e:
        emit('error', {'message': f"Error in WebSocket communication: {str(e)}"})
        print("Error in WebSocket communication:", e)

@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/profile')
def profile():
    if 'username' in session:
        return jsonify({'username': session['username'], 'message': 'Welcome to your profile!'})
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users:
            flash('Username already exists!')
            return redirect(url_for('register'))
        
        users[username] = password
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username not in users or users[username] != password:
            flash('Invalid username or password!')
            return redirect(url_for('login'))
        
        session['username'] = username
        flash('Login successful!')
        return redirect(url_for('home'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.')
    return redirect(url_for('home'))

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
