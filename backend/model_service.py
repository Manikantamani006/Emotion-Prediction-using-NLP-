import os
import re
import string
import pickle
from pathlib import Path
from typing import Dict, Any, Tuple
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

class ModelService:
    def __init__(self, artifacts_dir: str | Path | None = None):
        if artifacts_dir is None:
            # Default to backend/artifacts or project root fallback
            current_dir = Path(__file__).resolve().parent
            primary = current_dir / "artifacts"
            fallback = current_dir.parent
            if (primary / "best_lr_model.pkl").exists():
                self.artifacts_dir = primary
            elif (fallback / "best_lr_model.pkl").exists():
                self.artifacts_dir = fallback
            else:
                self.artifacts_dir = primary
        else:
            self.artifacts_dir = Path(artifacts_dir)

        self.model = None
        self.vectorizer = None
        self.mapping = None
        self.reverse_mapping = None
        self.classes = []
        self.stop_words = set()
        self.is_loaded = False
        self.error_message = None

        self._ensure_nltk_resources()
        self.load_artifacts()

    def _ensure_nltk_resources(self):
        """Ensure necessary NLTK tokenizers and stopwords are available."""
        try:
            self.stop_words = set(stopwords.words('english'))
            _ = word_tokenize("init test")
        except LookupError:
            try:
                nltk.download('punkt', quiet=True)
                nltk.download('punkt_tab', quiet=True)
                nltk.download('stopwords', quiet=True)
                self.stop_words = set(stopwords.words('english'))
            except Exception as e:
                # If offline/download fails, use fallback standard English stopwords
                self.stop_words = {
                    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've",
                    "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his',
                    'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself',
                    'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom',
                    'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be',
                    'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a',
                    'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of',
                    'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through',
                    'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in',
                    'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here',
                    'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few',
                    'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same',
                    'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', "now"
                }

    def load_artifacts(self):
        """Loads model, vectorizer, and mapping once during initialization."""
        model_path = self.artifacts_dir / "best_lr_model.pkl"
        vec_path = self.artifacts_dir / "tfidf_vectorizer.pkl"
        mapping_path = self.artifacts_dir / "emotion_mapping.pkl"

        for p in [model_path, vec_path, mapping_path]:
            if not p.exists():
                err = f"Required ML artifact missing at {p}. Ensure all .pkl artifacts exist in the artifacts directory."
                self.error_message = err
                raise FileNotFoundError(err)

        try:
            with open(model_path, "rb") as f:
                self.model = pickle.load(f)
            with open(vec_path, "rb") as f:
                self.vectorizer = pickle.load(f)
            with open(mapping_path, "rb") as f:
                self.mapping = pickle.load(f)

            # Map index -> emotion name
            self.reverse_mapping = {int(v): str(k) for k, v in self.mapping.items()}
            self.classes = [self.reverse_mapping[i] for i in range(len(self.reverse_mapping))]
            self.is_loaded = True
            self.error_message = None
        except Exception as e:
            self.is_loaded = False
            self.error_message = f"Failed to load machine learning artifacts: {str(e)}"
            raise RuntimeError(self.error_message) from e

    def preprocess_text(self, text: str) -> Tuple[str, int]:
        """
        Preprocesses text strictly matching the training pipeline in main.ipynb:
        1. Lowercase
        2. Remove punctuation
        3. Remove numbers
        4. Remove URLs
        5. Remove non-ASCII/emojis, retain alphanumeric and space, collapse whitespace
        6. Tokenize with word_tokenize and remove English stopwords
        """
        # 1. Lowercase
        cleaned = text.lower()
        # 2. Remove punctuation
        cleaned = cleaned.translate(str.maketrans('', '', string.punctuation))
        # 3. Remove numbers
        cleaned = ''.join([c for c in cleaned if not c.isdigit()])
        # 4. Remove URLs
        cleaned = re.sub(r'https?:\S+|www\.\S+', '', cleaned)
        # 5. Remove emojis and non-ASCII characters
        cleaned = cleaned.encode('ascii', 'ignore').decode('ascii')
        cleaned = re.sub(r'[^a-zA-Z0-9\s]', '', cleaned)
        cleaned = ' '.join(cleaned.split())

        # 6. Stopwords removal using word_tokenize
        tokens = word_tokenize(cleaned)
        filtered_tokens = [tok for tok in tokens if tok.lower() not in self.stop_words]
        final_text = ' '.join(filtered_tokens)

        return final_text, len(filtered_tokens)

    def predict(self, text: str) -> Dict[str, Any]:
        """
        Runs full inference pipeline:
        Validation -> Preprocessing -> TF-IDF Transformation -> Model Prediction -> Probabilities
        """
        if not self.is_loaded:
            raise RuntimeError(f"Model service is not loaded: {self.error_message}")

        if not text or not text.strip():
            raise ValueError("Input text cannot be empty or whitespace only.")

        clean_text, token_count = self.preprocess_text(text)

        # Fallback if text only contained stopwords/punctuation so vectorizer can still analyze
        # e.g., if clean_text is empty, use the non-stopword alphanumeric string or return informative error
        inference_text = clean_text
        if not inference_text.strip():
            # If all words were stopwords, fallback to the alphanumeric cleaned text so that short phrases still produce a signal
            fallback_text = re.sub(r'[^a-zA-Z0-9\s]', '', text.lower()).strip()
            if not fallback_text:
                raise ValueError("Input text contains no valid linguistic characters.")
            inference_text = fallback_text

        # Vectorize
        vectorized = self.vectorizer.transform([inference_text])

        # Predict
        prediction_idx = int(self.model.predict(vectorized)[0])
        probabilities_raw = self.model.predict_proba(vectorized)[0]

        predicted_emotion = self.reverse_mapping.get(prediction_idx, f"unknown_{prediction_idx}")
        confidence = float(probabilities_raw[prediction_idx])

        # Build class-to-probability mapping in verified order
        probabilities = {}
        for idx, prob in enumerate(probabilities_raw):
            cls_name = self.reverse_mapping.get(idx, f"class_{idx}")
            probabilities[cls_name] = round(float(prob), 4)

        return {
            "predicted_emotion": predicted_emotion,
            "confidence": round(confidence, 4),
            "probabilities": probabilities,
            "cleaned_text": clean_text,
            "tokens_count": token_count,
            "raw_text": text
        }
