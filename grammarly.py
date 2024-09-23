import nltk 
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
import re
from spellchecker import SpellChecker
import spacy
from transformers import pipeline
sample="hellko i is Sarthak  and hee is Aditya my frend."

#tokenize
sample = sample.lower()
sample=re.sub(r'[^a-z0-9\s]', '', sample)
print(sample)
tokens=word_tokenize(sample)
spell=SpellChecker()
misspelled = spell.unknown(tokens)

corr = [spell.correction(word) if word in misspelled and spell.correction(word) is not None else word for word in tokens]
print(corr)
# pos_tags = pos_tag(cor)
# print("\nPOS Tags:")
# for token, pos in pos_tags:
#     print(f"{token}: {pos}")
corrected_text = ' '.join(corr)
nlp=spacy.load("en_core_web_sm")
doc=nlp(corrected_text)
def apply_grammar_rules(doc):
    subject = None
    verb_phrase = []
    object_ = None
    interjections = []
    others = []

    for token in doc:
        if token.pos_ == "INTJ":
            interjections.append(token.text)
        elif token.dep_ == "nsubj" and token.pos_ in ["PRON", "NOUN", "PROPN"]:
            subject = token.text
        elif token.dep_ in ["aux", "ROOT", "auxpass"]:
            verb_phrase.append(token.text)
        elif token.dep_ in ["attr", "dobj", "pobj", "obl"]:
            object_ = token.text
        else:
            others.append(token.text)
    
    sentence = ' '.join(filter(None, [
        ' '.join(interjections), 
        subject, 
        ' '.join(verb_phrase), 
        object_, 
        ' '.join(others)
    ]))
    
    return sentence
hmodel=pipeline("text2text-generation", model='vennify/t5-base-grammar-correction')
tok=len(sample)
def model(text):
    corrected_text = hmodel(text,max_new_tokens=tok//2, temperature=0.5, num_return_sequences=1,
            do_sample=False, early_stopping=True)[0]['generated_text']
    return corrected_text

reordered_sentence = apply_grammar_rules(doc)
print("\nReordered Sentence:", reordered_sentence)
f_sentence=model(reordered_sentence)
print("\nFinal Sentence:", f_sentence)
