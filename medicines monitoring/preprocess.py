import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

def predict_quality(ingredients):
    vectorizer, model = pickle.load(open("ml_model/model.pkl", "rb"))
    input_vector = vectorizer.transform([ingredients])
    return model.predict(input_vector)[0]
