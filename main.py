import os
from flask import Flask, request, redirect
import requests
import urllib.parse

app = Flask(__name__)

# ================== CONFIGURACIÓN ==================
CLIENT_ID = "1457002138868777163"
CLIENT_SECRET = "6ETxm64ga7P7ZPtKpWIEShYtXyyaykcI"
REDIRECT_URI = "https://andoficial.github.io/112-valencia/callback"

# URL de tu dashboard en GitHub Pages donde recibirás los datos
FRONTEND_URL = "https://andoficial.github.io/112-valencia/dashboard.html"
# ====================================================

@app.route("/")
def home():
    return "Todo OK 😎 — Backend funcionando"


@app.route("/auth/discord")
def discord_auth():
    # 1️⃣ Recoger el "code" que manda Discord
    code = request.args.get("code")
    if not code:
        return "No se recibió ningún code", 400

    # 2️⃣ Intercambiar el code por un access_token
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "scope": "identify"
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    token_response = requests.post(
        "https://discord.com/api/oauth2/token",
        data=data,
        headers=headers
    )

    token = token_response.json()
    if "access_token" not in token:
        return f"Error obteniendo token: {token}", 400

    access_token = token["access_token"]

    # 3️⃣ Obtener los datos del usuario
    user = requests.get(
        "https://discord.com/api/users/@me",
        headers={"Authorization": f"Bearer {access_token}"}
    ).json()

    # 4️⃣ Redirigir al frontend con los datos como query params
    params = {
        "id": user.get("id"),
        "username": user.get("username"),
        "discriminator": user.get("discriminator"),
        "avatar": user.get("avatar")
    }

    query_string = urllib.parse.urlencode(params)
    return redirect(f"{FRONTEND_URL}?{query_string}")


if __name__ == "__main__":
    # Render asigna el puerto en la variable PORT
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)="0.0.0.0", port=port)
