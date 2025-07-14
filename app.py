
import os
import json
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/assets/logos/'
COMPANIES_JSON = 'companies.json'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'svg', 'webp'}

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)
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


# Gestionnaire d'erreurs global
@app.errorhandler(Exception)
def handle_exception(e):
    return f"<pre>Erreur : {e}</pre>", 500

if __name__ == '__main__':
    app.run(debug=True)