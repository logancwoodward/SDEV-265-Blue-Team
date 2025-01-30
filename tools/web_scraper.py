
import spacy


nlp = spacy.load('en_core_web_sm')

def extract_keywords(text):
    """Extract keywords from text using spaCy."""
    doc = nlp(text)
    keywords = []
    for token in doc:
        if token.is_alpha and not token.is_stop:
            keywords.append(token.lemma_)
    return keywords
