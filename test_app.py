#!/usr/bin/env python3
"""
Script de test pour identifier les bugs fonctionnels de l'application de booking
"""

import json
import sys

def test_data_loading():
    """Test du chargement des données JSON"""
    print("🔍 Test du chargement des données...")
    
    try:
        with open('clubs.json', 'r') as f:
            clubs = json.load(f)['clubs']
        print(f"✅ {len(clubs)} clubs chargés")
        
        with open('competitions.json', 'r') as f:
            competitions = json.load(f)['competitions']
        print(f"✅ {len(competitions)} compétitions chargées")
        
        return clubs, competitions
    except Exception as e:
        print(f"❌ Erreur lors du chargement: {e}")
        return None, None

def test_data_validation(clubs, competitions):
    """Test de la validation des données"""
    print("\n🔍 Test de la validation des données...")
    
    # Test des clubs
    for club in clubs:
        if not club.get('name') or not club.get('email') or not club.get('points'):
            print(f"❌ Club invalide: {club}")
        else:
            try:
                points = int(club['points'])
                if points < 0:
                    print(f"⚠️  Club avec points négatifs: {club['name']}")
            except ValueError:
                print(f"❌ Points invalides pour {club['name']}: {club['points']}")
    
    # Test des compétitions
    for comp in competitions:
        if not comp.get('name') or not comp.get('date') or not comp.get('numberOfPlaces'):
            print(f"❌ Compétition invalide: {comp}")
        else:
            try:
                places = int(comp['numberOfPlaces'])
                if places < 0:
                    print(f"⚠️  Compétition avec places négatives: {comp['name']}")
            except ValueError:
                print(f"❌ Places invalides pour {comp['name']}: {comp['numberOfPlaces']}")
    
    print("✅ Validation des données terminée")

def test_business_logic():
    """Test de la logique métier"""
    print("\n🔍 Test de la logique métier...")
    
    # Test des règles métier
    print("📋 Règles métier à vérifier:")
    print("   - Maximum 12 places par réservation")
    print("   - Points du club >= places demandées")
    print("   - Places disponibles >= places demandées")
    print("   - Places demandées > 0")
    print("   - Validation des emails")
    print("   - Gestion des erreurs")

def main():
    """Fonction principale de test"""
    print("🚀 Démarrage des tests de l'application de booking\n")
    
    # Test 1: Chargement des données
    clubs, competitions = test_data_loading()
    if not clubs or not competitions:
        print("❌ Impossible de continuer les tests")
        sys.exit(1)
    
    # Test 2: Validation des données
    test_data_validation(clubs, competitions)
    
    # Test 3: Logique métier
    test_business_logic()
    
    print("\n✅ Tests terminés!")
    print("\n📝 Prochaines étapes:")
    print("   1. Lancer le serveur Flask")
    print("   2. Tester manuellement les fonctionnalités")
    print("   3. Vérifier les cas limites")

if __name__ == "__main__":
    main()
