# 🧪 SCÉNARIOS DE TEST - APPLICATION DE BOOKING

## 📋 **INFORMATIONS DE TEST**

### **Emails de test disponibles :**
- `john@simplylift.co` (13 points)
- `admin@irontemple.com` (4 points)  
- `kate@shelifts.co.uk` (12 points)

### **Compétitions disponibles :**
- **Spring Festival** : 25 places (Date: 2020-03-27 10:00:00) - ⚠️ **PASSÉE**
- **Fall Classic** : 13 places (Date: 2020-10-22 13:30:00) - ⚠️ **PASSÉE**

---

## 🚨 **SCÉNARIOS D'ERREURS À TESTER**

### **1. TEST DE CONNEXION - Emails invalides**

#### **Scénario 1.1 : Email inexistant**
- **Action** : Saisir un email qui n'existe pas
- **Email à tester** : `test@inexistant.com`
- **Résultat attendu** : Message d'erreur "Sorry, that email wasn't found."

#### **Scénario 1.2 : Email vide**
- **Action** : Laisser le champ email vide et cliquer sur "Enter"
- **Résultat attendu** : Validation HTML (champ requis)

#### **Scénario 1.3 : Format email invalide**
- **Action** : Saisir un format email invalide
- **Email à tester** : `email-invalide`
- **Résultat attendu** : Validation HTML (format email)

---

### **2. TEST DE RÉSERVATION - Cas limites**

#### **Scénario 2.1 : Plus de places que disponibles**
- **Connexion** : `john@simplylift.co` (13 points)
- **Compétition** : Spring Festival (25 places)
- **Places demandées** : 30
- **Résultat attendu** : "Not enough places available!"

#### **Scénario 2.2 : Plus de places que de points**
- **Connexion** : `admin@irontemple.com` (4 points)
- **Compétition** : Fall Classic (13 places)
- **Places demandées** : 10
- **Résultat attendu** : "Not enough points available!"

#### **Scénario 2.3 : Plus de 12 places (limite max)**
- **Connexion** : `john@simplylift.co` (13 points)
- **Compétition** : Spring Festival (25 places)
- **Places demandées** : 15
- **Résultat attendu** : "Cannot book more than 12 places!"

#### **Scénario 2.4 : Nombre négatif de places**
- **Connexion** : `john@simplylift.co` (13 points)
- **Compétition** : Spring Festival (25 places)
- **Places demandées** : -5
- **Résultat attendu** : Validation HTML (min="1")

#### **Scénario 2.5 : Zéro places**
- **Connexion** : `john@simplylift.co` (13 points)
- **Compétition** : Spring Festival (25 places)
- **Places demandées** : 0
- **Résultat attendu** : Validation HTML (min="1")

---

### **3. TEST DE RÉSERVATION - Cas de succès**

#### **Scénario 3.1 : Réservation normale**
- **Connexion** : `john@simplylift.co` (13 points)
- **Compétition** : Spring Festival (25 places)
- **Places demandées** : 5
- **Résultat attendu** : "Great-booking complete!" + Points mis à jour (8 points)

#### **Scénario 3.2 : Réservation maximum**
- **Connexion** : `kate@shelifts.co.uk` (12 points)
- **Compétition** : Fall Classic (13 places)
- **Places demandées** : 12
- **Résultat attendu** : "Great-booking complete!" + Points mis à jour (0 points)

---

### **4. TEST DE PERSISTANCE DES DONNÉES**

#### **Scénario 4.1 : Vérification de la sauvegarde**
- **Action** : Faire une réservation, puis redémarrer le serveur
- **Vérification** : Les points et places doivent être conservés
- **⚠️ ATTENTION** : Cette fonctionnalité a été supprimée dans votre version actuelle

---

### **5. TEST DES COMPÉTITIONS PASSÉES**

#### **Scénario 5.1 : Réservation pour compétition passée**
- **Connexion** : `john@simplylift.co` (13 points)
- **Compétition** : Spring Festival (2020-03-27) - PASSÉE
- **Places demandées** : 5
- **Résultat attendu** : "Cannot book places for past competitions!"
- **⚠️ ATTENTION** : Cette validation a été supprimée dans votre version actuelle

---

## 🔍 **TESTS DE NAVIGATION**

### **Scénario 6.1 : Navigation entre pages**
- **Action** : Se connecter → Voir les compétitions → Cliquer sur "Book Places" → Retourner
- **Vérification** : Navigation fluide, pas d'erreurs 404

### **Scénario 6.2 : Déconnexion**
- **Action** : Se connecter → Cliquer sur "Logout"
- **Résultat attendu** : Retour à la page d'accueil

---

## 📊 **RÉSULTATS ATTENDUS PAR SCÉNARIO**

| Scénario | Erreur attendue | Statut |
|----------|----------------|---------|
| 1.1 | Email inexistant | ✅ Fonctionne |
| 1.2 | Email vide | ✅ Validation HTML |
| 1.3 | Format invalide | ✅ Validation HTML |
| 2.1 | Trop de places | ✅ Fonctionne |
| 2.2 | Pas assez de points | ✅ Fonctionne |
| 2.3 | Plus de 12 places | ✅ Fonctionne |
| 2.4 | Nombre négatif | ❌ Validation supprimée |
| 2.5 | Zéro places | ❌ Validation supprimée |
| 3.1 | Réservation normale | ✅ Fonctionne |
| 3.2 | Réservation max | ✅ Fonctionne |
| 4.1 | Persistance | ❌ Fonctionnalité supprimée |
| 5.1 | Compétition passée | ❌ Validation supprimée |

---

## 🚀 **COMMENT PROCÉDER AUX TESTS**

1. **Démarrer le serveur** : `python server.py`
2. **Ouvrir le navigateur** : http://127.0.0.1:5000
3. **Suivre chaque scénario** dans l'ordre
4. **Noter les résultats** observés
5. **Comparer** avec les résultats attendus

---

## ⚠️ **ERREURS IDENTIFIÉES DANS VOTRE VERSION ACTUELLE**

1. **Validation HTML supprimée** : Les champs n'ont plus d'attributs `required`, `min`, `max`
2. **Messages flash supprimés** : Plus d'affichage des erreurs dans booking.html
3. **Persistance supprimée** : Les modifications ne sont plus sauvegardées
4. **Validation des dates supprimée** : Plus de vérification des compétitions passées
5. **Balise HTML incorrecte** : `</br>` au lieu de `<br />`

---

## 🎯 **OBJECTIF DES TESTS**

Vérifier que les corrections de base fonctionnent encore :
- ✅ Gestion des emails inexistants
- ✅ Validation des points et places
- ✅ Limite de 12 places maximum
- ✅ Navigation entre pages
- ❌ Validations HTML (supprimées)
- ❌ Persistance des données (supprimée)
- ❌ Validation des dates (supprimée)
