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
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        return render_template('welcome.html',club=club,competitions=competitions)
    except IndexError:
        flash("Sorry, that email wasn't found.")
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
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    
    # Validation des points du club
    if placesRequired > int(club['points']):
        flash('Not enough points available!')
        return render_template('welcome.html', club=club, competitions=competitions)
    
    # Validation des places disponibles
    if placesRequired > int(competition['numberOfPlaces']):
        flash('Not enough places available!')
        return render_template('welcome.html', club=club, competitions=competitions)
    
    # Validation du nombre maximum de places (12 max par club)
    if placesRequired > 12:
        flash('Cannot book more than 12 places!')
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
    