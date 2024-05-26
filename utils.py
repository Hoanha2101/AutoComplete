from library import *

def split_to_sentences(data):
    """
    Split data by linebreak "\n"
    
    Args:
        data: str
    
    Returns:
        A list of sentences
    """
    sentences = data.split('\n')
    
    # Additional clearning (This part is already implemented)
    # - Remove leading and trailing spaces from each sentence
    # - Drop sentences if they are empty strings.
    sentences = [s.strip() for s in sentences]
    sentences = [s for s in sentences if len(s) > 0]
    
    return sentences 

def tokenize_sentences(sentences):
    """
    Tokenize sentences into tokens (words)
    
    Args:
        sentences: List of strings
    
    Returns:
        List of lists of tokens
    """

    # Initialize the list of lists of tokenized sentences
    tokenized_sentences = []
    # Go through each sentence
    for sentence in sentences: # complete this line
        
        # Convert to lowercase letters
        sentence = sentence.lower()
        
        # Convert into a list of words
        tokenized = nltk.word_tokenize(sentence)

        # append the list of words to the list of lists
        tokenized_sentences.append(tokenized)

    return tokenized_sentences


def get_tokenized_data(data):
    """
    Make a list of tokenized sentences
    
    Args:
        data: String
    
    Returns:
        List of lists of tokens
    """
    # Get the sentences by splitting up the data
    sentences = split_to_sentences(data)
    
    # Get the list of lists of tokens by tokenizing the sentences
    tokenized_sentences = tokenize_sentences(sentences)
    
    return tokenized_sentences

def count_words(tokenized_sentences):
    """
    Count the number of word appearence in the tokenized sentences
    
    Args:
        tokenized_sentences: List of lists of strings
    
    Returns:
        dict that maps word (str) to the frequency (int)
    """
            
    word_counts = {}
    
    # Loop through each sentence
    for sentence in tokenized_sentences: # complete this line
        
        # Go through each token in the sentence
        for token in sentence: # complete this line

            # If the token is not in the dictionary yet, set the count to 1
            if token not in word_counts.keys(): # complete this line with the proper condition
                word_counts[token] = 1
            
            # If the token is already in the dictionary, increment the count by 1
            else:
                word_counts[token] += 1
    
    return word_counts


#Hàm có công dụng trích ra những từ có số lần xuất hiện trên 1 threshold quy định
def get_words_with_nplus_frequency(tokenized_sentences, count_threshold):
    """
    Find the words that appear N times or more
    
    Args:
        tokenized_sentences: List of lists of sentences
        count_threshold: minimum number of occurrences for a word to be in the closed vocabulary.
    
    Returns:
        List of words that appear N times or more
    """

    closed_vocab = []
    
    word_counts = count_words(tokenized_sentences)
    
    closed_vocab = [word for word, cnt in word_counts.items() if cnt >= count_threshold]

    return closed_vocab

# UNIT TEST COMMENT: Candidate for Table Driven Tests 
### UNQ_C6 GRADED_FUNCTION: replace_oov_words_by_unk ###
def replace_oov_words_by_unk(tokenized_sentences, vocabulary, unknown_token="<unk>"):
    """
    Replace words not in the given vocabulary with '<unk>' token.
    
    Args:
        tokenized_sentences: List of lists of strings
        vocabulary: List of strings that we will use
        unknown_token: A string representing unknown (out-of-vocabulary) words
    
    Returns:
        List of lists of strings, with words not in the vocabulary replaced
    """
    
    # Place vocabulary into a set for faster search
    vocabulary = set(vocabulary)
    
    # Initialize a list that will hold the sentences
    # after less frequent words are replaced by the unknown token
    replaced_tokenized_sentences = []
    
    # Go through each sentence
    for sentence in tokenized_sentences:
        
        # Initialize the list that will contain
        # a single sentence with "unknown_token" replacements
        replaced_sentence = []

        # for each token in the sentence
        for token in sentence: # complete this line
            
            # Check if the token is in the closed vocabulary
            if token in vocabulary: # complete this line with the proper condition
                # If so, append the word to the replaced_sentence
                replaced_sentence.append(token)
            else:
                # otherwise, append the unknown token instead
                replaced_sentence.append(unknown_token)

        # Append the list of tokens to the list of lists
        replaced_tokenized_sentences.append(replaced_sentence)
        
    return replaced_tokenized_sentences

def count_n_grams(data, n, start_token='<s>', end_token = '<e>'):
    """
    Count all n-grams in the data
    
    Args:
        data: List of lists of words
        n: number of words in a sequence
    
    Returns:
        A dictionary that maps a tuple of n-words to its frequency
    """
    
    # Initialize dictionary of n-grams and their counts
    n_grams = {}

    # Go through each sentence in the data
    for sentence in data: # complete this line
        
        # prepend start token n times, and  append the end token one time
        sentence = [start_token] * n + sentence + [end_token]
        
        # convert list to tuple
        # So that the sequence of words can be used as
        # a key in the dictionary
        sentence = tuple(sentence)
        
        # Use 'i' to indicate the start of the n-gram
        # from index 0
        # to the last index where the end of the n-gram
        # is within the sentence.
        
        for i in range(len(sentence) if n==1 else len(sentence)-n+1): # complete this line

            # Get the n-gram from i to i+n
            n_gram = sentence[i:i+n]
            
            # check if the n-gram is in the dictionary
            if n_gram in n_grams.keys(): # complete this line with the proper condition
            
                # Increment the count for this n-gram
                n_grams[n_gram] += 1
            else:
                # Initialize this n-gram count to 1
                n_grams[n_gram] = 1

    return n_grams

