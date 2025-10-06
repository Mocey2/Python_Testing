#!/usr/bin/env python3
"""
Script de test automatisé pour l'application de booking
"""

import json
import sys
from datetime import datetime

def load_test_data():
    """Charge les données de test"""
    try:
        with open('clubs.json', 'r') as f:
            clubs = json.load(f)['clubs']
        with open('competitions.json', 'r') as f:
            competitions = json.load(f)['competitions']
        return clubs, competitions
    except Exception as e:
        print(f"❌ Erreur lors du chargement des données: {e}")
        return None, None

def test_data_integrity(clubs, competitions):
    """Test l'intégrité des données"""
    print("🔍 Test de l'intégrité des données...")
    
    # Test des clubs
    for club in clubs:
        print(f"📋 Club: {club['name']}")
        print(f"   Email: {club['email']}")
        print(f"   Points: {club['points']}")
        
        # Vérification des points
        try:
            points = int(club['points'])
            if points < 0:
                print(f"   ⚠️  Points négatifs!")
            elif points == 0:
                print(f"   ⚠️  Aucun point disponible")
            else:
                print(f"   ✅ Points valides")
        except ValueError:
            print(f"   ❌ Points invalides: {club['points']}")
    
    # Test des compétitions
    for comp in competitions:
        print(f"🏆 Compétition: {comp['name']}")
        print(f"   Date: {comp['date']}")
        print(f"   Places: {comp['numberOfPlaces']}")
        
        # Vérification de la date
        try:
            comp_date = datetime.strptime(comp['date'], '%Y-%m-%d %H:%M:%S')
            now = datetime.now()
            if comp_date < now:
                print(f"   ⚠️  COMPÉTITION PASSÉE!")
            else:
                print(f"   ✅ Compétition future")
        except ValueError:
            print(f"   ❌ Date invalide: {comp['date']}")
        
        # Vérification des places
        try:
            places = int(comp['numberOfPlaces'])
            if places <= 0:
                print(f"   ⚠️  Aucune place disponible")
            else:
                print(f"   ✅ Places disponibles")
        except ValueError:
            print(f"   ❌ Places invalides: {comp['numberOfPlaces']}")

def generate_test_scenarios(clubs, competitions):
    """Génère des scénarios de test spécifiques"""
    print("\n🎯 Scénarios de test recommandés:")
    
    # Scénarios d'erreur
    print("\n🚨 TESTS D'ERREUR:")
    
    # Test 1: Email inexistant
    print("1. Email inexistant:")
    print("   - Email: test@inexistant.com")
    print("   - Résultat attendu: 'Sorry, that email wasn't found.'")
    
    # Test 2: Trop de places
    print("\n2. Trop de places:")
    for club in clubs:
        if int(club['points']) > 0:
            print(f"   - Club: {club['name']} ({club['points']} points)")
            print(f"   - Email: {club['email']}")
            print(f"   - Places à tester: {int(club['points']) + 5}")
            print("   - Résultat attendu: 'Not enough points available!'")
            break
    
    # Test 3: Plus de 12 places
    print("\n3. Plus de 12 places:")
    for club in clubs:
        if int(club['points']) >= 12:
            print(f"   - Club: {club['name']} ({club['points']} points)")
            print(f"   - Email: {club['email']}")
            print("   - Places à tester: 15")
            print("   - Résultat attendu: 'Cannot book more than 12 places!'")
            break
    
    # Test 4: Compétition passée
    print("\n4. Compétition passée:")
    for comp in competitions:
        try:
            comp_date = datetime.strptime(comp['date'], '%Y-%m-%d %H:%M:%S')
            if comp_date < datetime.now():
                print(f"   - Compétition: {comp['name']} ({comp['date']})")
                print("   - Résultat attendu: 'Cannot book places for past competitions!'")
                break
        except ValueError:
            continue
    
    # Scénarios de succès
    print("\n✅ TESTS DE SUCCÈS:")
    
    # Test 5: Réservation normale
    print("5. Réservation normale:")
    for club in clubs:
        if int(club['points']) >= 5:
            print(f"   - Club: {club['name']} ({club['points']} points)")
            print(f"   - Email: {club['email']}")
            print("   - Places à tester: 5")
            print("   - Résultat attendu: 'Great-booking complete!'")
            break

def check_current_issues():
    """Vérifie les problèmes actuels du code"""
    print("\n⚠️  PROBLÈMES IDENTIFIÉS DANS VOTRE VERSION:")
    
    issues = [
        "❌ Validation HTML supprimée (attributs required, min, max manquants)",
        "❌ Messages flash supprimés dans booking.html",
        "❌ Persistance des données supprimée (saveClubs, saveCompetitions)",
        "❌ Validation des compétitions passées supprimée",
        "❌ Balise HTML incorrecte (</br> au lieu de <br />)",
        "❌ Validation du nombre minimum de places supprimée"
    ]
    
    for issue in issues:
        print(f"   {issue}")
    
    print("\n💡 RECOMMANDATIONS:")
    print("   1. Tester d'abord les fonctionnalités de base qui marchent encore")
    print("   2. Vérifier que les corrections principales sont toujours actives")
    print("   3. Noter quelles validations ne fonctionnent plus")

def main():
    """Fonction principale"""
    print("🚀 DÉMARRAGE DES TESTS DE L'APPLICATION DE BOOKING\n")
    
    # Chargement des données
    clubs, competitions = load_test_data()
    if not clubs or not competitions:
        print("❌ Impossible de continuer les tests")
        sys.exit(1)
    
    # Test de l'intégrité des données
    test_data_integrity(clubs, competitions)
    
    # Génération des scénarios de test
    generate_test_scenarios(clubs, competitions)
    
    # Vérification des problèmes actuels
    check_current_issues()
    
    print("\n🎯 PRÊT POUR LES TESTS MANUELS!")
    print("   1. Lancez le serveur: python server.py")
    print("   2. Ouvrez: http://127.0.0.1:5000")
    print("   3. Suivez les scénarios ci-dessus")

if __name__ == "__main__":
    main()
