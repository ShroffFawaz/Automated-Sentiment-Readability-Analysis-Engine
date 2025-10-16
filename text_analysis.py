import pandas as pd # type: ignore
import os
import numpy as np # type: ignore
import re
import codecs
from nltk.tokenize import sent_tokenize,word_tokenize # type: ignore


def read_all_txt_files(directory_path):
    """
    Read all .txt files in a directory
    """
    all_files = os.listdir(directory_path)
    txt_files = [f for f in all_files if f.endswith('.txt')]
    
    files_content = {}
    
    for txt_file in txt_files:
        file_path = os.path.join(directory_path, txt_file)
        try:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
                files_content[txt_file] = file.read()
        except Exception as e:
            print(f"Error reading {txt_file}: {e}")
    
    return files_content


def read_all_txt_files_from_directory(directory_path):
    """
    Read all .txt files in a directory
    """
    all_files = os.listdir(directory_path)
    txt_files = [f for f in all_files if f.endswith('.txt')]
    
    files_content_dir = {}
    
    for txt_file in txt_files:
        file_path = os.path.join(directory_path, txt_file)
        try:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
                files_content_dir[txt_file] = file.read()
        except Exception as e:
            print(f"Error reading {txt_file}: {e}")
    
    return files_content_dir



def combine_all_stopwords(stopwords_data):
    all_stopwords=set()
    
    for filename,content in stopwords_data.items():
        words=content.splitlines()
        all_stopwords.update(word.strip().lower() for word in words if word.strip())

    return all_stopwords

def preprocess_text(content,stopwords_set):
        #Converting text into lowercase
        content=content.lower()
        #Tokenization
        sentences=sent_tokenize(content) # Sentence tokenization

        tokenization_sentence=[word_tokenize(sentence) for sentence in sentences ] # Word tokenization

        #Remove stopwords
        no_stopwords=[]
        for sentence in tokenization_sentence:
            clean_sentence=[]
            for w in sentence:
                if w.lower() not in stopwords_set:
                    clean_sentence.append(w)
            no_stopwords.append(clean_sentence)
        #Remove punctuation
        final_clean=[]
        for sentence in no_stopwords:
            clean_sentence=[]
            for w in sentence:
                if isinstance(w,str):
                    res=re.sub(r'[^\w\s]',"",w)
                    if res != "":
                        clean_sentence.append(res)
            final_clean.append(clean_sentence)
        
        return final_clean


def main():
    articles_directory  = r"C:\Users\Sam\Downloads\extracted_articles"
    stopwords_directory  = r"C:\Users\Sam\Downloads\Stopwords"
    contents = read_all_txt_files(articles_directory) # type: ignore
    stopwords_data = read_all_txt_files_from_directory(stopwords_directory)
    all_stopwords = combine_all_stopwords(stopwords_data)
    processed_files={}
    for filename, content in contents.items():
        print(f"Processing: {filename}")
        processed_content =preprocess_text(content,all_stopwords)
        processed_files[filename]=processed_content
if __name__=="__main__":
    main()



