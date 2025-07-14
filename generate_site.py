import os

# Dossiers
BASE = os.path.dirname(os.path.abspath(__file__))
LOGO_DIR = os.path.join(BASE, "static", "assets", "logos")
TEMPLATE_DIR = os.path.join(BASE, "templates")

# Liste des sociétés à générer (dérivée des fichiers logos)
logos = [f for f in os.listdir(LOGO_DIR) if f.lower().endswith(('.svg', '.png', '.webp', '.jpg', '.jpeg')) and not f.startswith('0')]
logos.sort()

# Génère un nom d'entreprise et un score fictif (ajuste selon tes besoins)
def company_name(filename):
    name = os.path.splitext(filename)[0]
    # Cas spéciaux (à compléter si certains noms doivent être beaux)
    special = {
        "philipmorris": "Philip Morris International",
        "swissre": "Swiss Re",
        "swisslife": "Swiss Life",
        "credit-suisse": "Credit Suisse",
        "partnersgroup": "Partners Group",
        "lonza_group": "Lonza",
    }
    return special.get(name.lower(), name.replace("_", " ").replace("-", " ").title())

def page_link(filename):
    name = os.path.splitext(filename)[0]
    return f"templates/company-{name}.html"

def score_for_company(idx):
    return f"{round(3.85 + 0.13 * ((idx % 10) / 10), 2)}"  # Score fictif lisible

# Génération d’index.html
def generate_index_html():
    head = '''<!DOCTYPE html>
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
'''
    tail = '''
    </div>
  </div>
  <div class="footer">
    &copy; 2025 SwissRate | <a href="legal.html">CGU</a> | <a href="about.html">À propos</a> | <a href="contact.html">Contact</a>
  </div>
</body>
</html>
'''

    grid = ""
    for idx, logo in enumerate(logos):
        name = company_name(logo)
        page = page_link(logo)
        score = score_for_company(idx)
        grid += f'''      <a href="{page}" class="company-card">
        <img class="company-logo" src="static/assets/logos/{logo}" alt="{name} logo">
        <div class="company-name">{name}</div>
        <div class="company-rating">{score} <span class="star">⭐️</span></div>
      </a>
'''

    with open(os.path.join(BASE, "index.html"), "w", encoding="utf-8") as f:
        f.write(head + grid + tail)
    print("index.html généré avec succès ! ({}) sociétés".format(len(logos)))

# Génération d’une page entreprise générique
def generate_company_pages():
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
      </div>
    </div>
    <div style="margin-top:2.5rem;color:#333;">Page de présentation de l'entreprise {name}.<br>À compléter avec plus de détails…</div>
  </div>
  <div class="footer">
    &copy; 2025 SwissRate | <a href="../legal.html">CGU</a> | <a href="../about.html">À propos</a> | <a href="../contact.html">Contact</a>
  </div>
</body>
</html>
'''
    for idx, logo in enumerate(logos):
        name = company_name(logo)
        filename = os.path.join(TEMPLATE_DIR, f"company-{os.path.splitext(logo)[0]}.html")
        score = score_for_company(idx)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(template.format(name=name, logo=logo, score=score))
    print("Pages entreprise générées avec succès.")

if __name__ == "__main__":
    generate_index_html()
    generate_company_pages()