import os
import random

BASE_DIR = "/Users/louisboyer/Documents/Website"
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
LOGOS_DIR = os.path.join(BASE_DIR, "static/assets/logos")

def display_name_from_logo(filename):
    name = os.path.splitext(filename)[0]
    return name.replace('_', ' ').replace('-', ' ').title()

def slug_from_logo(filename):
    return os.path.splitext(filename)[0].lower()

def random_scores(n):
    return [round(random.uniform(3.7, 4.8), 1) for _ in range(n)]

def make_avatar(nom):
    parts = nom.split()
    initials = (parts[0][0] + parts[1][0] if len(parts) > 1 else parts[0][0]).upper()
    return initials

def render_svg_stars(score):
    # max 5 étoiles
    html = ''
    for i in range(1, 6):
        if score >= i:
            html += '''<svg class="star-svg" viewBox="0 0 20 20"><defs><linearGradient id="s1" x1="0" x2="0" y1="0" y2="1"><stop stop-color="#ffc100"/><stop offset="1" stop-color="#ffb800"/></linearGradient></defs><polygon points="10,2 12.59,7.36 18.51,8.03 14,12.25 15.18,18.09 10,15.05 4.82,18.09 6,12.25 1.49,8.03 7.41,7.36" fill="url(#s1)" stroke="#e2aa00" stroke-width="0.7"/></svg>'''
        elif (score + 0.5) >= i:
            html += '''<svg class="star-svg" viewBox="0 0 20 20"><defs><linearGradient id="halfgrad"><stop offset="50%" stop-color="#ffc100"/><stop offset="50%" stop-color="#eef0f4"/></linearGradient></defs><polygon points="10,2 12.59,7.36 18.51,8.03 14,12.25 15.18,18.09 10,15.05 4.82,18.09 6,12.25 1.49,8.03 7.41,7.36" fill="url(#halfgrad)" stroke="#e2aa00" stroke-width="0.7"/></svg>'''
        else:
            html += '''<svg class="star-svg" viewBox="0 0 20 20"><polygon points="10,2 12.59,7.36 18.51,8.03 14,12.25 15.18,18.09 10,15.05 4.82,18.09 6,12.25 1.49,8.03 7.41,7.36" fill="#eef0f4" stroke="#d3d6db" stroke-width="0.7"/></svg>'''
    return html

def average(scores):
    return round(sum(scores) / len(scores), 1) if scores else 0

def weighted_average(scores_dict):
    total_weight = 5 + 5 + 4
    sum_weighted = (sum(scores_dict["candidats"]) + sum(scores_dict["prestataires"]) + sum(scores_dict["commerciaux"]))
    return round(sum_weighted / total_weight, 2)

def render_header(name, logo_path, score):
    stars_html = render_svg_stars(score)
    return f'''
      <div class="company-header">
        <img class="company-logo" src="{logo_path}" alt="{name} logo">
        <div class="company-name">{name}</div>
        <div class="company-rating-main"><span class="main-score">{score:.2f}</span> <span class="star-bar">{stars_html}</span></div>
      </div>
    '''

def render_scores_section(scores_dict):
    subs = {
        "candidats": [
            "Facilité de candidature", "Retour sur candidature", "Processus d’entretien", "Clarté des attentes", "Respect des délais"
        ],
        "prestataires": [
            "Communication", "Rapidité de paiement", "Qualité de la relation", "Respect des engagements", "Accueil partenaires"
        ],
        "commerciaux": [
            "Réactivité", "Transparence", "Équité négociation", "Ouverture innovation"
        ]
    }
    cats = [("Candidats", "candidats", 5), ("Prestataires / Clients", "prestataires", 5), ("Commerciaux externes", "commerciaux", 4)]
    html = '<div class="ratings-grid">\n'
    for (title, key, n) in cats:
        values = scores_dict[key]
        avg = average(values)
        html += f'<div class="rating-cat"><h3>{title}</h3><div class="cat-score">{avg:.1f}/5</div><div class="subratings">'
        for i, v in enumerate(values):
            label = subs[key][i] if i < len(subs[key]) else f"Sous-score {i+1}"
            html += f'''
              <div>
                <span class="sub-label">{label}</span>
                <span class="star-bar">{render_svg_stars(v)}</span>
                <span class="sub-star-score">{v:.1f}</span>
              </div>
            '''
        html += '</div></div>\n'
    html += '</div>'
    return html