def main():
    articles_directory = r"C:\Users\Sam\Downloads\extracted_articles"
    stopwords_directory = r"C:\Users\Sam\Downloads\Stopwords"
    
    # Read the output file structure at the beginning
    df_output = pd.read_excel(r"C:\Users\Sam\Downloads\Output Data Structure.xlsx")
    
    contents = read_all_txt_files(articles_directory)
    stopwords_data = read_all_txt_files_from_directory(stopwords_directory)
    all_stopwords = combine_all_stopwords(stopwords_data)
    processed_files = {}
    
    # Load positive/negative words ONCE outside the loop
    df_pos = pd.read_csv(r"C:\Users\Sam\Downloads\drive-download-20251011T180633Z-1-001\positive-words.txt", encoding='latin-1')  
    df_neg = pd.read_csv(r"C:\Users\Sam\Downloads\drive-download-20251011T180633Z-1-001\negative-words.txt", encoding='latin-1')
    
    # Convert to FLAT lists of words
    pos_words = df_pos.to_numpy().flatten().tolist()
    neg_words = df_neg.to_numpy().flatten().tolist()
    
    print(f"Loaded {len(pos_words)} positive words and {len(neg_words)} negative words")
    
    # Define helper functions for text analysis
    def count_syllables(word):
        """Count syllables in a word."""
        word = word.lower()
        # Remove non-alphabetic characters
        word = re.sub(r'[^a-z]', '', word)

        # If word is empty after cleaning, return 0
        if not word:
            return 0

        vowels = "aeiou"
        syllable_count = 0
        prev_char_was_vowel = False

        for char in word:
            if char in vowels:
                if not prev_char_was_vowel:
                    syllable_count += 1
                prev_char_was_vowel = True
            else:
                prev_char_was_vowel = False

        # Handle silent endings
        if word.endswith(("es", "ed")) and syllable_count > 1:
            syllable_count -= 1

        # Ensure at least 1 syllable
        return max(1, syllable_count)

    def count_complex_words(words):
        """Return the number of complex words (more than 2 syllables)."""
        complex_words = [word for word in words if count_syllables(word) > 2]
        return len(complex_words)
    
    def count_personal_pronouns(text):
        """Count personal pronouns in text."""
        pattern = r'\b(I|we|my|ours|us)\b'
        matches = re.findall(pattern, text, flags=re.IGNORECASE)
        filtered = [m for m in matches if m.lower() != 'us' or not re.match(r'\bUS\b', m)]
        return len(filtered)
    
    # Create a list to store all results
    all_results = []
    
    for filename, content in contents.items():
        print(f"Processing: {filename}")
        processed_content = preprocess_text(content, all_stopwords)
        processed_files[filename] = processed_content
        print(f"Completed preprocessing: {filename}")
        print("-" * 50)
        
        # Get the current file's content for sentiment analysis
        current_content = processed_files[filename]
        
        # Convert to numpy array for consistency with your analysis script
        content_array = np.array(current_content, dtype=object)
        
        # Flatten all words from current file
        all_content_words = [word for sentence in current_content for word in sentence]
        
        print(f"Total words in {filename}: {len(all_content_words)}")
        
        # Convert to lowercase for case-insensitive matching
        all_content_lower = [word.lower() for word in all_content_words]
        pos_words_lower = [word.lower() for word in pos_words]
        neg_words_lower = [word.lower() for word in neg_words]
        
        # Find positive and negative words
        positive_words = [word for word in all_content_lower if word in pos_words_lower]
        negative_words = [word for word in all_content_lower if word in neg_words_lower]
        
        # Calculate text analysis metrics
        count_pos = len(positive_words)
        count_neg = len(negative_words)
        total_words_after_cleaning = len(all_content_words)
        
        # Calculate total number of characters across all words
        total_characters = sum(len(word) for word in all_content_words)

        # Calculate average word length
        average_word_length = total_characters / total_words_after_cleaning if total_words_after_cleaning > 0 else 0
        
        total_no_of_sentences = len(current_content)
        Average_Number_of_Words_Per_Sentence = total_words_after_cleaning / total_no_of_sentences if total_no_of_sentences > 0 else 0
        Average_Sentence_Length = Average_Number_of_Words_Per_Sentence
        
        # Calculate subjectivity and polarity scores
        Subjectivity_Score = (count_pos + count_neg) / (total_words_after_cleaning + 0.000001)
        Polarity_Score = (count_pos - count_neg) / ((count_pos + count_neg) + 0.000001)
        
        # Calculate syllable-related metrics
        total_syllables = sum(count_syllables(word) for word in all_content_words)
        Syllable_Count_Per_Word = total_syllables / total_words_after_cleaning if total_words_after_cleaning > 0 else 0
        
        # Calculate complex words percentage
        complex_word_count = count_complex_words(all_content_words)
        percentage_complex_words = complex_word_count / total_words_after_cleaning if total_words_after_cleaning > 0 else 0

        #Fog Index
        Fog_Index= 0.4*(Average_Sentence_Length + percentage_complex_words)
        
        # Count personal pronouns (need original text for this)
        personal_pronouns_count = count_personal_pronouns(content)
        
        # Store results for this file
        result = {
            'POSITIVE SCORE': count_pos,
            'NEGATIVE SCORE': count_neg,
            'POLARITY SCORE': Polarity_Score,
            'SUBJECTIVITY SCORE': Subjectivity_Score,
            'AVG SENTENCE LENGTH': Average_Sentence_Length,
            'PERCENTAGE OF COMPLEX WORDS': percentage_complex_words,
            'FOG INDEX': Fog_Index,
            'AVG NUMBER OF WORDS PER SENTENCE': Average_Number_of_Words_Per_Sentence,
            'COMPLEX WORD COUNT': complex_word_count,
            'WORD COUNT': total_words_after_cleaning,
            'SYLLABLE PER WORD': Syllable_Count_Per_Word,
            'PERSONAL PRONOUNS': personal_pronouns_count,
            'AVG WORD LENGTH': average_word_length,
        }
        
        all_results.append(result)
        print("=" * 80)
    
    # After processing all files, update the output dataframe
    results_df = pd.DataFrame(all_results)
    
    # Make sure we have the same number of rows
    if len(results_df) == len(df_output):
        # Update the columns in the output dataframe
        for column in results_df.columns:
            if column in df_output.columns:
                df_output[column] = results_df[column]
    
    # Save the updated dataframe back to Excel
    df_output.to_excel(r"C:\Users\Sam\Downloads\Output Data Structure.xlsx", index=False)
    print(f"Successfully updated output file with {len(df_output)} rows")

if __name__ == "__main__":
    main()    