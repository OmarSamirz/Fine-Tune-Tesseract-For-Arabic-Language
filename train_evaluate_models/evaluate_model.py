import os
import subprocess

def generate_accuracy(ground_truth_path : str, output_folder_path : str, model_name : str):
    dataset_name_lst = []
    file_name_lst = []
    engine_name_lst = []
    char_acc_lst = []
    word_acc_lst = []

    for filename_output in os.listdir(output_folder_path):
        filename_gt = filename_output.split('_')[0] + '.txt'
        filename_output_path = os.path.join(output_folder_path, filename_output)
        filename_gt_path = os.path.join(ground_truth_path, filename_gt)

        print(filename_gt_path, filename_output_path)
        
        command_accuracy = f'accuracy {filename_gt_path} {filename_output_path}'
        command_wordacc = f'wordacc {filename_gt_path} {filename_output_path}'

        result_accuracy = subprocess.run(command_accuracy, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result_wordacc = subprocess.run(command_wordacc, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output_accuracy = result_accuracy.stdout.decode('utf-8').split('\n')
        output_wordacc = result_wordacc.stdout.decode('utf-8').split('\n')

        dataset_name_lst.append(output_folder_path.replace('_output', '').split('/')[-1])
        file_name_lst.append(filename_gt)
        engine_name_lst.append(model_name)
        word_acc_lst.append(output_wordacc[4].split()[0])
        char_acc_lst.append(output_accuracy[4].split()[0])
        print(f'word_acc index: {output_wordacc[4].split()[0]}')
        print(f'char_acc index: {output_accuracy[4].split()[0]}')
            
    return dataset_name_lst, file_name_lst, engine_name_lst, char_acc_lst, word_acc_lst