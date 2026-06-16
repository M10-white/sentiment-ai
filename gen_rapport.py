# -*- coding: utf-8 -*-
"""Construit le rapport complet de l'atelier (TP0 a TP4), format questions/reponses."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle, PageBreak,
    KeepTogether, Image
)
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate
from reportlab.platypus.frames import Frame
import os

OUTPUT = r"C:\Users\bchao\Downloads\rapport_atelier_tests_sentimentia.pdf"
SCREENSHOTS_DIR = r"C:\Users\bchao\Downloads\screenshots"  # Dossier où placer vos screenshots

styles = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=styles["Heading1"], fontSize=15,
    textColor=colors.HexColor("#14306b"), spaceBefore=16, spaceAfter=6)
H2 = ParagraphStyle("H2", parent=styles["Heading2"], fontSize=11.5,
    textColor=colors.HexColor("#33475b"), spaceBefore=11, spaceAfter=3)
BODY = ParagraphStyle("BODY", parent=styles["Normal"], fontSize=10.3, leading=15.5,
    spaceAfter=7, alignment=4)
QSTYLE = ParagraphStyle("Q", parent=styles["Normal"], fontSize=10, leading=14,
    textColor=colors.HexColor("#14306b"), backColor=colors.HexColor("#eaeef5"),
    borderColor=colors.HexColor("#c3ccdd"), borderWidth=0.5, borderPadding=7,
    spaceAfter=5, fontName="Helvetica-Bold")
ANS = ParagraphStyle("ANS", parent=styles["Normal"], fontSize=10.3, leading=15.5,
    spaceAfter=9, alignment=4, leftIndent=4)
CODE = ParagraphStyle("CODE", parent=styles["Code"], fontSize=8.5, leading=12.5,
    backColor=colors.HexColor("#f4f5f7"), borderColor=colors.HexColor("#d0d3d9"),
    borderWidth=0.5, borderPadding=6, spaceAfter=8)
LI = ParagraphStyle("LI", parent=styles["Normal"], fontSize=10.3, leading=15,
    leftIndent=14, spaceAfter=3)

story = []
def P(t): story.append(Paragraph(t, BODY))
def h1(t): story.append(Paragraph(t, H1))
def h2(t): story.append(Paragraph(t, H2))
def li(t): story.append(Paragraph(f"&#8226;&nbsp;&nbsp;{t}", LI))
def code(t): story.append(Paragraph(t, CODE))
def sp(h=6): story.append(Spacer(1, h))

def qa(num, question, answers):
    """Un bloc question + reponse(s), gardes ensemble si possible."""
    flow = [Paragraph(f"Question {num}. {question}", QSTYLE)]
    for a in answers:
        flow.append(Paragraph(a, ANS))
    story.append(KeepTogether(flow))

def add_screenshot(filename, width=15*cm, caption=""):
    """Ajoute une image (screenshot) au rapport."""
    filepath = os.path.join(SCREENSHOTS_DIR, filename)
    if os.path.exists(filepath):
        img = Image(filepath, width=width)
        story.append(img)
        if caption:
            story.append(Paragraph(f"<i>{caption}</i>", 
                ParagraphStyle("Caption", parent=styles["Normal"], fontSize=9, 
                    alignment=1, spaceAfter=8, textColor=colors.HexColor("#666666"))))
        sp(6)
    else:
        story.append(Paragraph(f"<font color='red'>[Image manquante: {filename}]</font>", BODY))
        sp(3)

def make_table(data, widths, header_color="#33475b"):
    t = Table(data, colWidths=widths)
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0), colors.HexColor(header_color)),
        ("TEXTCOLOR",(0,0),(-1,0), colors.white),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
        ("FONTSIZE",(0,0),(-1,-1),9),
        ("GRID",(0,0),(-1,-1),0.4, colors.HexColor("#c2c6cc")),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white, colors.HexColor("#eef1f5")]),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("BOTTOMPADDING",(0,0),(-1,-1),5),("TOPPADDING",(0,0),(-1,-1),5),
        ("LEFTPADDING",(0,0),(-1,-1),6),
    ]))
    story.append(t)

def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#9aa0a6"))
    canvas.drawString(2*cm, 1.2*cm, "Atelier Automatisation des Tests, Projet SentimentIA")
    canvas.drawRightString(19*cm, 1.2*cm, "%d" % doc.page)
    canvas.restoreState()

doc = BaseDocTemplate(OUTPUT, pagesize=A4,
    leftMargin=2.3*cm, rightMargin=2.3*cm, topMargin=2.1*cm, bottomMargin=1.9*cm)
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="main")
doc.addPageTemplates([PageTemplate(id="all", frames=[frame], onPage=footer)])

# ============ PAGE DE TITRE ============
story.append(Spacer(1, 5*cm))
story.append(Paragraph("Mise en place d'une suite de tests automatises",
    ParagraphStyle("T1", parent=styles["Title"], fontSize=24,
        textColor=colors.HexColor("#14306b"), leading=30, spaceAfter=10)))
story.append(Paragraph("Projet SentimentIA, API d'analyse de sentiments",
    ParagraphStyle("T2", parent=styles["Normal"], fontSize=14, alignment=1,
        textColor=colors.HexColor("#5a6472"), spaceAfter=40)))
story.append(HRFlowable(width="55%", thickness=1.2, color=colors.HexColor("#14306b"),
    spaceAfter=30, hAlign="CENTER"))
story.append(Paragraph("Rapport d'atelier", ParagraphStyle("T3", parent=styles["Normal"],
    fontSize=13, alignment=1, textColor=colors.HexColor("#33475b"), spaceAfter=6)))
story.append(Paragraph("Tests unitaires, tests d'integration, integration continue, "
    "TDD, tests de performance et audit de securite",
    ParagraphStyle("T4", parent=styles["Normal"], fontSize=10.5, alignment=1,
        textColor=colors.HexColor("#5a6472"), leading=16)))
story.append(PageBreak())

# ============ INTRODUCTION ============
h1("1. Introduction et contexte")
P("Dans le cadre de cet atelier, j'ai pris en charge la mise en place de la suite de tests "
  "complete de SentimentIA, une API d'analyse de sentiments destinee a traiter les avis "
  "clients. Le travail s'est deroule en cinq etapes successives : la mise en place de "
  "l'environnement (TP0), l'ecriture des tests unitaires (TP1), les tests d'integration de "
  "l'API (TP2), la construction d'un pipeline d'integration continue (TP3), puis un cycle TDD "
  "accompagne de tests de performance et d'un audit de securite (TP4).")
P("L'objectif n'etait pas de developper l'application elle-meme, fournie au depart, mais d'en "
  "garantir la fiabilite par une strategie de test progressive. J'ai structure ma demarche "
  "pour que chaque niveau de test reponde a une question precise : la logique metier est-elle "
  "correcte, l'API repond-elle bien, le code reste-t-il sain, et tient-il la charge ? "
  "Au fil de l'atelier, quatre defauts ont ete identifies puis corriges grace aux tests.")

# ============ PRESENTATION ============
h1("2. Presentation de l'application")
P("SentimentIA expose une API HTTP construite avec FastAPI. Le coeur metier, la classe "
  "SentimentModel, analyse un texte en comptant les mots positifs et negatifs qu'il contient, "
  "puis en deduit un label (POSITIVE, NEGATIVE ou NEUTRAL) et un score de confiance compris "
  "entre 0 et 1. La validation des donnees entrantes est assuree par Pydantic : un texte vide, "
  "trop long ou absent est automatiquement rejete. L'API met a disposition quatre points "
  "d'entree :")
make_table([
    ["Methode", "URL", "Role"],
    ["GET", "/health", "Verifier que l'API est operationnelle"],
    ["POST", "/predict", "Analyser un texte et renvoyer le sentiment"],
    ["GET", "/stats", "Consulter les compteurs de predictions"],
    ["POST", "/reset", "Remettre les compteurs a zero"],
], [2.5*cm, 3.5*cm, 9.5*cm])

# ============ TP0 ============
h1("3. TP0, mise en place de l'environnement")
P("J'ai cree l'arborescence du projet en separant le code source (src/) des tests (tests/), "
  "isole les dependances dans un environnement virtuel, installe les bibliotheques en versions "
  "epinglees, et centralise la configuration de pytest dans pytest.ini. Les deux smoke tests "
  "fournis passent, ce qui confirme que l'environnement est fonctionnel.")
qa("0.1", "Que renvoie l'API pour un texte vide, un texte de 6000 caracteres, ou un champ text absent ?",
   ["Dans les trois cas, l'API renvoie un code 422. Le champ text est contraint par Pydantic "
    "avec min_length=1 et max_length=5000 : un texte vide viole la longueur minimale, un texte "
    "de 6000 caracteres depasse la longueur maximale, et l'absence du champ viole l'obligation "
    "de le fournir. Ces rejets ont lieu avant meme que la logique metier soit atteinte."])
qa("0.2", "Tracez l'execution de predict('Ce produit est horrible et mauvais').",
   ["La tokenisation donne ['ce', 'produit', 'est', 'horrible', 'et', 'mauvais']. Le comptage "
    "trouve 0 mot positif et 2 mots negatifs (horrible et mauvais), donc neg superieur a pos. "
    "Le score vaut min(0.6 + 0.1 x 2, 1.0) = 0.8. La methode renvoie "
    "{'label': 'NEGATIVE', 'score': 0.8, 'text': 'Ce produit est horrible et mauvais'}."])
qa("0.3", "Dans quel cas predict() leve-t-elle une exception ?",
   ["Elle leve SentimentError lorsque la tokenisation ne trouve aucun mot, c'est a dire quand "
    "le texte ne contient aucun caractere alphabetique. Par exemple predict('1234 !!! ???') "
    "declenche l'exception. On le reconnait dans le code au bloc 'if not tokens' place juste "
    "apres la tokenisation."])
qa("0.4", "Que se passe-t-il si model.predict() leve une SentimentError dans l'endpoint /predict ?",
   ["L'endpoint capture l'exception et la transforme en HTTPException avec le code 422. C'est "
    "donc le meme code que celui renvoye par Pydantic en cas de validation echouee, mais "
    "l'origine differe : ici l'erreur vient de la logique metier, et non de la validation du "
    "schema d'entree."])
qa("0.5", "Capture d'ecran des 2 smoke tests en statut PASSED.",
   ["Les deux smoke tests (test_health_returns_ok et test_predict_positive_text) passent. "
    "pytest affiche '2 passed', ce qui valide l'installation de l'environnement."])
add_screenshot("tp0_smoke_tests.png", caption="Figure 0.1 – Résultat des 2 smoke tests en vert")
sp(3)
qa("0.6", "Quelles lignes de src/model.py ne sont pas couvertes par les 2 smoke tests, et pourquoi ?",
   ["Avant l'ecriture des tests du TP1, la couverture laissait de cote la levee de "
    "SentimentError ainsi que les branches NEGATIVE et NEUTRAL. C'est normal : les smoke tests "
    "n'envoient qu'un texte positif valide, donc seul ce chemin est parcouru. Pour couvrir le "
    "reste, il faut des tests unitaires ciblant chaque branche (texte negatif, texte neutre, "
    "texte sans mot analysable)."])

# ============ TP1 ============
h1("4. TP1, tests unitaires du modele")
P("Les tests unitaires ciblent la methode predict() en isolation. J'ai introduit une fixture "
  "qui fournit une instance fraiche du modele a chaque test, couvert les trois labels, "
  "l'exception, et utilise la parametrisation ainsi qu'un mock.")
qa("1.1", "Les deux tests fournis passent-ils ? Que remarquez-vous sur leur nom ?",
   ["Les deux tests passent. Leur nom explicite (par exemple test_predict_retourne_positive) "
    "permet de comprendre immediatement ce qui est verifie et de localiser un echec dans le "
    "rapport sans avoir a lire le corps du test."])
qa("1.2", "Quel est l'apport de la fixture model() ?",
   ["Les tests ne contiennent plus la ligne de creation de l'instance, elle est injectee "
    "automatiquement. Si le constructeur de la classe evolue, je n'ai qu'un seul endroit a "
    "modifier au lieu de chaque test. Chaque test demarre aussi avec une instance propre, ce "
    "qui evite tout etat partage involontaire."])
qa("1.3", "Combien de tests genere le bloc parametrize, et comment sont-ils nommes ?",
   ["Le bloc avec cinq jeux de donnees genere cinq tests distincts. Chacun apparait "
    "individuellement dans le rapport, avec ses parametres entre crochets, par exemple "
    "test_predict_labels_parametrises[produit super-POSITIVE]. Chaque cas peut donc echouer "
    "independamment des autres."])
qa("1.4", "La vraie methode predict() s'execute-t-elle dans le test avec mock ? A quoi sert ce test ?",
   ["Non, la vraie methode ne s'execute pas : le mock la remplace et renvoie directement une "
    "valeur predefinie. Ce test verifie le contrat d'appel (predict appelee une seule fois, "
    "avec le bon argument). Ce mecanisme deviendrait indispensable si la methode appelait une "
    "API externe payante : on testerait le comportement sans declencher d'appel reseau reel."])
qa("1.5", "Quelle est votre couverture sur src/model.py ?",
   ["Apres l'ecriture de tous les tests et la correction du defaut de score, la couverture de "
    "src/model.py atteint 100 pour cent. Toutes les branches sont exercees : positif, negatif, "
    "neutre, exception, et le plafonnement du score."])
add_screenshot("tp1_coverage.png", caption="Figure 1.1 – Rapport de couverture TP1: 100%")
sp(3)
h2("Defaut detecte au TP1 : le score non borne")
P("Un test envoyant les dix mots positifs verifiait que le score ne depassait pas 1.0. Il a "
  "echoue en affichant 1.6 : la formule 0.6 + 0.1 x n n'etait pas plafonnee. J'ai corrige le "
  "calcul en l'encadrant par min(..., 1.0).")

# ============ TP2 ============
h1("5. TP2, tests d'integration de l'API")
P("Les tests d'integration verifient le comportement de bout en bout, de la requete HTTP a la "
  "reponse JSON. J'ai regroupe les outils communs dans conftest.py : un client reutilisable, "
  "des generateurs de textes via Faker, et une fixture de remise a zero des compteurs.")
qa("2.1", "Pourquoi reset_stats utilise yield, et pourquoi autouse=True ?",
   ["yield separe ce qui s'execute avant le test de ce qui s'executerait apres. La remise a "
    "zero est placee avant le yield pour que chaque test demarre d'un etat propre. Si on "
    "appelait /reset apres le yield, la remise a zero aurait lieu a la fin et le premier test "
    "partirait d'un etat non garanti. autouse=True garantit que cette remise a zero s'applique "
    "a tous les tests sans avoir a la declarer, assurant leur isolation systematique."])
qa("2.2", "Pourquoi test_stats_incremente n'appelle pas /reset, et que se passe-t-il sans autouse ?",
   ["Il n'a pas besoin d'appeler /reset car la fixture autouse l'a deja fait avant le test : "
    "les compteurs sont a zero. Sans autouse, la fixture ne s'executerait plus automatiquement, "
    "les compteurs conserveraient les valeurs des tests precedents, et l'assertion "
    "total_predictions == 0 echouerait de facon imprevisible selon l'ordre d'execution."])
qa("2.3", "Quelle structure JSON renvoie une erreur 422, et ou se trouve le message ?",
   ["FastAPI renvoie une structure de la forme {'detail': [ {...} ]}. Le message lisible se "
    "trouve dans detail[0]['msg'], et le champ detail[0]['loc'] indique precisement quel champ "
    "est en cause."])
qa("2.4", "Pourquoi les tests restent stables malgre Faker, et quel est son interet ?",
   ["Les fixtures injectent toujours un mot-cle connu du modele dans une phrase aleatoire, et "
    "les assertions portent sur le label (determine par ce mot-cle), pas sur le texte exact. "
    "Le resultat reste donc deterministe. L'interet de Faker est de tester une grande variete "
    "de textes realistes plutot qu'une seule chaine figee, ce qui revele des bugs lies a des "
    "formats inattendus."])
qa("2.5", "Que constatez-vous en inversant l'ordre des deux tests defectueux ?",
   ["Selon l'ordre, l'un des deux echoue : le test qui suppose des compteurs a zero ne reussit "
    "que si l'autre ne s'est pas execute avant. Comme l'ordre d'execution de pytest n'est pas "
    "garanti, cette dependance produit des echecs imprevisibles. La fixture autouse de remise a "
    "zero resout le probleme en rendant chaque test independant."])
qa("2.6", "A quoi servent les balises de report.xml et pourquoi Jenkins en a besoin ?",
   ["Le fichier contient une balise testsuite (resume global) et une balise testcase par test, "
    "dont l'attribut time donne la duree d'execution. Jenkins a besoin de ce format XML "
    "structure plutot que de la sortie console car il peut le parser de facon fiable, marquer "
    "le build en succes ou en echec, et archiver l'historique sur plusieurs builds pour suivre "
    "les tendances (tests qui ralentissent, nouveaux echecs)."])
add_screenshot("tp2_junit_report.png", caption="Figure 2.1 – Rapports JUnit des tests d'intégration")
sp(3)
h2("Defaut detecte au TP2 : l'etat partage")
P("Deux tests volontairement dependants donnaient des resultats differents selon leur ordre "
  "d'execution. La fixture autouse de remise a zero corrige le probleme en isolant chaque test.")

# ============ TP3 ============
h1("6. TP3, pipeline d'integration continue")
P("J'ai conteneurise l'application avec un Dockerfile (python:3.12-slim), dont la construction "
  "aboutit sans erreur, decrit l'orchestration dans docker-compose, et ecrit un Jenkinsfile de "
  "six etapes : Checkout, Install, Lint, Tests Unitaires, Tests Integration et Security Scan.")
qa("3.1", "Pourquoi installer seulement le client Docker dans Jenkins, et quel est le role de docker.sock ?",
   ["Le client envoie les commandes, le daemon les execute. On installe seulement le client "
    "dans le conteneur Jenkins car il reutilise le daemon de la machine hote, accessible via le "
    "montage du fichier /var/run/docker.sock (le socket par lequel le client dialogue avec le "
    "daemon). Cela evite un daemon imbrique et reste la methode standard dite "
    "Docker-outside-of-Docker."])
qa("3.2", "Pourquoi la commande Pylint se termine par || true ?",
   ["|| true force le code de retour a zero, donc le stage ne casse jamais sur un simple "
    "avertissement de style. Sans ce suffixe, un score inferieur a 7.0 (via --fail-under) "
    "renverrait un code non nul, ferait echouer le stage, et par le principe du fail fast "
    "stopperait tous les stages suivants."])
qa("3.3", "Que signifie post { always } et pourquoi publier le rapport JUnit meme en cas d'echec ?",
   ["always s'execute quel que soit le resultat du stage, contrairement a success ou failure "
    "qui sont conditionnels. On publie le rapport JUnit meme quand des tests echouent car c'est "
    "precisement dans ce cas qu'on a besoin de voir quels tests ont echoue et pourquoi."])
qa("3.4", "Pourquoi pip3 --break-system-packages est-il necessaire et acceptable ici ?",
   ["Les distributions recentes protegent l'environnement Python systeme (PEP 668) et refusent "
    "une installation pip globale sans cette option. Dans un conteneur jetable et isole, il n'y "
    "a aucun risque de casser un autre projet, donc installer dans l'environnement systeme est "
    "parfaitement acceptable."])
qa("3.5", "Pourquoi separer tests unitaires et tests d'integration en deux stages ?",
   ["Cette separation permet de savoir immediatement quel type de test casse (la logique metier "
    "ou l'API), de produire deux rapports JUnit distincts, et grace au fail fast d'eviter de "
    "lancer les tests d'integration, plus lourds, si les tests unitaires echouent deja."])
qa("3.6", "Combien d'alertes Bandit obtenez-vous, et de quel niveau ?",
   ["Sur mon code source, Bandit ne remonte aucune alerte (0 Low, 0 Medium, 0 High). Le defaut "
    "intentionnel evoque par l'atelier provient d'une variante vulnerable du code (par exemple "
    "une ecoute reseau sur 0.0.0.0 ecrite en Python), que mon implementation ne contient pas."])
qa("3.7", "Corrigez les alertes Bandit et confirmez 0 alerte HIGH ou MEDIUM.",
   ["Aucune alerte HIGH ou MEDIUM n'est a corriger, l'audit est deja a zero. L'ecoute sur "
    "0.0.0.0, necessaire au fonctionnement dans un conteneur, est confinee au Dockerfile, hors "
    "du perimetre analyse (src/). En relancant 'bandit -r src/', le resultat reste a 0 alerte."])
qa("3.8", "Quel score Pylint obtenez-vous une fois le pipeline vert ?",
   ["Pylint affiche un score de 9.61 sur 10, nettement au-dessus du seuil de 7.0 exige par le "
    "stage Lint. Le pipeline conserve donc ses six etapes au vert."])
add_screenshot("tp3_pipeline_green.png", caption="Figure 3.1 – Pipeline Jenkins avec 6 étapes vertes")
add_screenshot("tp3_pylint_score.png", caption="Figure 3.2 – Score Pylint : 9.61/10")
add_screenshot("tp3_bandit_zero.png", caption="Figure 3.3 – Bandit : 0 alerte")
sp(3)

# ============ TP4 ============
h1("7. TP4, TDD, performance et securite")
P("J'ai traite la gestion des negations en suivant le cycle TDD, mene des tests de charge avec "
  "Locust, et relance l'audit de securite.")
qa("4.1", "Pourquoi confirmer que les tests echouent avant d'ecrire le code ?",
   ["Confirmer l'echec prouve que le test verifie reellement la nouvelle fonctionnalite : il "
    "echoue parce que le comportement n'existe pas encore. Un test qui passerait avant meme "
    "d'ecrire le code serait trompeur, signe que ses assertions sont fausses ou qu'il ne teste "
    "pas ce que l'on croit."])
qa("4.2", "Les tests du TP1 passent-ils toujours apres l'ajout des negations ?",
   ["Oui, aucune regression. Le fichier test_model.py compte 27 tests au vert (18 du TP1 et 9 "
    "lies aux negations). L'implementation des negations n'a casse aucun comportement existant."])
qa("4.3", "Ajoutez un test parametrise couvrant au moins 4 cas de negation.",
   ["J'ai ecrit test_negation_parametrisee avec six cas, qui passe apres le refactor sans "
    "modifier le code de production : 'pas bien' donne NEGATIVE, 'jamais mauvais' donne "
    "POSITIVE, 'produit pas nul' donne POSITIVE, 'plus jamais super' donne NEGATIVE, "
    "'sans aucun defaut' donne NEUTRAL, et 'vraiment excellent' reste POSITIVE."])
qa("4.4", "Votre couverture a-t-elle augmente ou diminue par rapport au TP1 ?",
   ["La couverture de src/model.py reste a 100 pour cent, alors que le nombre d'instructions "
    "est passe de 24 a 37. Les nouvelles lignes (parcours des tokens, gestion du drapeau de "
    "negation, branches inversees) sont toutes exercees par les tests de negation, donc aucune "
    "nouvelle ligne non couverte."])
qa("4.5", "Pourquoi un poids de 3 pour /predict et de 1 pour /stats dans Locust ?",
   ["Le poids represente la frequence relative de selection d'une tache par un utilisateur "
    "virtuel. Un poids de 3 contre 1 signifie que /predict est appele environ trois fois plus "
    "souvent que /stats. Ce ratio reflete un usage reel, ou l'on analyse des textes bien plus "
    "frequemment qu'on ne consulte les statistiques."])
qa("4.6", "Resultats a 50 utilisateurs : le P95 de /predict est-il inferieur a 500 ms ?",
   ["Oui, tres largement. Voici les mesures relevees a 50 utilisateurs :"])
make_table([
    ["Endpoint", "Requetes", "P50", "P95", "Echecs"],
    ["POST /predict", "2162", "4 ms", "7 ms", "0"],
    ["GET /stats", "498", "3 ms", "6 ms", "0"],
], [5*cm, 3*cm, 2.5*cm, 2.5*cm, 2.5*cm])
sp(8)
qa("4.7", "Comment evolue la latence entre 50 et 100 utilisateurs ?",
   ["En doublant la charge, le P95 de /predict passe de 7 ms a 14 ms, sans aucune erreur "
    "supplementaire. L'API evolue de facon lineaire sur cette plage et dispose d'une marge "
    "confortable avant saturation."])
make_table([
    ["Charge", "Requetes", "P95 /predict", "Echecs"],
    ["50 utilisateurs", "2 660", "7 ms", "0"],
    ["100 utilisateurs", "4 993", "14 ms", "0"],
], [4*cm, 4*cm, 4*cm, 3.5*cm])
sp(8)
qa("4.8", "Combien d'alertes Bandit subsistent apres les modifications TDD ?",
   ["Aucune. L'ajout de la logique de negation n'a introduit ni eval, ni entree non validee, "
    "ni secret. Bandit reste a zero alerte et le code source demeure sain."])
qa("4.9", "Le pipeline reste-t-il vert, et pourquoi le TDD ameliore la couverture ?",
   ["Les six etapes restent vertes apres le commit. Le TDD ameliore mecaniquement la couverture "
    "car chaque test ecrit avant le code force l'execution de lignes nouvelles, qui passent de "
    "non couvertes a couvertes des qu'elles sont implementees."])
add_screenshot("tp4_tdd_tests.png", caption="Figure 4.1 – Tests de négation au vert")
add_screenshot("tp4_locust_results.png", caption="Figure 4.2 – Résultats Locust à 50 utilisateurs")
add_screenshot("tp4_pipeline_final.png", caption="Figure 4.3 – Pipeline final vert après TP4")
sp(3)
qa("4.10", "Recapitulatif des quatre defauts identifies et corriges.",
   ["Le tableau ci-dessous resume les quatre defauts rencontres au fil de l'atelier et la "
    "correction que j'ai appliquee a chacun."])
make_table([
    ["Etape", "Defaut", "Comment je l'ai detecte", "Correction apportee"],
    ["TP1", "Score depassant 1.0", "Test verifiant score <= 1.0", "Plafonnement par min(..., 1.0)"],
    ["TP2", "Tests dependants entre eux", "Inversion de l'ordre d'execution", "Fixture de reset automatique (autouse)"],
    ["TP3", "Qualite et securite du code", "Pylint et Bandit dans le pipeline", "Code maintenu propre (9.61/10, 0 alerte)"],
    ["TP4", "Negations ignorees", "Test TDD en phase RED", "Parcours des tokens avec drapeau de negation"],
], [1.5*cm, 3.6*cm, 4.6*cm, 5.3*cm])

# ============ CONCLUSION ============
h1("8. Conclusion")
P("Au terme de l'atelier, le projet dispose d'une suite de 42 tests, tous au vert, et d'une "
  "couverture globale de 98 pour cent (100 pour cent sur la logique metier). L'application est "
  "conteneurisee, passe les audits de qualite et de securite, et tient la charge avec une "
  "latence tres faible. L'ensemble s'integre dans un pipeline automatise reproductible.")
P("J'ai surtout retenu que les tests ne servent pas seulement a confirmer ce qui fonctionne, "
  "mais qu'ils revelent activement les defauts. Cette progression, du test unitaire le plus "
  "fin jusqu'au pipeline complet, m'a permis de comprendre concretement comment une equipe "
  "garantit la fiabilite d'un logiciel avant de le livrer, et pourquoi chaque test doit rester "
  "independant, lisible et reproductible.")

doc.build(story)
print("OK ->", OUTPUT)
