import os
import pandas as pd
import re
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import nltk

# Make sure to download required NLTK packages if not already downloaded

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('punkt_tab')

# Load Stop Words from the provided folder
stopwords_dir = 'C:/Blackoffer/StopWords'  # Adjust with the actual path
stop_words = set()

for file in os.listdir(stopwords_dir):
    if file.endswith(".txt"):
        with open(os.path.join(stopwords_dir, file), 'r') as f:
            stop_words.update([line.strip().lower() for line in f])

# Load Positive and Negative Words from the Master Dictionary
master_dict_dir = 'C:/Blackoffer/MasterDictionary'  # Adjust with the actual path
positive_words = set()
negative_words = set()

with open(os.path.join(master_dict_dir, 'positive-words.txt'), 'r') as f:
    positive_words.update([line.strip().lower() for line in f if line.strip() and not line.startswith(";")])

with open(os.path.join(master_dict_dir, 'negative-words.txt'), 'r') as f:
    negative_words.update([line.strip().lower() for line in f if line.strip() and not line.startswith(";")])

# Helper functions for textual analysis
def clean_text(text):
    """Cleans the text by removing stopwords and punctuation."""
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    tokens = word_tokenize(text.lower())
    cleaned_tokens = [word for word in tokens if word not in stop_words]
    return cleaned_tokens

def positive_score(text):
    """Calculates the positive score."""
    return sum(1 for word in text if word in positive_words)

def negative_score(text):
    """Calculates the negative score."""
    return sum(1 for word in text if word in negative_words)

def polarity_score(pos_score, neg_score):
    """Calculates the polarity score."""
    return (pos_score - neg_score) / ((pos_score + neg_score) + 0.000001)

def subjectivity_score(pos_score, neg_score, total_words):
    """Calculates the subjectivity score."""
    return (pos_score + neg_score) / (total_words + 0.000001)

def avg_sentence_length(text, num_sentences):
    """Calculates the average sentence length."""
    return len(text) / num_sentences

def percentage_complex_words(complex_words, total_words):
    """Calculates the percentage of complex words."""
    return (complex_words / total_words) * 100

def fog_index(avg_sentence_len, perc_complex_words):
    """Calculates the Fog Index."""
    return 0.4 * (avg_sentence_len + perc_complex_words)

def complex_word_count(text):
    """Counts the complex words in the text."""
    return sum(1 for word in text if syllable_count(word) > 2)

def syllable_count(word):
    """Counts the syllables in a word."""
    vowels = 'aeiou'
    word = word.lower()
    count = sum(1 for char in word if char in vowels)

    if word.endswith('es') or word.endswith('ed'):
        count -= 1

    return max(1, count)

def personal_pronouns(text):
    """Counts personal pronouns in the text."""
    pronouns = re.findall(r'\b(I|we|my|ours|us)\b', ' '.join(text), re.I)
    return len(pronouns)

def avg_word_length(text):
    """Calculates the average word length."""
    return sum(len(word) for word in text) / len(text)

# Load input and output files
input_df = pd.read_excel('C:/Blackoffer/Input.xlsx')
output_structure_df = pd.read_excel('C:/Blackoffer/Output Data Structure.xlsx')

# Prepare output DataFrame
output_df = pd.DataFrame(columns=output_structure_df.columns)

# Perform analysis on each article
rows_list = []
for index, row in input_df.iterrows():
    url_id = row['URL_ID']
    file_path = os.path.join('C:/Blackoffer/extracted_articles', f"{url_id}.txt")
    
    # Read the article text
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()

        # Tokenize text
        sentences = sent_tokenize(text)
        words = clean_text(text)
        num_sentences = len(sentences)
        total_words = len(words)
        
        # Compute variables
        pos_score = positive_score(words)
        neg_score = negative_score(words)
        pol_score = polarity_score(pos_score, neg_score)
        subj_score = subjectivity_score(pos_score, neg_score, total_words)
        avg_sent_len = avg_sentence_length(words, num_sentences)
        complex_words = complex_word_count(words)
        perc_complex_words = percentage_complex_words(complex_words, total_words)
        fog_idx = fog_index(avg_sent_len, perc_complex_words)
        avg_words_per_sent = avg_sentence_length(words, num_sentences)
        syllables_per_word = sum(syllable_count(word) for word in words) / total_words
        personal_pronoun_count = personal_pronouns(words)
        avg_word_len = avg_word_length(words)

        # Prepare output row
        output_row = {
            'URL_ID': url_id,
            'POSITIVE SCORE': pos_score,
            'NEGATIVE SCORE': neg_score,
            'POLARITY SCORE': pol_score,
            'SUBJECTIVITY SCORE': subj_score,
            'AVG SENTENCE LENGTH': avg_sent_len,
            'PERCENTAGE OF COMPLEX WORDS': perc_complex_words,
            'FOG INDEX': fog_idx,
            'AVG NUMBER OF WORDS PER SENTENCE': avg_words_per_sent,
            'COMPLEX WORD COUNT': complex_words,
            'WORD COUNT': total_words,
            'SYLLABLE PER WORD': syllables_per_word,
            'PERSONAL PRONOUNS': personal_pronoun_count,
            'AVG WORD LENGTH': avg_word_len
        }
        
        # Add input variables from 'Input.xlsx'
        for col in input_df.columns:
            output_row[col] = row[col]

        rows_list.append(output_row)

    except Exception as e:
        print(f"Error processing file {file_path}: {e}")


# Concatenate the list of rows into the DataFrame
if rows_list:  # Check if rows_list is not empty
    new_rows_df = pd.DataFrame(rows_list)  
    output_df = pd.concat([output_df, new_rows_df], ignore_index=True)

# Save the final output if output_df is not empty
if not output_df.empty:
    output_df.to_excel('C:/Blackoffer/output.xlsx', index=False)
else:
    print("No data to save in the output file.")