def estimate_probability(previous_n_gram, word, 
                         n_gram_counts, n_plus1_gram_counts, vocabulary_size, k=1.0):
    """
    Estimate the probabilities of a next word using the n-gram counts with k-smoothing
    
    Args:
        word: next word
        previous_n_gram: A sequence of words of length n
        n_gram_counts: Dictionary of counts of n-grams
        n_plus1_gram_counts: Dictionary of counts of (n+1)-grams
        vocabulary_size: number of words in the vocabulary
        k: positive constant, smoothing parameter
    
    Returns:
        A probability
    """
    # convert list to tuple to use it as a dictionary key
    previous_n_gram = tuple(previous_n_gram)
    
    # Set the denominator
    # If the previous n-gram exists in the dictionary of n-gram counts,
    # Get its count.  Otherwise set the count to zero
    # Use the dictionary that has counts for n-grams
    previous_n_gram_count = n_gram_counts[previous_n_gram] if previous_n_gram in n_gram_counts else 0
       
    # Calculate the denominator using the count of the previous n gram
    # and apply k-smoothing
    denominator = previous_n_gram_count + vocabulary_size*k
    
    # Define n plus 1 gram as the previous n-gram plus the current word as a tuple
    n_plus1_gram = previous_n_gram+(word,)
    
    # Set the count to the count in the dictionary,
    # otherwise 0 if not in the dictionary
    # use the dictionary that has counts for the n-gram plus current word    
    n_plus1_gram_count = n_plus1_gram_counts[n_plus1_gram] if n_plus1_gram in n_plus1_gram_counts else 0
            
    # Define the numerator use the count of the n-gram plus current word,
    # and apply smoothing
    numerator = n_plus1_gram_count+k
        
    # Calculate the probability as the numerator divided by denominator
    probability = numerator/denominator
    
    return probability

def max_delete(probability_list,token_list,index_del):
    probability_list.pop(index_del)
    token_list.pop(index_del)
    index_max = probability_list.index(max(probability_list))
    token = token_list[index_max]
    return probability_list, token_list, index_max, token

def suggest(previous_sentence, tokenized_sentences_data, unique_words, k_smooth = 1):
    words = previous_sentence.split(" ")
    len_words = len(words)
    
    previous_gram = count_n_grams(tokenized_sentences_data, len_words)
    plus_gram = count_n_grams(tokenized_sentences_data, len_words + 1)
    
    probability_list = []
    token_list = []
    
    for token in unique_words:
        tmp_prob = estimate_probability(words, token, 
                                previous_gram, plus_gram, len(unique_words), k=k_smooth)
        probability_list.append(tmp_prob)
        token_list.append(token)
    index_token = probability_list.index(max(probability_list))
    if index_token == 0:
        return ""
    else:
        
        next_word_1 = token_list[index_token]
        probability_list, token_list, index_token, next_word_2 = max_delete(probability_list,token_list,index_token)
        probability_list, token_list, index_token, next_word_3 = max_delete(probability_list,token_list,index_token)
        probability_list, token_list, index_token, next_word_4 = max_delete(probability_list,token_list,index_token)
        probability_list, token_list, index_token, next_word_5 = max_delete(probability_list,token_list,index_token)
        probability_list, token_list, index_token, next_word_6 = max_delete(probability_list,token_list,index_token)
        probability_list, token_list, index_token, next_word_7 = max_delete(probability_list,token_list,index_token)
        probability_list, token_list, index_token, next_word_8 = max_delete(probability_list,token_list,index_token)
        probability_list, token_list, index_token, next_word_9 = max_delete(probability_list,token_list,index_token)
        probability_list, token_list, index_token, next_word_10 = max_delete(probability_list,token_list,index_token)
        
        return next_word_1, next_word_2, next_word_3, next_word_4, next_word_5, next_word_6, next_word_7, next_word_8, next_word_9, next_word_10


def options(input_sentence, tokenized_sentences_data, unique_words):
  
    if len(input_sentence.strip()) > 0:
        suggest_word = " "
        out_suggest = None
        if input_sentence[-1] == " ":
            out_suggest = suggest(input_sentence.strip(), tokenized_sentences_data, unique_words, k_smooth=1)

        if out_suggest is not None and len(out_suggest) > 0:
            list_suggest = [None]
            for id in range(len(out_suggest)):
                suggest_word = out_suggest[id]
                suggested_sentence = input_sentence + suggest_word
                list_suggest.append(suggested_sentence)
            return list_suggest
        else:
            suggested_sentence = input_sentence + suggest_word
            return [None,suggested_sentence]
    else:
        return [None]
    