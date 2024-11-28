
# Grammarcheck
## Overview
 
This repository contains a GrammarCheck Model that performs grammar correction using two different methods:

Open Source Model: A grammar correction system built using a publicly available model and library.
Gemini API: A grammar correction system utilizing Gemini’s advanced API for NLP tasks. 
Both methods are implemented to provide grammar correction, with the flexibility to choose between free, open-source tools and the advanced capabilities of the Gemini API.

## Features
- Corrects grammatical errors in text.
- Provides two different approaches for grammar correction: open-source and API-based (Gemini API).
- Choose between free and open-source tools or advanced Gemini API capabilities.




## Installation

Install my-project with npm

```bash
 git clone https://github.com/sarthakm402/grammarcheck.git
 cd grammarcheck
```
    
## Usage
### Open Source
Simply pass your input text to the grammar_correction_open_source() function, and it will return the corrected version of the text.

 Pros:                      

- Free to use
- Customizable	
- Easy to modify and tweak.
Cons:
- May struggle with very complex sentences
- Limited to trained dataset capabilities
- Performance may vary for larger tasks
### API
This approach leverages the Gemini API to deliver superior performance with state-of-the-art grammar correction models.

Pros:                      

- Advanced performance	R
- Handles complex language effectively
- Fast and scalable
Cons:
- equires subscription to Gemini API
- No customization options
- Dependent on API availability
## Conclusion
This repository offers two distinct approaches for grammar correction:

#### Open Source Model: 
Ideal for smaller-scale projects 
free, and customizable.

#### Gemini API: 
Ideal for advanced, large-scale projects, with superior performance.
Both methods offer flexibility based on your project’s requirements.
