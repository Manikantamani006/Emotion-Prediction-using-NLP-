import streamlit as st
import pickle
import re
import string

# Set Page configuration
st.set_page_config(page_title="Emotion Classifier", page_icon="🎭", layout="centered")

# Load Pickle Artifacts
@st.cache_resource
def load_artifacts():
    with open('best_lr_model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
    with open('tfidf_vectorizer.pkl', 'rb') as vec_file:
        vectorizer = pickle.load(vec_file)
    with open('emotion_mapping.pkl', 'rb') as mapping_file:
        mapping = pickle.load(mapping_file)

    # Reverse mapping to get emotion name from predicted label index
    reverse_mapping = {v: k for k, v in mapping.items()}
    return model, vectorizer, reverse_mapping

try:
    model, vectorizer, reverse_mapping = load_artifacts()
except Exception as e:
    st.error(f"Error loading artifacts: {e}")

# Preprocessing Functions
def preprocess_text(text):
    # 1. Lowercase
    text = text.lower()
    # 2. Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    # 3. Remove numbers
    text = ''.join([i for i in text if not i.isdigit()])
    # 4. Remove URLs
    text = re.sub(r'https?:\S+|www\.\S+', '', text)
    # 5. Remove emojis and non-ASCII characters
    text = text.encode('ascii', 'ignore').decode('ascii')
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = ' '.join(text.split())
    return text

# Design the UI/UX
st.title("🎭 Emotion Classifier App")
st.write("Enter a text passage below to predict the underlying emotion.")

user_input = st.text_area("Your Text:", height=150, placeholder="Type how you feel today...")

# Emotion representation mapping
emotion_emojis = {
    'sadness': "😢 Sadness",
    'anger': "😡 Anger",
    'love': "❤️ Love",
    'surprise': "😲 Surprise",
    'fear': "😨 Fear",
    'joy': "😊 Joy"
}

if st.button("Classify Emotion", use_container_width=True):
    if user_input.strip() == "":
        st.warning("Please enter some text before processing.")
    else:
        # Preprocess input text
        clean_text = preprocess_text(user_input)

        # Vectorize text
        vectorized_text = vectorizer.transform([clean_text])

        # Predict class & probabilities
        prediction = model.predict(vectorized_text)[0]
        probabilities = model.predict_proba(vectorized_text)[0]

        predicted_emotion = reverse_mapping[prediction]
        emoji_name = emotion_emojis.get(predicted_emotion, predicted_emotion.capitalize())

        # Display results
        st.success(f"Predicted Emotion: **{emoji_name}**")

        # Display class probabilities visualizer
        st.write("### Confidence Levels:")
        for idx, prob in enumerate(probabilities):
            class_name = reverse_mapping[idx]
            emoji_label = emotion_emojis.get(class_name, class_name.capitalize())
            st.write(f"{emoji_label}: {prob:.2%}")
            st.progress(float(prob))
