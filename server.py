import json
from flask import Flask,render_template,request,redirect,flash,url_for


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

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
    try:
        foundClub = [c for c in clubs if c['name'] == club][0]
        foundCompetition = [c for c in competitions if c['name'] == competition][0]
        if foundClub and foundCompetition:
            return render_template('booking.html',club=foundClub,competition=foundCompetition)
        else:
            flash("Something went wrong-please try again")
            return render_template('welcome.html', club=foundClub, competitions=competitions)
    except IndexError:
        flash("Club or competition not found")
        return render_template('index.html')


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    try:
        competition = [c for c in competitions if c['name'] == request.form['competition']][0]
        club = [c for c in clubs if c['name'] == request.form['club']][0]
        placesRequired = int(request.form['places'])
    except (IndexError, ValueError, KeyError):
        flash("Invalid data provided. Please try again.")
        return render_template('index.html')
    
    # Validation du nombre minimum de places
    if placesRequired <= 0:
        flash('❌ ERREUR: Vous devez saisir un nombre de places supérieur à 0!')
        return render_template('welcome.html', club=club, competitions=competitions)
    
    # Validation des points du club
    if placesRequired > int(club['points']):
        flash('❌ ERREUR: Pas assez de points disponibles!')
        return render_template('welcome.html', club=club, competitions=competitions)
    
    # Validation des places disponibles
    if placesRequired > int(competition['numberOfPlaces']):
        flash('❌ ERREUR: Pas assez de places disponibles dans cette compétition!')
        return render_template('welcome.html', club=club, competitions=competitions)
    
    # Validation du nombre maximum de places (12 max par club)
    if placesRequired > 12:
        flash('❌ ERREUR: Vous ne pouvez pas réserver plus de 12 places!')
        return render_template('welcome.html', club=club, competitions=competitions)
    
    # Mise à jour des données
    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
    club['points'] = str(int(club['points']) - placesRequired)
    
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
    