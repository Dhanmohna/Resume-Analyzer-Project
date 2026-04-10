import spacy

#loading english model
nlp =spacy.load("en_core_web_sm")

def clean_text(text):
    doc = nlp(text)

    cleaned_tokens = []

    for token in doc:
        #removing stopwords,punctuation and spaces
        if token.is_stop or token.is_punct or token.is_space:
            continue

        #Keeping only meaningful words and lemmatizing them
        if token.is_alpha:
            cleaned_tokens.append(token.lemma_.lower())

    return cleaned_tokens        