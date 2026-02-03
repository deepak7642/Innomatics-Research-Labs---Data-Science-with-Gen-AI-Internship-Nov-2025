# =========================================
# STREAMLIT SENTIMENT ANALYSIS APP
# =========================================

import streamlit as st
import joblib
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download once (safe for Streamlit)
nltk.download("stopwords")
nltk.download("wordnet")

# =========================================
# LOAD MODEL & VECTORIZER
# =========================================
model = joblib.load("sentiment_model.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")

# =========================================
# TEXT PREPROCESSING (SAME AS TRAINING)
# =========================================
stop_words = set(stopwords.words("english")) - {"not", "no", "never"}
lemmatizer = WordNetLemmatizer()

def preprocess(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"[^a-z\s]", "", text)
    words = text.split()
    words = [lemmatizer.lemmatize(w) for w in words if w not in stop_words]
    return " ".join(words)

# =========================================
# STREAMLIT UI
# =========================================
st.set_page_config(page_title="Flipkart Sentiment Analysis", layout="centered")

st.title("🛒 Flipkart Review Sentiment Analysis")
st.write("Enter a product review and predict its sentiment")

review_text = st.text_area(
    "Enter your review here:",
    height=150,
    placeholder="Example: This product quality is amazing and worth the price!"
)

if st.button("Predict Sentiment"):
    if review_text.strip() == "":
        st.warning("Please enter a review text.")
    else:
        clean_text = preprocess(review_text)
        vectorized_text = vectorizer.transform([clean_text])
        prediction = model.predict(vectorized_text)[0]

        if prediction == 1:
            st.success("✅ Positive Review")
        else:
            st.error("❌ Negative Review")

# =========================================
# FOOTER
# =========================================
st.markdown("---")
st.markdown("**Model:** TF-IDF + Logistic Regression")
st.markdown("**Metric Used:** F1-score")