def render_comments_section(comments):
    html = '<div class="comments-list">\n'
    for nom, role, date, texte in comments:
        avatar = make_avatar(nom)
        html += f'''
        <div class="comment-item">
            <div class="comment-avatar">{avatar}</div>
            <div class="comment-body">
                <div>
                    <span class="comment-author">{nom}</span>
                    <span class="comment-type">{role}</span>
                    <span class="comment-date">– {date}</span>
                    <button class="comment-flag-btn" onclick="reportComment('{nom}', '{date}')">Signaler</button>
                </div>
                <div class="comment-text">{texte}</div>
            </div>
        </div>
        '''
    html += '</div>'
    return html

def js_report_popup():
    return '''
    <script>
    function reportComment(nom, date) {
        alert("Fonction de signalement à implémenter pour " + nom + " (" + date + ")");
    }
    </script>
    '''

def generate_random_comments(name):
    # List of realistic French/Swiss names for each role
    candidats = [
        ("Élodie Martin", "Candidat"),
        ("Lucas Dubois", "Candidat"),
        ("Chloé Lambert", "Candidat"),
        ("Maxime Moreau", "Candidat"),
        ("Camille Lefevre", "Candidat"),
    ]
    prestataires = [
        ("Sophie Girard", "Prestataire"),
        ("Antoine Blanc", "Prestataire"),
        ("Claire Fontaine", "Prestataire"),
        ("Julien Perrin", "Prestataire"),
        ("Isabelle Roche", "Prestataire"),
    ]
    commercants = [
        ("Nicolas Mercier", "Commerçant"),
        ("Laura Petit", "Commerçant"),
        ("Thomas Bernard", "Commerçant"),
        ("Marie Dubois", "Commerçant"),
        ("Pauline Simon", "Commerçant"),
    ]
    # Randomly select one name per role
    c_nom, c_role = random.choice(candidats)
    p_nom, p_role = random.choice(prestataires)
    co_nom, co_role = random.choice(commercants)

    comments = [
        (c_nom, c_role, "12 avril 2024", f"Très bonne expérience avec {name}, le processus de candidature est clair et rapide."),
        (p_nom, p_role, "5 mars 2024", f"La communication avec {name} est excellente, toujours un bon suivi."),
        (co_nom, co_role, "28 février 2024", f"Les commerciaux externes de {name} sont réactifs et à l’écoute, je recommande."),
    ]
    return comments

# Nettoyage des anciens fichiers company-*.html
for file in os.listdir(TEMPLATES_DIR):
    if file.startswith("company-") and file.endswith(".html"):
        os.remove(os.path.join(TEMPLATES_DIR, file))

# Récupération de tous les fichiers logos valides dans le dossier logos
logo_files = [f for f in os.listdir(LOGOS_DIR) if f.lower().endswith(('.svg', '.png', '.webp'))]

TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8" />
  <title>__COMPANY_TITLE__</title>
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <link rel="stylesheet" href="../static/assets/style.css" />
  <style>
    body {{font-family: 'Segoe UI', Arial, sans-serif; background: #f7f8fa; margin:0; padding:0;}}
    .container {{max-width: 1240px; margin: 0 auto; padding: 0 1.5rem;}}
    .company-header {{text-align: center; margin: 3.5rem 0 2.4rem;}}
    .company-logo {{height: 64px; max-width: 220px; object-fit: contain; margin: 0 auto 1.5rem;}}
    .company-name {{font-size: 2.1rem; font-weight: 800; letter-spacing: 0.04em; margin-bottom: 0.6rem;}}
    .company-rating-main {{font-size: 2.1rem; color: #e63946; font-weight: 700; display: inline-flex; align-items: center;}}
    .main-score {{font-size:2.1rem;font-weight:700;color:#e63946;margin-right:0.4em;}}
    .star-bar {{display: inline-flex; gap: 1.2px; vertical-align: middle;}}
    .star-svg {{ width: 18px; height: 18px; margin: 0 0.5px; filter: drop-shadow(0px 1px 1.1px #ebe9ee); vertical-align: middle;}}
    .ratings-grid {{display: grid; grid-template-columns: repeat(3, 1fr); gap: 2.7rem; margin: 3rem 0;}}
    .rating-cat {{background: #fff; border-radius: 18px; box-shadow: 0 2px 14px 0 rgba(0,0,0,0.04); padding: 2.1rem 1.4rem 1.3rem; min-width: 0;}}
    .rating-cat h3 {{text-align: center; margin-bottom: 1rem; font-size: 1.2rem;}}
    .rating-cat .cat-score {{text-align: center; font-size: 1.4rem; font-weight: bold; color: #222; margin-bottom: 1rem;}}
    .subratings {{margin-top: 0.6rem;}}
    .subratings div {{display: flex; justify-content: space-between; align-items: center; padding: 0.35em 0;}}
    .sub-label {{flex: 1 1 60%; text-align: left;}}
    .sub-star-score {{font-size:0.97em;color:#444;margin-left:0.35em;}}
    @media (max-width: 900px) {{.ratings-grid {{grid-template-columns: 1fr; gap: 1.1rem;}}}}
    .comments-section {{margin: 3.5rem auto 2rem; max-width: 800px;}}
    .comments-section h2 {{font-size: 1.25rem; font-weight: 600; margin-bottom: 1rem;}}
    .comment-form {{display: flex; flex-direction: column; gap: 1rem; margin-bottom: 2rem;}}
    .comment-form textarea {{min-height: 70px; padding: 0.8em; font-size: 1.02rem; border-radius: 8px; border: 1px solid #e5e6ea; background: #fafdff;}}
    .comment-form button {{align-self: flex-end; background: #e63946; color: #fff; border: none; border-radius: 7px; padding: 0.7em 1.7em; font-weight: 600; font-size: 1.06em; cursor: pointer; transition: opacity 0.3s ease;}}
    .comment-form button:disabled {{opacity: 0.7; cursor: not-allowed;}}
    .comment-form textarea:focus {{outline: 1.5px solid #cbd0d8;}}
    .comments-list {{margin-top: 0.8rem;}}
    .comment-item {{display: flex; gap: 1.1em; align-items: flex-start; margin-bottom: 1.7em;}}
    .comment-avatar {{width: 40px; height: 40px; background: #dde0e6; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; color: #aaa; font-size: 1.15em;}}
    .comment-body {{flex:1;}}
    .comment-author {{font-weight:600; font-size:1em;}}
    .comment-type {{font-style: italic; color: #ae1836; font-size:0.99em; margin-left:0.8em;}}
    .comment-date {{color:#777; font-size:0.98em; margin-left:0.7em;}}
    .comment-text {{margin-top: 0.25em; font-size: 1.06em;}}
    .comment-flag-btn {{
      margin-left: 0.7em; font-size: 0.97em; color: #aaa; border: 1px solid #ccc; background: #f7f7fa;
      border-radius: 6px; padding: 2.5px 14px; cursor: pointer; transition: background .14s,color .12s;
    }}
    .comment-flag-btn:hover {{background:#fee; color:#e63946; border-color:#e63946;}}

    /* Navbar styles updated */
    nav.navbar {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0.9rem 1.5rem;
      background-color: #fff;
      box-shadow: 0 2px 8px rgba(0,0,0,0.08);
      position: sticky;
      top: 0;
      z-index: 1000;
      font-family: 'Segoe UI', Arial, sans-serif;
    }}
    .navbar-left {{
      display: flex;
      align-items: center;
      gap: 1.5rem;
      flex: 0 0 auto;
    }}
    .nav-logo {{
      font-weight: 800;
      font-size: 1.5rem;
      letter-spacing: 0.01em;
      color: #111;
      text-decoration: none;
      display: flex;
      align-items: center;
    }}
    .nav-logo span:first-child {{
      color: #e63946;
    }}
    .nav-link {{
      font-weight: 600;
      font-size: 1rem;
      color: #444;
      text-decoration: none;
      padding: 0.3rem 0.6rem;
      border-radius: 5px;
      transition: background-color 0.3s ease, color 0.3s ease;
    }}
    .nav-link:hover {{
      background-color: #fceaea;
      color: #e63946;
    }}
    .navbar-center {{
      flex: 1 1 auto;
      display: flex;
      justify-content: center;
    }}
    .navbar-center input[type="search"] {{
      width: 100%;
      max-width: 400px;
      padding: 0.5rem 1rem;
      border-radius: 25px;
      border: 1.5px solid #ddd;
      font-size: 1rem;
      transition: border-color 0.3s ease;
    }}
    .navbar-center input[type="search"]:focus {{
      outline: none;
      border-color: #e63946;
      box-shadow: 0 0 5px rgba(230, 57, 70, 0.5);
    }}
    .navbar-right {{
      display: flex;
      align-items: center;
      gap: 1rem;
      flex: 0 0 auto;
    }}
    .nav-btn {{
      background-color: #e63946;
      color: white;
      padding: 0.5rem 1.3rem;
      font-weight: 700;
      border-radius: 25px;
      text-decoration: none;
      font-size: 1rem;
      transition: background-color 0.3s ease;
      cursor: pointer;
      border: none;
      display: inline-flex;
      align-items: center;
      justify-content: center;
    }}
    .nav-btn:hover {{
      background-color: #b32a35;
      color: #fff;
    }}
    @media (max-width: 768px) {{
      nav.navbar {{
        flex-wrap: wrap;
        justify-content: center;
        gap: 0.8rem;
      }}
      .navbar-left, .navbar-right {{
        flex: 1 1 100%;
        justify-content: center;
        gap: 1rem;
      }}
      .navbar-center {{
        order: 3;
        width: 100%;
        max-width: none;
        margin-top: 0.5rem;
      }}
      .navbar-center input[type="search"] {{
        max-width: 100%;
      }}
    }}
  </style>
</head>
<body>
  <nav class="navbar">
    <div class="navbar-left">
      <a href="../index.html" class="nav-logo">
        <span>Swiss</span><span>Rate</span>
      </a>
      <a href="../index.html" class="nav-link">Accueil</a>
    </div>
    <div class="navbar-center">
      <input type="search" placeholder="Rechercher une société…" aria-label="Recherche">
    </div>
    <div class="navbar-right">
      <a href="../templates/about.html" class="nav-link">À propos</a>
      <a href="../templates/legal.html" class="nav-link">CGU</a>
      <a href="../templates/add-company.html" class="nav-link">Ajouter une société</a>
      <a href="../templates/login.html" class="nav-btn">Se connecter</a>
    </div>
  </nav>
  <div class="container">
    {header}
    {scores_section}
  </div>
  <div class="comments-section">
    <h2>Commentaires</h2>
    <form class="comment-form" onsubmit="return false;">
      <textarea placeholder="Écrivez votre avis…" oninput="document.getElementById('publishBtn').disabled = !this.value.trim()"></textarea>
      <button id="publishBtn" disabled>Publier</button>
    </form>
    {comments_section}
  </div>
  {js_popup}
</body>
</html>
"""

for logo_file in logo_files:
    name = display_name_from_logo(logo_file)
    slug = slug_from_logo(logo_file)
    logo_path = f"../static/assets/logos/{logo_file}"
    scores = {
        "candidats": random_scores(5),
        "prestataires": random_scores(5),
        "commerciaux": random_scores(4),
    }
    score = weighted_average(scores)
    comments = generate_random_comments(name)
    html = TEMPLATE.format(
        header=render_header(name, logo_path, score),
        scores_section=render_scores_section(scores),
        comments_section=render_comments_section(comments),
        js_popup=js_report_popup()
    ).replace("__COMPANY_TITLE__", f"{name} – SwissRate")
    with open(os.path.join(TEMPLATES_DIR, f"company-{slug}.html"), "w", encoding="utf-8") as f:
        f.write(html)

print(f"{len(logo_files)} pages générées dans {TEMPLATES_DIR}")