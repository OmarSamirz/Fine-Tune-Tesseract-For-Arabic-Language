import os
import re
import regex
import string
import numpy as np
import pandas as pd
from scipy.sparse import spmatrix
from qdrant_client import  QdrantClient
from sklearn.metrics.pairwise import cosine_similarity
from pyarabic.araby import strip_tashkeel, strip_tatweel


def remove_space_in_tatweel(text):
  return re.sub(r'ـ\s+(\w)', r'ـ\1', text)


def contains_english_letters(text : str) -> bool:
    all_letters = string.ascii_letters
    return any(char in all_letters for char in text)


def remove_english_letters(text : str) -> str:
    if contains_english_letters(text) == False:
        return text
    
    all_letters = string.ascii_letters
    for char in text:
        if char in all_letters:
            text = text.replace(char, ' ')
    

    return re.sub(r'\s+', ' ', text)


def count_words(text : str) -> int:
    return len(text.split())


def check_tashkeel(text : str) -> bool:
    if text == strip_tashkeel(text):
        return False
    
    return True


def check_tatweel(text : str) -> bool:
    if text == strip_tatweel(text):
        return False
    
    return True


def remove_extra_space(text : str) -> str:
    text =  re.sub(
                    r'(\S)\s*([:،.\{\}\[\]\(\)<>؟!،])\s*(?=\s)', r'\1\2', 
                    re.sub(r'\{\s*(.*?)\s*\}', r'{\1}', 
                        re.sub(r'\[\s*(.*?)\s*\]', r'[\1]', 
                            re.sub(r'\(\s*(.*?)\s*\)', r'(\1)', 
                                re.sub(r'<\s*(.*?)\s*>', r'<\1>', text)
                            )
                        )
                    )
                 )
    
    return re.sub(r'\s+', ' ', text)
    

def count_words_in_list(lst : list[str]) -> tuple[int, int, int]:
    count_words = 0
    count_tashkeel = 0
    count_tatweel = 0
    
    for text in lst:
        try:
            splitted_text = text.split()
        except:
            continue
        
        for word in splitted_text:
            if check_tashkeel(word) == True:
                count_tashkeel += 1
            if check_tatweel(word) == True:
                count_tatweel += 1
            
            count_words += 1
    
    return count_words, count_tashkeel, count_tatweel


def split_data(df : pd.DataFrame, isTashkeel : bool = False) -> tuple[list, list, list]:
    new_text_lst = []
    new_num_tashkeel_lst = []
    new_num_tatweel_lst = []
    new_num_words_lst = []
    
    word_count = 2
    for _, row in df.iterrows():
        if word_count == 1:
            word_count = 2
        
        left_split_count = 0
        right_split_count = word_count
        splitted_text = row[0].split()
        
        if isTashkeel == True:
            splitted_text_tashkeel = row[1].split()
        
        if len(splitted_text) <= 10:
            new_text_splitted = splitted_text[left_split_count:right_split_count]
            new_text = " ".join(new_text_splitted)
            num_words, num_tashkeel, num_tatweel = count_words_in_list(new_text_splitted)        
            
            if isTashkeel == True:
                new_text_tashkeel_splitted = splitted_text_tashkeel[left_split_count:right_split_count]
                new_text_tashkeel = " ".join(new_text_tashkeel_splitted)
                new_text_lst.append((new_text, new_text_tashkeel))
            else:
                new_text_lst.append(new_text)
                
            new_num_tashkeel_lst.append(num_tashkeel)
            new_num_tatweel_lst.append(num_tatweel)
            new_num_words_lst.append(num_words)
            continue
            
        remaineded_length = len(splitted_text)
        while right_split_count <= len(splitted_text):
            
            new_text_splitted = splitted_text[left_split_count:right_split_count]
            new_text = " ".join(new_text_splitted)
            num_words, num_tashkeel, num_tatweel = count_words_in_list(new_text_splitted)
            
            if isTashkeel == True:
                new_text_tashkeel_splitted = splitted_text_tashkeel[left_split_count:right_split_count]
                new_text_tashkeel = " ".join(new_text_tashkeel_splitted)
                new_text_lst.append((new_text, new_text_tashkeel))
            else:
                new_text_lst.append(new_text)
                
            new_num_tashkeel_lst.append(num_tashkeel)
            new_num_tatweel_lst.append(num_tatweel)
            new_num_words_lst.append(num_words)
        
            remaineded_length -= word_count
            word_count = (word_count % 10) + 1
            
            if word_count == 1:
                word_count = 2
                
            left_split_count = right_split_count
            right_split_count += word_count  
        else:
            new_text_splitted = splitted_text[left_split_count:len(splitted_text)]
            if len(new_text_splitted) > 0:
                new_text = " ".join(new_text_splitted)
                num_words, num_tashkeel, num_tatweel = count_words_in_list(splitted_text[left_split_count:len(splitted_text)])
                
                if isTashkeel == True:
                    new_text_tashkeel_splitted = splitted_text_tashkeel[left_split_count:len(splitted_text)]
                    new_text_tashkeel = " ".join(new_text_tashkeel_splitted)
                    new_text_lst.append((new_text, new_text_tashkeel))
                else:
                    new_text_lst.append(new_text)
                
                new_num_tashkeel_lst.append(num_tashkeel)
                new_num_tatweel_lst.append(num_tatweel)
                new_num_words_lst.append(num_words)
            
                word_count = (word_count % 10) + 1  
    
    return new_text_lst, new_num_tashkeel_lst, new_num_tatweel_lst, new_num_words_lst


def find_similarity(df : pd.DataFrame, query_vec : spmatrix, 
                    tfidf : spmatrix, index : int, size : int) -> tuple[pd.DataFrame, np.ndarray]:
    
    similarity = cosine_similarity(query_vec, tfidf).flatten()
    indices = np.argpartition(similarity, -size)[-size:]
    result = df.iloc[indices][::-1]
    
    return result, similarity[indices][::-1]


def remove_arabic_stop_words(sentence : str, stop_words : set[str] | None, punc_pattern : regex.Pattern[str]) -> str:
    removed_punc_sentence = punc_pattern.sub('', sentence)
    splitted_sentence = removed_punc_sentence.split()
    
    if stop_words != None:
        removed_stop_words_sentence = [word for word in splitted_sentence if word not in stop_words]
    
    return ' '.join(removed_stop_words_sentence) if stop_words != None else ' '.join(splitted_sentence)


def get_client():
    return QdrantClient(
        url=os.getenv("QDRANT_DB_URL"),
        api_key=os.getenv("QDRANT_API_KEY")
    )

def get_similar_records(query_vector, chunks, client : QdrantClient):
    similar_records = []
    
    for chunk_id in chunks:
        result = client.recommend(
            positive=[query_vector],
            collection_name=f"arabic_setences_chunk_{chunk_id}", 
            limit=10
        )
        
        similar_records.extend(result['result'])
        return similar_records


def find_similar_records_across_chunks(query_vector, num_chunks=270):
    chunk_ids = range(0, num_chunks+1) 
    similar_records = get_similar_records(query_vector, chunk_ids)
    
    unique_records = {}
    for record in similar_records:
        record_id = record['payload']['id']
        if record_id not in unique_records:
            unique_records[record_id] = record
    
    similar_records = list(unique_records.values())
    return similar_records
        