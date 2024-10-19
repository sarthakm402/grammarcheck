import nltk 
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
import re
from spellchecker import SpellChecker
import spacy
from transformers import pipeline
from symspellpy.symspellpy import SymSpell, Verbosity
sample=" we is Sarthak ."
#### SENTENCE CORRECTION WITH OPEN SOURCE SOFTWARE and Library like Spellchecker####

sample = sample.lower()
sample=re.sub(r'[^a-z0-9\s]','', sample)
print(sample)
tokens=word_tokenize(sample)
# spell=SpellChecker()
# misspelled = spell.unknown(tokens)

# cor = [spell.correction(word) if word in misspelled and spell.correction(word) is not None else word for word in tokens]
# print(cor)
sym_spell = SymSpell(max_dictionary_edit_distance=2)
sym_spell.load_dictionary(r"frequency_bigramdictionary_en_243_342.txt", term_index=0, count_index=1)


custom_words = ["sarthak", "aditya"]

# Correct spelling using SymSpell
corrected_tokens = []
for word in tokens:
    if word not in custom_words:
        suggestions = sym_spell.lookup(word, Verbosity.CLOSEST, max_edit_distance=2)
        if suggestions:
            corrected_tokens.append(suggestions[0].term)
        else:
            corrected_tokens.append(word)
    else:
        corrected_tokens.append(word)

corrected_text = ' '.join(corrected_tokens)
print("Corrected Text:", corrected_text)

# Load SpaCy for further processing
nlp = spacy.load("en_core_web_sm")
doc = nlp(corrected_text)
def apply_grammar_rules(doc):
    subject = None
    verb_phrase = []
    object_ = []
    others = []

    for token in doc:
        if token.dep_ == "nsubj" and token.pos_ in ["PRON", "NOUN", "PROPN"]:  # Subject detection
            subject = token.text
        elif token.dep_ in ["aux", "ROOT", "auxpass"]:  # Verb detection
            verb_phrase.append(token.text)
        elif token.dep_ in ["attr", "dobj", "pobj", "obl"]:  # Object detection
            object_.append(token.text)
        else:
            others.append(token.text)

    sentence = ' '.join(filter(None, [
        subject,
        ' '.join(verb_phrase),
        ' '.join(object_),
        ' '.join(others)
    ]))

    return sentence

# Grammar model for final correction
hmodel = pipeline("text2text-generation", model='vennify/t5-base-grammar-correction')

def model(text):
    corrected_text = hmodel(text, max_new_tokens=len(text)//2, temperature=0.7, num_return_sequences=1,
                            do_sample=True, early_stopping=True)[0]['generated_text']
    return corrected_text

# # Apply grammar rules and pass it to the model
reordered_sentence = apply_grammar_rules(doc)
print("\nReordered Sentence:", reordered_sentence)

# Generate final corrected sentence
f_sentence = model(reordered_sentence)
print("\nFinal Sentence:", f_sentence)



#### SENTENCE CORRECTION WITH APIS###
import nltk 
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
import re
import google.generativeai as genai
genai.configure(api_key='API_KEY')
model = genai.GenerativeModel(model_name="gemini-1.0-pro")
sample=" helko I is Sarthak  and aditya he is my frend."
sample = sample.lower()
sample=re.sub(r'[^a-z0-9\s]', '', sample)
print(sample)
tokens=word_tokenize(sample)   
sent=' '.join(tokens)
full_prompt = f"Correct the sentence: '{sent}'."
final=model.generate_content(full_prompt)
print(final.text)
