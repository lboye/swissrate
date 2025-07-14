import os
import sys
import subprocess
import json

base_dir = os.path.abspath(os.path.dirname(__file__))

def pip_install(pkg):
    try:
        __import__(pkg)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

print("Vérification/installation de Flask...")
pip_install("flask")
from flask import Flask

# 1. Dossiers
folders = [
    "static/assets/logos",
    "templates"
]
for folder in folders:
    path = os.path.join(base_dir, folder)
    os.makedirs(path, exist_ok=True)
print("Dossiers créés/présents.")

# 2. companies.json
companies_json = os.path.join(base_dir, "companies.json")
if not os.path.exists(companies_json):
    with open(companies_json, "w", encoding="utf-8") as f:
        json.dump([], f)
    print("Fichier companies.json créé.")

# 3. style.css
css_path = os.path.join(base_dir, "static/assets/style.css")
if not os.path.exists(css_path):
    with open(css_path, "w", encoding="utf-8") as f:
        f.write("""
body {font-family:'Segoe UI',Arial,sans-serif;background:#f7f8fa;margin:0;}
.navbar {display:flex;align-items:center;justify-content:space-between;padding:0.85rem 2.1rem;background:#fff;border-bottom:1.5px solid #e4e9ec;}
.logo{font-weight:900;font-size:1.44rem;color:#e63946;}
.logo span{color:#191919;}
.navbar-center a,.navbar-right a{margin:0 0.8rem;text-decoration:none;color:#222;font-weight:500;}
.navbar-center a.active{color:#e63946;}
.navbar-right .search-bar{padding:0.35rem 0.8rem;border-radius:8px;border:1.2px solid #e0e5e9;margin-right:0.7rem;}
.container{max-width:1240px;margin:0 auto;padding:0 1.5rem;}
.footer{margin-top:3.8rem;padding:1.25rem 0;text-align:center;color:#777;font-size:0.98rem;}
.flashes{list-style:none;margin:0 0 1rem 0;padding:0;}
.flashes li{padding:0.6em 1.2em;border-radius:6px;font-weight:500;}
.flashes .success{background:#d9fbe4;color:#16531b;border:1.3px solid #99e7b2;}
.flashes .error{background:#ffe2e2;color:#9b2226;border:1.3px solid #ee8989;}
        """)
    print("Feuille de style CSS créée.")

# 4. app.py
app_path = os.path.join(base_dir, "app.py")
if not os.path.exists(app_path):
    with open(app_path, "w", encoding="utf-8") as f:
        f.write("""
import os
import json
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/assets/logos/'
COMPANIES_JSON = 'companies.json'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'svg', 'webp'}

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_companies():
    if not os.path.exists(COMPANIES_JSON):
        return []
    with open(COMPANIES_JSON, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_companies(companies):
    with open(COMPANIES_JSON, 'w', encoding='utf-8') as f:
        json.dump(companies, f, indent=2, ensure_ascii=False)

@app.route('/')
def index():
    companies = load_companies()
    return render_template('index.html', companies=companies)

@app.route('/add-company', methods=['GET', 'POST'])
def add_company():
    if request.method == 'POST':
        name = request.form.get('company-name', '').strip()
        website = request.form.get('company-website', '').strip()
        logo = request.files.get('company-logo')

        if not name or not website or not logo or logo.filename == '':
            flash("Tous les champs sont obligatoires, logo compris.", 'error')
            return redirect(url_for('add_company'))

        if not allowed_file(logo.filename):
            flash("Format de logo non autorisé.", 'error')
            return redirect(url_for('add_company'))

        logo_filename = secure_filename(name.lower().replace(' ', '_') + '.' + logo.filename.rsplit('.', 1)[1].lower())
        logo.save(os.path.join(app.config['UPLOAD_FOLDER'], logo_filename))

        companies = load_companies()
        if any(c['name'].lower() == name.lower() for c in companies):
            flash("Cette société existe déjà.", 'error')
            return redirect(url_for('add_company'))

        score = 4.00
        new_company = {
            "name": name,
            "website": website,
            "logo": logo_filename,
            "score": score
        }
        companies.append(new_company)
        save_companies(companies)

        generate_company_page(new_company)
        flash("Société ajoutée avec succès !", 'success')
        return redirect(url_for('index'))
    return render_template('add-company.html')

def generate_company_page(company):
    template = '''<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <title>{name} – SwissRate</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="../static/assets/style.css">
</head>
<body>
  <nav class="navbar container">
    <div class="navbar-left">
      <span class="logo"><span>Swiss</span>Rate</span>
    </div>
    <div class="navbar-center">
      <a href="../index.html">Accueil</a>
      <a href="../about.html">À propos</a>
      <a href="../legal.html">CGU</a>
      <a href="../contact.html">Contact</a>
      <a href="../add-company.html">Ajouter une société</a>
    </div>
    <div class="navbar-right">
      <input class="search-bar" type="search" placeholder="Rechercher…">
      <a class="login-btn" href="../login.html">Login</a>
    </div>
  </nav>
  <div class="container">
    <div style="display:flex;align-items:center;gap:2rem;margin:2.2rem 0;">
      <img class="company-logo" src="../static/assets/logos/{logo}" alt="Logo {name}">
      <div>
        <div class="company-name" style="font-size:2rem;font-weight:700;">{name}</div>
        <div class="company-rating" style="font-size:1.3rem;">
          {score} <span class="star" style="color:#ffb800;font-size:1.3rem;">⭐️</span>
        </div>
        <div style="margin-top:1.5rem;font-size:1.12rem;">
          <a href="{website}" target="_blank" rel="noopener">Visiter le site officiel</a>
        </div>
      </div>
    </div>
    <div style="margin-top:2.5rem;color:#333;">Page de présentation de l'entreprise {name}.<br>À compléter…</div>
  </div>
  <div class="footer">
    &copy; 2025 SwissRate | <a href="../legal.html">CGU</a> | <a href="../about.html">À propos</a> | <a href="../contact.html">Contact</a>
  </div>
</body>
</html>
'''
    fname = f"company-{company['name'].lower().replace(' ', '_')}.html"
    filepath = os.path.join("templates", fname)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(template.format(
            name=company['name'],
            logo=company['logo'],
            score=company['score'],
            website=company['website']
        ))

@app.route('/templates/<filename>')
def company_file(filename):
    return send_from_directory('templates', filename)

if __name__ == '__main__':
    app.run(debug=True)
        """)
    print("Backend app.py créé.")

