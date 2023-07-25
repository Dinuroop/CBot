from flask import Flask,request,render_template,jsonify,flash,redirect,request, session, abort, url_for
import flask
import json
import requests
from flask_cors import CORS
import openai
import config

app = Flask(__name__)
CORS(app)
app.secret_key = config.SECRET_KEY

# Firebase configuration
firebase_api_key = config.FIREBASE_API_KEY
firebase_auth_domain = config.FIREBASE_AUTH_DOMAIN
firebase_database_url = config.FIREBASE_DATABASE_URL


@app.route("/",methods=["GET","POST"])
def login():
    if request.method == 'POST':
        result = request.form           #Get the data
        email = result["email"]
        password = result["pass"]
        # Login using Firebase REST API
        login_url = f"https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key={firebase_api_key}"
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
        response = requests.post(login_url, json=payload)

        if response.ok:
            # Log in successful, store user's idToken in session for future authentication
            session['user_idToken'] = response.json().get('idToken', '')
            return redirect('/chatbot')
        else:
            message = 'Invalid credentials. Please try again.'
            return render_template('login.html', message=message)

    return render_template('login.html')

@app.route("/signup",methods=["GET","POST"])
def signup():
    return render_template('signup.html')

@app.route("/register",methods=["GET","POST"])
def register():
     if request.method == 'POST':
        result = request.form           #Get the data
        email = result["email"]
        password = result["pass"]
        # Signup using Firebase REST API
        signup_url = f"https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key={firebase_api_key}"
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
        response = requests.post(signup_url, json=payload)

        if response.ok:
            # User created successfully, you can do additional tasks here
            # For example, store additional user data in the Firebase database
            return redirect('/')
        else:
            message = 'An error occurred: ' + response.json().get('error', {}).get('message', '')
            return render_template('signup.html', message=message)

openai.api_key = config.OPENAI_API_KEY
def askGPT(text):
    response = openai.Completion.create(
        engine="davinci-instruct-beta-v3",
        prompt=text,
        temperature=0.6,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].text


@app.route("/chatbot",methods=["GET","POST"])
def users():
    user_idToken = session.get('user_idToken', None)
    if user_idToken:
        # User authenticated, you can fetch additional user data here if needed
        if request.method == "POST":
            data=request.get_json()
            ans = askGPT(data["message"])
            print(ans)
            return jsonify({"answer":ans})
        return render_template('base.html')
    else:
        return redirect('/')
    
@app.route("/logout")
def logOut():
    session.pop('user_idToken', None)
    return redirect('/')


if __name__ == "__main__":
    app.run("0.0.0.0",6969)
