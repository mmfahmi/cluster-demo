from crypt import methods
from flask import Flask, jsonify, redirect, render_template, request, url_for, session
import requests
from gdrive.folderIndexing import folderIndexing
from gdrive.fileIndexing import list_files_efficiently
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google.auth.exceptions import RefreshError
import os
from dotenv import load_dotenv

load_dotenv()  # This will load environment variables from the .env file

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/getCredentials')
def needCredentials(access_token, refresh_token):
    try:
        credentials = Credentials(
            token=access_token,
            refresh_token=refresh_token,
            token_uri='https://oauth2.googleapis.com/token',
            client_id=os.getenv('GOOGLE_CLIENT_ID'),
            client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
            scopes=['https://www.googleapis.com/auth/drive','email']
        )
        return credentials
    except:
        return redirect(url_for('index'))


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index')
def Index():
    return render_template('index.html')

@app.route('/home')
def home():
    token_data = session.get('credentials')
    if token_data is None:
        return redirect(url_for('index'))
    return render_template('home.html')

@app.route('/home/list')
def table():
    token_data = session.get('credentials')
    if token_data is None:
        return redirect(url_for('index'))

    access_token = token_data.get('access_token')
    refresh_token = token_data.get('refresh_token')
    if access_token is None:
        return jsonify({'error': 'Access token is missing'})
    creds = needCredentials(access_token, refresh_token)
    try:
        service = build("drive", "v3", credentials=creds)
        folders = folderIndexing(service)
        return render_template('home.html', files=folders)
    except RefreshError as refresh_error:
        return redirect(url_for('login/google'))
    except HttpError as error:
        print(f"An error occurred: {error}")
        return jsonify({'error': 'Failed to list folders'})
    


@app.route('/files', methods=['GET', 'POST'])
def files():
    token_data = session.get('credentials')
    if token_data is None:
        return redirect(url_for('login'))

    access_token = token_data.get('access_token')
    refresh_token = token_data.get('refresh_token')
    if access_token is None:
        return jsonify({'error': 'Access token is missing'})
    creds = needCredentials(access_token, refresh_token)
    folder_name = request.args.get('folderName') if request.method == 'GET' else request.form['folderName']
    folder_id = request.args.get('folderId')
    service = build("drive", "v3", credentials=creds)
    files = list_files_efficiently(service, folder_id=folder_id)
    return render_template('files.html', folder_name=folder_name, files = files, 
    folder_id=folder_id)

@app.route('/files/list', methods=['GET'])
def cluster():
    token_data = session.get('credentials')
    if token_data is None:
        return redirect(url_for('login'))

    access_token = token_data.get('access_token')
    refresh_token = token_data.get('refresh_token')
    if access_token is None:
        return jsonify({'error': 'Access token is missing'})

    creds = needCredentials(access_token, refresh_token)
    
    folderNames = request.args.getlist('folderName')
    folderIds = request.args.getlist('folderId')
    
    if not folderIds:
        return jsonify({'error': 'No folder IDs provided'})
    try:
        service = build("drive", "v3", credentials=creds)
    except RefreshError as refresh_error:
        return redirect(url_for('login'))
    
    files = []
    for folder_id in folderIds:
        folder_files = list_files_efficiently(service, folder_id=folder_id)
        files.extend(folder_files)
    
    return render_template('files.html', folder_name=folderNames, files=files, folder_ids=folderIds)

@app.route('/login/google')
def login():
    client_id = os.getenv('GOOGLE_CLIENT_ID')
    redirect_uri = 'http://localhost:5000/login/callback'
    scopes = [
        'https://www.googleapis.com/auth/drive',
        'email'
    ]
    scope = ' '.join(scopes)
    auth_url = f'https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope={scope}'
    return redirect(auth_url)

@app.route('/login/callback')
def login_callback():
    code = request.args.get('code')
    token_url = 'https://oauth2.googleapis.com/token'
    client_id = os.getenv('GOOGLE_CLIENT_ID')
    client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
    redirect_uri = 'http://localhost:5000/login/callback'

    params = {
        'code': code,
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code'
    }

    response = requests.post(token_url, data=params)
    token_data = response.json()

    if 'error' in token_data:
        return jsonify(token_data)

    session['credentials'] = token_data

    # Optionally, retrieve user info and store in session
    user_info_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    headers = {'Authorization': f"Bearer {token_data['access_token']}"}
    user_info = requests.get(user_info_url, headers=headers).json()
    session['user_email'] = user_info.get('email')

    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    token_data = session.get('credentials')
    if token_data:
        access_token = token_data.get('access_token')
        revoke_url = f'https://oauth2.googleapis.com/revoke?token={access_token}'
        response = requests.post(revoke_url)
        
        if response.status_code == 200:
            session.clear()
            return redirect(url_for('index'))
        else:
            return jsonify({'error': 'Failed to revoke token'}), 400
    session.clear()
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
