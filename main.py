from flask import Flask, request, redirect, jsonify
import requests

app = Flask(__name__)

CLIENT_ID = "1457002138868777163"
CLIENT_SECRET = "6ETxm64ga7P7ZPtKpWIEShYtXyyaykcI"
REDIRECT_URI = "https://andoficial.github.io/112-valencia/callback"


@app.route("/auth/discord")
def discord_auth():

    code = request.args.get("code")
    if not code:
        return "No se recibió ningún code", 400

    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "scope": "identify"
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    token = requests.post(
        "https://discord.com/api/oauth2/token",
        data=data,
        headers=headers
    ).json()

    if "access_token" not in token:
        return jsonify(token), 400

    user = requests.get(
        "https://discord.com/api/users/@me",
        headers={"Authorization": f"Bearer {token['access_token']}"}
    ).json()

    return jsonify(user)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