# 5. index.html (Jinja2-ready)
index_html_path = os.path.join(base_dir, "templates/index.html")
if not os.path.exists(index_html_path):
    with open(index_html_path, "w", encoding="utf-8") as f:
        f.write("""
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <title>SwissRate</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="static/assets/style.css">
  <style>
    .company-logo { height: 34px; max-width: 90%; object-fit: contain; display: block; margin-left: auto; margin-right: auto; }
    .star { color: #ffb800; font-size: 1.13rem; margin-left: 0.15rem; vertical-align: middle; }
    .company-rating { font-size: 1.13rem; font-weight: 500; color: #222; display: flex; align-items: center; justify-content: center; gap: 0.15rem; }
    .company-card { background: #fff; border: 1.5px solid #eee; border-radius: 14px; box-shadow: 0 1px 8px 0 rgba(36,37,38,0.04); padding: 1.35rem 1rem 1rem 1rem; text-align: center; cursor: pointer; transition: box-shadow .18s, border-color .16s;}
    .company-card:hover { border-color: #e63946; box-shadow: 0 6px 16px 0 rgba(230,57,70,0.08);}
    .company-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1.35rem; margin-top: 2.7rem;}
    .company-name { font-size: 1.09rem; font-weight: 600; margin-bottom: 0.4rem; color: #191919; letter-spacing: 0.2px;}
    @media (max-width: 800px) { .company-grid { grid-template-columns: repeat(auto-fit, minmax(155px, 1fr)); gap: 0.65rem;} .company-card { padding: 0.7rem 0.3rem 0.7rem 0.3rem;} .company-logo { height: 24px; margin-bottom: 0.6rem;} .company-name { font-size: 0.97rem;}}
  </style>
</head>
<body>
  <nav class="navbar container">
    <div class="navbar-left">
      <span class="logo"><span>Swiss</span>Rate</span>
    </div>
    <div class="navbar-center">
      <a href="index.html" class="active">Accueil</a>
      <a href="about.html">À propos</a>
      <a href="legal.html">CGU</a>
      <a href="contact.html">Contact</a>
      <a href="add-company.html">Ajouter une société</a>
    </div>
    <div class="navbar-right">
      <input class="search-bar" type="search" placeholder="Rechercher…">
      <a class="login-btn" href="login.html">Login</a>
    </div>
  </nav>
  <div class="container">
    <h1 style="margin-top:2.5rem;">SwissRate</h1>
    <p>Explorez et comparez la réputation de toutes les entreprises suisses. Faites défiler pour découvrir plus de sociétés :</p>
    <div class="company-grid">
      {% for company in companies %}
        <a href="templates/company-{{ company.name.lower().replace(' ', '_') }}.html" class="company-card">
          <img class="company-logo" src="static/assets/logos/{{ company.logo }}" alt="{{ company.name }} logo">
          <div class="company-name">{{ company.name }}</div>
          <div class="company-rating">{{ company.score }} <span class="star">⭐️</span></div>
        </a>
      {% endfor %}
    </div>
  </div>
  <div class="footer">
    &copy; 2025 SwissRate | <a href="legal.html">CGU</a> | <a href="about.html">À propos</a> | <a href="contact.html">Contact</a>
  </div>
</body>
</html>
        """)
    print("index.html généré (Jinja2 ready).")

