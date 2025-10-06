import json
from datetime import datetime
from flask import Flask,render_template,request,redirect,flash,url_for


def loadClubs():
    try:
        with open('clubs.json') as c:
             listOfClubs = json.load(c)['clubs']
             return listOfClubs
    except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
        print(f"❌ ERREUR: Impossible de charger clubs.json: {e}")
        return []


def loadCompetitions():
    try:
        with open('competitions.json') as comps:
             listOfCompetitions = json.load(comps)['competitions']
             return listOfCompetitions
    except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
        print(f"❌ ERREUR: Impossible de charger competitions.json: {e}")
        return []


def saveClubs(clubs_data):
    """Sauvegarde les données des clubs dans le fichier JSON"""
    try:
        with open('clubs.json', 'w') as c:
            json.dump({'clubs': clubs_data}, c, indent=4)
    except Exception as e:
        print(f"❌ ERREUR: Impossible de sauvegarder clubs.json: {e}")


def saveCompetitions(competitions_data):
    """Sauvegarde les données des compétitions dans le fichier JSON"""
    try:
        with open('competitions.json', 'w') as c:
            json.dump({'competitions': competitions_data}, c, indent=4)
    except Exception as e:
        print(f"❌ ERREUR: Impossible de sauvegarder competitions.json: {e}")


def is_competition_past(competition_date):
    """Vérifie si une compétition est dans le passé"""
    try:
        comp_date = datetime.strptime(competition_date, '%Y-%m-%d %H:%M:%S')
        return comp_date < datetime.now()
    except ValueError:
        return False


app = Flask(__name__)
app.secret_key = 'something_special'

# Chargement et validation des données
competitions = loadCompetitions()
clubs = loadClubs()

# Validation que les données sont chargées
if not competitions:
    print("❌ ERREUR CRITIQUE: Aucune compétition chargée!")
if not clubs:
    print("❌ ERREUR CRITIQUE: Aucun club chargé!")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    email = request.form.get('email', '').strip()
    
    # Validation de l'email
    if not email:
        flash('❌ ERREUR: Veuillez saisir un email!')
        return render_template('index.html')
    
    if '@' not in email or '.' not in email:
        flash('❌ ERREUR: Format d\'email invalide!')
        return render_template('index.html')
    
    try:
        club = [club for club in clubs if club['email'] == email][0]
        return render_template('welcome.html',club=club,competitions=competitions)
    except IndexError:
        flash('❌ ERREUR: Email non trouvé dans notre base de données!')
        return render_template('index.html')


@app.route('/book/<competition>/<club>')
def book(competition,club):
    # Validation des données d'entrée
    if not competition or not club:
        flash("❌ ERREUR: Paramètres manquants")
        return render_template('index.html')
    
    try:
        foundClub = [c for c in clubs if c['name'] == club][0]
        foundCompetition = [c for c in competitions if c['name'] == competition][0]
        
        # Validation que la compétition n'est pas dans le passé
        if is_competition_past(foundCompetition['date']):
            flash('❌ ERREUR: Cette compétition est dans le passé!')
            return render_template('welcome.html', club=foundClub, competitions=competitions)
        
        if foundClub and foundCompetition:
            return render_template('booking.html',club=foundClub,competition=foundCompetition)
        else:
            flash("❌ ERREUR: Quelque chose s'est mal passé, veuillez réessayer")
            return render_template('welcome.html', club=foundClub, competitions=competitions)
    except IndexError:
        flash("❌ ERREUR: Club ou compétition non trouvé")
        return render_template('index.html')


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    # Validation des données d'entrée
    if not request.form.get('competition') or not request.form.get('club') or not request.form.get('places'):
        flash("❌ ERREUR: Données manquantes dans le formulaire")
        return render_template('index.html')
    
    try:
        competition_name = request.form['competition'].strip()
        club_name = request.form['club'].strip()
        placesRequired = int(request.form['places'])
        
        # Validation que les noms ne sont pas vides
        if not competition_name or not club_name:
            flash("❌ ERREUR: Noms de compétition ou club invalides")
            return render_template('index.html')
            
        competition = [c for c in competitions if c['name'] == competition_name][0]
        club = [c for c in clubs if c['name'] == club_name][0]
        
    except (IndexError, ValueError, KeyError):
        flash("❌ ERREUR: Données invalides fournies")
        return render_template('index.html')
    
    # Validation du nombre minimum de places
    if placesRequired <= 0:
        flash('❌ ERREUR: Vous devez saisir un nombre de places supérieur à 0!')
        return render_template('welcome.html', club=club, competitions=competitions)
    
    # Protection contre les nombres trop grands (overflow)
    if placesRequired > 999999:
        flash('❌ ERREUR: Nombre de places trop élevé!')
        return render_template('welcome.html', club=club, competitions=competitions)
    
    # Validation des points du club avec gestion d'erreur
    try:
        club_points = int(club['points'])
        if placesRequired > club_points:
            flash('❌ ERREUR: Pas assez de points disponibles!')
            return render_template('welcome.html', club=club, competitions=competitions)
    except (ValueError, KeyError):
        flash('❌ ERREUR: Données du club corrompues!')
        return render_template('index.html')
    
    # Validation des places disponibles avec gestion d'erreur
    try:
        competition_places = int(competition['numberOfPlaces'])
        if placesRequired > competition_places:
            flash('❌ ERREUR: Pas assez de places disponibles dans cette compétition!')
            return render_template('welcome.html', club=club, competitions=competitions)
    except (ValueError, KeyError):
        flash('❌ ERREUR: Données de la compétition corrompues!')
        return render_template('index.html')
    
    # Validation du nombre maximum de places (12 max par club)
    if placesRequired > 12:
        flash('❌ ERREUR: Vous ne pouvez pas réserver plus de 12 places!')
        return render_template('welcome.html', club=club, competitions=competitions)
    
    # Validation que la compétition n'est pas dans le passé
    if is_competition_past(competition['date']):
        flash('❌ ERREUR: Vous ne pouvez pas réserver pour des compétitions passées!')
        return render_template('welcome.html', club=club, competitions=competitions)
    
    # Mise à jour des données avec validation
    try:
        new_competition_places = competition_places - placesRequired
        new_club_points = club_points - placesRequired
        
        # Validation que les nouvelles valeurs sont cohérentes
        if new_competition_places < 0 or new_club_points < 0:
            flash('❌ ERREUR: Calcul des nouvelles valeurs invalide!')
            return render_template('welcome.html', club=club, competitions=competitions)
        
        competition['numberOfPlaces'] = str(new_competition_places)
        club['points'] = str(new_club_points)
        
        # Sauvegarde des modifications
        saveClubs(clubs)
        saveCompetitions(competitions)
        
    except Exception as e:
        flash('❌ ERREUR: Impossible de mettre à jour les données!')
        return render_template('welcome.html', club=club, competitions=competitions)
    
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
    