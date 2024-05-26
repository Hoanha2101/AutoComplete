from library import *
from utils import *

#Load tokenized_sentences_data that is set up.
with open("./data/tokenized_sentences_data.pickle", 'rb') as handle:
    tokenized_sentences_data = pickle.load(handle)

with open("./data/unique_words.pickle", 'rb') as handle:
    unique_words = pickle.load(handle)

start = 0

while True:
    if start == 0:
        print("Search:")
        print()
        input_sentence = ""
        start += 1
        
    origin_sentences = input_sentence
    input_sentence = input(input_sentence)
    input_sentence = origin_sentences + input_sentence
    
    if "-----" in input_sentence:
            break 
    
    if len(input_sentence.strip()) > 0 : 
        suggest_word = " "
        out_suggest = None
        if input_sentence[-1] == " ":
            out_suggest = suggest(input_sentence.strip(), tokenized_sentences_data, unique_words, k_smooth = 1)
            print("''''''",out_suggest)
        if out_suggest != None and len(out_suggest) > 0:
            print("Suggest:")
            for id in range(len(out_suggest)):
                suggest_word = out_suggest[id]
                print(f"({input_sentence + suggest_word})")
            print()
            input_sentence =  input_sentence + out_suggest[0]
        else:
            print("Suggest:")
            print(f"({suggest_word})")
            print()
            input_sentence =  input_sentence + suggest_word
    else:
        start = 0
        print("----Please enter input----")
