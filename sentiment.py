import joblib
from textblob import TextBlob
import os

# Charger le modèle entraîné
model_path = os.path.join('Users/abderramanbensalah/Desktop/IA/Movie_reviews/WebScrapping_project/', 'sentiment_model.pkl')
model = joblib.load("./sentiment_model.pkl")

# Fonction pour prédire le sentiment d'un commentaire
def predict_sentiment(comment):
    # Utiliser TextBlob pour calculer la polarité du commentaire
    polarity = TextBlob(comment).sentiment.polarity
    # Transformer la polarité en une prédiction binaire (0 pour négatif, 1 pour positif)
    prediction = 1 if polarity > 0 else 0
    return prediction

# Fonction principale pour tester le modèle
def main():
    # Saisir un commentaire à tester
    comment = input("Entrez votre commentaire : ")
    # Faire une prédiction
    prediction = predict_sentiment(comment)
    # Afficher le résultat
    if prediction == 1:
        print("Le commentaire est prédit comme positif.")
    else:
        print("Le commentaire est prédit comme négatif.")

if __name__ == "__main__":
    main()
