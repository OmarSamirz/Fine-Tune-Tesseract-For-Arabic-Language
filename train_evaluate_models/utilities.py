import os
import requests
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from evaluate_model import generate_accuracy

def download_benchmark(downloadurl : str, destination : str):
    req = requests.get(downloadurl)

    filename = req.url[downloadurl.rfind('/')+1:-11]

    file_path = os.path.join(destination, filename)
    with open(file_path, 'wb') as f:
        for chunk in req.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
        
                
def get_accuracy(ground_truth_path : str, output_benchmarks_path : str, model_name : str, is_combination=False):
    dataset_name_lst = []
    file_name_lst = []
    engine_name_lst = []
    char_acc_lst = []
    word_acc_lst = []
    oem_lst = []
    psm_lst = []
    
    for folder in os.listdir(output_benchmarks_path):    
        print(folder)    
        output_folder_path = os.path.join(output_benchmarks_path, folder)
        dataset_name, file_name, engine_name, char_acc, word_acc = generate_accuracy(ground_truth_path=ground_truth_path, 
                                                                                     output_folder_path=output_folder_path, 
                                                                                     model_name=model_name)
        dataset_name_lst.extend(dataset_name)
        file_name_lst.extend(file_name)
        engine_name_lst.extend(engine_name)
        char_acc_lst.extend(char_acc)
        word_acc_lst.extend(word_acc)
        
        if is_combination == True:
            splitted_folder_name = folder.split('_')
            oem_lst.extend([splitted_folder_name[-2]] * len(dataset_name))
            psm_lst.extend([splitted_folder_name[-1]] * len(dataset_name))
    
    return dataset_name_lst, file_name_lst, engine_name_lst, char_acc_lst, word_acc_lst, oem_lst, psm_lst
    


def create_df(csv_name : str, dataset_name_lst, file_name_lst, engine_name_lst, char_acc_lst, word_acc_lst, oem_lst=[], psm_lst=[]):         
    data = {'dataset': dataset_name_lst, 'file': file_name_lst, 
            'engine': engine_name_lst, 'oem': oem_lst, 'psm': psm_lst, 'char_acc': char_acc_lst,
            'word_acc': word_acc_lst}
    
    if len(oem_lst) == 0 and len(psm_lst) == 0:
        del data['oem']
        del data['psm']
    
    df = pd.DataFrame(data)
    df.to_csv(f'./benchmarks/csv_benchmarks/{csv_name}.csv', index=False)
    

def create_graph(df : pd.DataFrame, title : str, text, folder_path : str):
    print(f"mean: {np.mean(df['word_acc'])}")
    mean = (100 - np.mean(df['word_acc']))

    plt.figure(figsize=(10, 4))
    sns.kdeplot((100 - df['word_acc']), color="teal", fill=False, bw_adjust=2, linewidth=2)
    kde_x, kde_y = sns.kdeplot((df['word_acc'] - 100) * -1, bw_adjust=2).get_lines()[0].get_data()
    plt.fill_between(kde_x, kde_y, color="red", alpha=0.3)

    middle_y_position = 0.7 * np.max(kde_y)
    plt.text(mean, middle_y_position, f'{mean:.1f}', ha='center', va='bottom', color='black', fontsize=10, bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))
    plt.axline((mean, middle_y_position), (mean, 0), color='green', linewidth=2)

    plt.title(title)
    plt.xlabel('Word Error')
    plt.ylabel('Density')
    plt.xticks([0, 25, 50, 75, 100])
    sns.despine(top=True, right=True, left=True, bottom=True)
    plt.gca().set_facecolor('white')
    plt.text(x=60, y=0.01, s=text)
    plt.savefig(f"{folder_path + '/' + title.replace(' + ', '_')}")
    plt.show()
    plt.close()