# 6. add-company.html
add_company_path = os.path.join(base_dir, "templates/add-company.html")
if not os.path.exists(add_company_path):
    with open(add_company_path, "w", encoding="utf-8") as f:
        f.write("""
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <title>Ajouter une société – SwissRate</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="static/assets/style.css">
  <style>
    .add-company-form {max-width: 430px; background: #fafbfc; margin: 3.5rem auto 2.5rem auto; padding: 2rem 2.2rem 1.7rem 2.2rem; border-radius: 14px; box-shadow: 0 2px 12px 0 rgba(0,0,0,0.03); border: 1.5px solid #e4e9ec;}
    .add-company-form h2 {text-align: center; margin-bottom: 1.2rem; font-weight: 700; font-size: 1.35rem;}
    .form-group {margin-bottom: 1.1rem;}
    .form-group label {display: block; font-weight: 500; margin-bottom: 0.3rem; color: #222;}
    .form-group input[type="text"], .form-group input[type="url"], .form-group input[type="file"] {width: 100%; padding: 0.45rem 0.65rem; border-radius: 7px; border: 1.3px solid #c8d0d8; font-size: 1rem; background: #fff; box-sizing: border-box; margin-bottom: 0.1rem;}
    .form-group input[type="file"] {padding: 0.2rem 0.1rem; background: none; border: none;}
    .add-company-btn-main {width: 100%; background: #e63946; color: #fff; border: none; border-radius: 18px; padding: 0.55rem 0; font-size: 1.07rem; font-weight: 600; margin-top: 0.5rem; cursor: pointer; transition: background 0.18s; letter-spacing: .04em;}
    .add-company-btn-main:disabled {opacity:0.55;cursor:not-allowed;}
    .add-company-btn-main:hover:enabled {background: #b92a36;}
    .form-help {text-align: center; font-size: 0.97rem; color: #5b6166; margin-top: 1.2rem;}
    @media (max-width: 600px) {.add-company-form { padding: 1.2rem 0.7rem; }}
  </style>
</head>
<body>
  <nav class="navbar container">
    <div class="navbar-left">
      <span class="logo"><span>Swiss</span>Rate</span>
    </div>
    <div class="navbar-center">
      <a href="index.html">Accueil</a>
      <a href="about.html">À propos</a>
      <a href="legal.html">CGU</a>
      <a href="contact.html">Contact</a>
      <a href="add-company.html" class="active">Ajouter une société</a>
    </div>
    <div class="navbar-right">
      <input class="search-bar" type="search" placeholder="Rechercher…">
      <a class="login-btn" href="login.html">Login</a>
    </div>
  </nav>
  {% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
      <ul class="flashes">
        {% for category, message in messages %}
          <li class="{{ category }}">{{ message }}</li>
        {% endfor %}
      </ul>
    {% endif %}
  {% endwith %}
  <form class="add-company-form" autocomplete="off" method="POST" enctype="multipart/form-data">
    <h2>Ajouter une nouvelle société</h2>
    <div class="form-group">
      <label for="company-name">Nom de la société <span style="color:#e63946;">*</span></label>
      <input type="text" id="company-name" name="company-name" required placeholder="ex : Nestlé SA">
    </div>
    <div class="form-group">
      <label for="company-website">Site web</label>
      <input type="url" id="company-website" name="company-website" required placeholder="ex : https://www.nestle.com">
    </div>
    <div class="form-group">
      <label for="company-logo">Logo de la société</label>
      <input type="file" id="company-logo" name="company-logo" accept=".png,.jpg,.jpeg,.svg,.webp" required>
    </div>
    <button type="submit" class="add-company-btn-main" disabled>Ajouter la société</button>
    <div class="form-help">
      Les informations seront vérifiées avant d’être publiées.<br>
      <span style="font-size:0.92em;">Merci de fournir un logo au format SVG ou PNG si possible.</span>
    </div>
  </form>
  <div class="footer">
    &copy; 2025 SwissRate | <a href="legal.html">CGU</a> | <a href="about.html">À propos</a> | <a href="contact.html">Contact</a>
  </div>
  <script>
document.addEventListener('DOMContentLoaded', function () {
  const form = document.querySelector('.add-company-form');
  const btn = document.querySelector('.add-company-btn-main');
  const name = document.getElementById('company-name');
  const website = document.getElementById('company-website');
  const logo = document.getElementById('company-logo');
  function checkForm() {
    if (name.value.trim() && website.value.trim() && logo.files.length > 0) {
      btn.disabled = false;
    } else {
      btn.disabled = true;
    }
  }
  name.addEventListener('input', checkForm);
  website.addEventListener('input', checkForm);
  logo.addEventListener('change', checkForm);
  btn.disabled = true;
});
  </script>
</body>
</html>
        """)
    print("add-company.html généré.")

print("\n✅ Site SwissRate prêt !\n")
print("Pour lancer le serveur :")
print("  cd", base_dir)
print("  python3 app.py")
print("\nPuis ouvre http://localhost:5000 dans ton navigateur.")
print("\nAjoute tes logos dans static/assets/logos/. Les ajouts de sociétés se font ensuite via le formulaire !")