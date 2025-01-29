

import spacy

nlp = spacy.load('en_core_web_sm')

def keyword_extractor(user_input):
    doc = nlp(user_input)

    keywords = []
    for token in doc:
        if token.pos_ in ['NOUN', 'PROPN', 'VERB']:
            keywords.append(token.text)

    return keywords


# Example chatbot function
# def chatbot():
#     print("Chatbot: Hello! How can I assist you today?")
#     while True:
#         user_input = input("You: ")
#         if user_input.lower() in ['exit', 'quit', 'bye']:
#             print("Chatbot: Goodbye!")
#             break
#
#         keywords = keyword_extractor(user_input)
#         print(f"Chatbot: I identified these keywords: {', '.join(keywords)}")
#
# chatbot()