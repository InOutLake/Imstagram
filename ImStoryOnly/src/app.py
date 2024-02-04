from flask import Flask, render_template, redirect, request, session, url_for
from urllib.parse import urlencode
from werkzeug.datastructures import ImmutableMultiDict
import requests
import pdb

app = Flask(__name__)
app.config['SECRET_KEY'] = 'c7359a4a-fa96-42ff-84aa-fe61bc8a3f24'
app_id = 1

app_request_base_url = 'http://oauth-client-app:8001'
server_request_base_url = 'http://oauth-server-app:8000'
app_base_url = 'http://localhost:8001'
server_base_url = 'http://localhost:8000'

@app.route('/')
def home():

    try : 
        a = session['token']
    except:
        return render_template('home.html')
    token = session['token']
    response = requests.get(f'{server_request_base_url}/dataprovider/provide_images_info/?token={token}')
    if not response.status_code == 200:
        return render_template('error.html', data=response.status_code)
    data = response.json()
    return render_template('stories.html', data=data)
    

@app.route('/authorize/')
def authenticate():
    data = {
        'client_id': app_id,
        'scope_name': 'Read',
        'redirect_uri': f"http://localhost:8001{url_for('oauth_callback')}"
    }
    return redirect(f'http://localhost:8000/oauth/authorize/' + '?' + urlencode(data))

@app.route('/authorize/oauth_callback/cb')
def oauth_callback():
    authorization_code = request.args.get('code', None)
    if not authorization_code:
        render_template('error.html', data='Login or password were incorrect')
    return get_token(authorization_code)

@app.route('/get_token/')
def get_token(authorization_code: str):
    data = {
        'client_id': app_id,
        'client_secret': app.secret_key,
        'scope_name': 'Read',
        'redirect_uri': app_request_base_url,
        'code': authorization_code,
    }
    response = requests.post(f'{server_request_base_url}/oauth/token/', json=data)
    if not response.status_code == 200:
        return render_template('error.html', data=response.status_code)
    data = response.json()
    session['token'] = data.get('token')
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8001)