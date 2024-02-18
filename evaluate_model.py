import os
import subprocess
import pandas as pd

def generate_accuracy(ground_truth_path : str, output_folder_path : str, model_name : str):
    dataset_name_lst = []
    file_name_lst = []
    engine_name_lst = []
    char_acc_lst = []
    word_acc_lst = []

    for filename_output in os.listdir(output_folder_path):
        for filename_gt in os.listdir(ground_truth_path):
            if filename_output.split('_')[0] == filename_gt.split('.')[0]:
                filename_output_path = os.path.join(output_folder_path, filename_output)
                filename_gt_path = os.path.join(ground_truth_path, filename_gt)

                print(filename_gt_path, filename_output_path)
                
                command_accuracy = f'accuracy {filename_gt_path} {filename_output_path}'
                command_wordacc = f'wordacc {filename_gt_path} {filename_output_path}'

                result_accuracy = subprocess.run(command_accuracy, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                result_wordacc = subprocess.run(command_wordacc, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output_accuracy = result_accuracy.stdout.decode('utf-8').split(' ')
                output_wordacc = result_wordacc.stdout.decode('utf-8').split(' ')

                dataset_name_lst.append(output_folder_path.replace('_output', '').split('/')[-1])
                file_name_lst.append(filename_gt)
                engine_name_lst.append(model_name)
                for idx, name in enumerate(output_accuracy):
                    if name == 'Accuracy\n\n':
                        percentage_idx = idx - 2
                        char_acc_lst.append(output_accuracy[percentage_idx])
                        print(f'char_acc: {output_accuracy[percentage_idx]}')
                        break
                
                for idx, name in enumerate(output_wordacc):
                    if name == 'Accuracy\n\nStopwords\n':
                        percentage_idx = idx - 2
                        word_acc_lst.append(output_wordacc[percentage_idx])
                        print(f'word_acc: {output_wordacc[percentage_idx]}')
                        break

                break
            
    return dataset_name_lst, file_name_lst, engine_name_lst, char_acc_lst, word_acc_lst

def create_df(csv_name : str, dataset_name_lst, file_name_lst, engine_name_lst, char_acc_lst, word_acc_lst):         
    data = {'dataset': dataset_name_lst, 'file': file_name_lst, 
            'engine': engine_name_lst, 'char_acc': char_acc_lst,
            'word_acc': word_acc_lst}
    
    df = pd.DataFrame(data)
    df.to_csv(f'./benchmarks/csv_benchmarks/{csv_name}.csv', index=False)