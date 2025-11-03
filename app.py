from flask import Flask, request, redirect, url_for, render_template_string, flash
from werkzeug.security import generate_password_hash
from markupsafe import escape

app = Flask(__name__)
app.secret_key = "dev-secret-change-me"  # mijn geheime sleutel (voor flash berichten)

# tijdelijke opslag voor gebruikers (ik gebruik geen echte database)
users_db = {}

# --- HTML pagina met formulier ---
PAGE = """
<!doctype html>
<html lang="nl">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width,initial-scale=1" />
    <title>SVI Bank — Account aanmaken</title>
    <style>
      :root{--pink:#ec189a;--text:#111;--muted:#6b7280}
      *{box-sizing:border-box}
      body{margin:0;font-family:system-ui,-apple-system,Segoe UI,Roboto,Arial;background:#f6f7f9;color:var(--text)}
      .wrap{max-width:420px;margin:40px auto;background:#fff;border:1px solid #e5e7eb;border-radius:12px;padding:24px}
      h1{margin:0 0 16px;font-size:24px}
      form{display:grid;gap:12px}
      input{padding:12px 14px;border:2px solid #e5e7eb;border-radius:8px;font-size:16px}
      input:focus{outline:none;border-color:var(--pink)}
      .btn{border:0;padding:12px 16px;border-radius:8px;background:var(--pink);color:#fff;font-weight:700;cursor:pointer}
      .helper{margin-top:8px;color:var(--muted);font-size:14px}
      .messages{list-style:none;margin:8px 0 0;padding:0}
      .messages li{background:#fff3f6;color:#9b0d5a;border:1px solid #ffcde0;padding:10px 12px;border-radius:8px;margin-top:6px}
    </style>
  </head>
  <body>
    <div class="wrap">
      <h1>Account aanmaken</h1>

      {% with msgs = get_flashed_messages() %}
        {% if msgs %}
          <ul class="messages">
            {% for m in msgs %}<li>{{ m }}</li>{% endfor %}
          </ul>
        {% endif %}
      {% endwith %}

      <form method="post" action="{{ url_for('register') }}" novalidate>
        <input type="text"     name="username" placeholder="Gebruikersnaam"  value="{{ request.form.get('username','') }}" required />
        <input type="email"    name="email"    placeholder="E-mailadres"     value="{{ request.form.get('email','') }}" required />
        <input type="password" name="password" placeholder="Wachtwoord" required />
        <input type="password" name="confirm"  placeholder="Wachtwoord herhalen" required />
        <button class="btn" type="submit">Aanmaken</button>
      </form>

      <p class="helper">Heb je al een account? <a href="#">Inloggen</a></p>
    </div>
  </body>
</html>
"""

# --- succes pagina ---
SUCCESS_PAGE = """
<!doctype html>
<html lang="nl">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width,initial-scale=1" />
    <title>SVI Bank — Succes</title>
    <style>
      body{font-family:system-ui,-apple-system,Segoe UI,Roboto,Arial;margin:0;display:grid;place-items:center;min-height:100vh;background:#f6f7f9}
      .card{background:#fff;border:1px solid #e5e7eb;border-radius:12px;padding:28px;max-width:420px}
      h2{margin:0 0 10px}
      a{display:inline-block;margin-top:12px;text-decoration:none;color:#ec189a;font-weight:700}
      .muted{color:#6b7280}
    </style>
  </head>
  <body>
    <div class="card">
      <h2>Account is aangemaakt 🎉</h2>
      <p class="muted">
        Gebruikersnaam: <strong>{{ username }}</strong><br/>
        E-mail: <strong>{{ email }}</strong>
      </p>
      <a href="{{ url_for('register') }}">Nog een account aanmaken</a>
    </div>
  </body>
</html>
"""

def validate_form(username: str, email: str, password: str, confirm: str):
    # ik controleer of de velden correct zijn ingevuld
    errors = []

    if not username or len(username) < 3:
        errors.append("Gebruikersnaam moet minstens 3 tekens zijn.")
    if "@" not in email or "." not in email:
        errors.append("Voer een geldig e-mailadres in.")
    if len(password) < 6:
        errors.append("Wachtwoord moet minstens 6 tekens zijn.")
    if password != confirm:
        errors.append("Wachtwoorden komen niet overeen.")
    if username in users_db:
        errors.append("Gebruikersnaam is al in gebruik.")

    return errors

@app.route("/", methods=["GET"])
def home():
    # gewoon doorsturen naar /register
    return redirect(url_for("register"))

@app.route("/register", methods=["GET", "POST"])
def register():
    # als de gebruiker op de knop klikt (POST)
    if request.method == "POST":
        username = escape(request.form.get("username", "")).strip()
        email    = escape(request.form.get("email", "")).strip()
        password = request.form.get("password", "")
        confirm  = request.form.get("confirm", "")

        # eerst checken of het formulier klopt
        errs = validate_form(username, email, password, confirm)
        if errs:
            for e in errs:
                flash(e)  # foutmelding tonen
            return render_template_string(PAGE)

        # gebruiker opslaan met een gehasht wachtwoord
        users_db[username] = {
            "email": email,
            "password_hash": generate_password_hash(password)
        }

        # laat succes pagina zien
        return render_template_string(SUCCESS_PAGE, username=username, email=email)

    # bij GET gewoon formulier tonen
    return render_template_string(PAGE)

if __name__ == "__main__":
    app.run(debug=True)  # debug aan voor ontwikkeling
