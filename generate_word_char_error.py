import os
import subprocess


def extract_words_chars_error(input_text, word_count, char_count, filename, is_word):
    start_capture = False
    lines = input_text.split('\n')
    checkpoint = 'Count   Missed   %Right'
    
    if is_word == True:
        checkpoint = 'Non-stopwords'
    
    counter = 0
    for idx, line in enumerate(lines):
        if (counter == 6 and is_word == True) or (counter == 3 and is_word == False):
            start_capture = True
        if (checkpoint in line or checkpoint in lines[idx-1]) and start_capture == False:
            counter += 1
            continue 
        
        if start_capture:
            line_lst = line.split()
            
            if len(line_lst) == 0:
                continue
            
            if is_word == False:
                char = line_lst[-1]
                new_count = int(line_lst[1])
                if line_lst[-2] == '{' and line_lst[-1] == '}':
                    char = 'White Space'
                
                if char in char_count and new_count > 0:
                    current_count, files = char_count[char]
                    char_count[char] = (current_count + new_count, files + [filename])
                elif char not in char_count and new_count > 0:
                    char_count[char] = (new_count, [filename])
            
            else:
                word = line_lst[-1]
                new_count = int(line_lst[1])
                if word in word_count and new_count > 0:
                    count, files = word_count[word]
                    word_count[word] = (count + new_count, files + [filename])
                elif word not in word_count and new_count > 0:
                    word_count[line_lst[-1]] = (new_count, [filename])
                    
    return word_count, char_count
            

def run_command(filename_gt_path, filename_output_path, is_word):
    command_accuracy = f'accuracy {filename_gt_path} {filename_output_path}'
    
    if is_word:
        command_accuracy = f'wordacc {filename_gt_path} {filename_output_path}'
        
    result_accuracy = subprocess.run(command_accuracy, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output_accuracy = result_accuracy.stdout.decode('utf-8')
    
    return output_accuracy         


def generate_errors(ground_truth_path, output_folder_path, is_word, is_yarmouk=False):
    char_count = dict()
    word_count = dict()
    
    for filename_output in os.listdir(output_folder_path):
        filename_gt = filename_output.replace('.output', '.gt')
        if is_yarmouk == True:
            filename_gt = filename_output.split('_')[0] + '.txt'
        
        filename_output_path = os.path.join(output_folder_path, filename_output)
        filename_gt_path = os.path.join(ground_truth_path, filename_gt)

        print(filename_gt_path, filename_output_path)

        output_accuracy = run_command(filename_gt_path, filename_output_path, is_word)
        
        new_word_count, new_char_count = extract_words_chars_error(output_accuracy, word_count, char_count,
                                                                   filename_gt.replace('.gt.txt', ''), is_word)
        
        word_count.update(new_word_count)
        char_count.update(new_char_count)
        
    return char_count, word_count