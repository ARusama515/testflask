import asyncio
import websockets
import json
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import threading

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# In-memory user storage (replace with database in production)
users = {}

DEEPGRAM_API_KEY = 'your_deepgram_api_key'

async def deepgram_connection(websocket, path):
    # Connect to Deepgram Voice Agent WebSocket
    async with websockets.connect(f"wss://agent.deepgram.com/agent?access_token={DEEPGRAM_API_KEY}") as deepgram_socket:
        while True:
            try:
                audio_chunk = await websocket.recv()
                # Forward the audio to Deepgram
                await deepgram_socket.send(audio_chunk)
                
                # Receive the response from Deepgram (audio + text)
                response = await deepgram_socket.recv()
                
                # Send the response back to the client
                await websocket.send(response)
            except Exception as e:
                print("Error in WebSocket communication:", e)
                break

# WebSocket route for handling audio
@app.route('/audio', methods=['GET'])
def audio():
    # Start a background thread to handle the WebSocket connection
    thread = threading.Thread(target=asyncio.run, args=(deepgram_connection(websocket, path),))
    thread.start()
    return jsonify({"message": "WebSocket connection established."})

@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html')
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
    app.run(host='0.0.0.0', port=5000, debug=True)
