from flask import Flask, request, redirect, jsonify
import requests

app = Flask(__name__)

CLIENT_ID = "1457002138868777163"
CLIENT_SECRET = "6ETxm64ga7P7ZPtKpWIEShYtXyyaykcI"
REDIRECT_URI = "https://andoficial.github.io/112-valencia/"


@app.route("/")
def home():
    return "Todo OK 😎 — Backend funcionando"


@app.route("/auth/discord")
def discord_auth():
    code = request.args.get("code")

    if not code:
        return "No se recibió ningún code", 400

    # Intercambiar el code por un access token
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "scope": "identify"
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    token_response = requests.post(
        "https://discord.com/api/oauth2/token",
        data=data,
        headers=headers
    )

    token = token_response.json()

    if "access_token" not in token:
        return jsonify(token), 400

    access_token = token["access_token"]

    # Obtener datos del usuario
    user = requests.get(
        "https://discord.com/api/users/@me",
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    ).json()

    return jsonify(user)


if __name__ == "__main__":
    # Render te da el puerto en la variable PORT
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
