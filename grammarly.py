import nltk 
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
import re
from spellchecker import SpellChecker
import spacy
from transformers import pipeline
sample="hellko me is Sarthak ."

#tokenize
sample = sample.lower()
sample=re.sub(r'[^a-z0-9\s]', '', sample)
print(sample)
tokens=word_tokenize(sample)
spell=SpellChecker()
misspelled = spell.unknown(tokens)

cor = [spell.correction(word) if word in misspelled and spell.correction(word) is not None else word for word in tokens]
print(cor)
# pos_tags = pos_tag(cor)
# print("\nPOS Tags:")
# for token, pos in pos_tags:
#     print(f"{token}: {pos}")
corrected_text = ' '.join(cor)
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

        sentence = ' '.join(filter(None, [' '.join(interjections), subject, ' '.join(verb_phrase), object_, ' '.join(others)]))
    
    return sentence


def model(text):
    # Load the pre-trained model and tokenizer
    hmodel=pipeline("text2text-generation", model='google/flan-t5-large')
    corrected_text = hmodel(text)[0]['generated_text']
    return corrected_text

reordered_sentence = apply_grammar_rules(doc)
print("\nReordered Sentence:", reordered_sentence)
f_sentence=model(reordered_sentence)
print("\nFinal Sentence:", f_sentence)