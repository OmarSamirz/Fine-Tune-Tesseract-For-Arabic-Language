import os
import time
import subprocess


def run_tesseract(input_image : str, output_file : str, lang='ara', oem='3', is_colab=True):
    command = f'tesseract {input_image} {output_file} --oem {oem} -l {lang} --tessdata-dir ./tessdata_best'
    
    if is_colab == False:
        command = f'tesseract {input_image} {output_file} --oem {oem} -l {lang}'
        
    start_time=time.time()
    process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    end_time=time.time()
    if process.returncode != 0:
        err = process.stderr.decode()
        raise RuntimeError(f'Error running tesseract: {err}')
    
    return end_time - start_time


def process_images(folder_path : str, model='ara', is_colab=True):
    benchmark_input_path = './benchmarks/yarmouk_benchmarks/'
    benchmark_output_path = './benchmarks/output_benchmarks/'
    output_folder_path = os.path.join(benchmark_output_path, 'yarmouk_' + folder_path + '_output')
    command = f'mkdir {output_folder_path}'
    subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    for filename in os.listdir(benchmark_input_path + folder_path):
        if filename.endswith('.png') or filename.endswith('.tiff'):
            input_image_path = os.path.join(benchmark_input_path + folder_path, filename)
            output_text_path = os.path.join(output_folder_path, os.path.splitext(filename)[0] + '.output')

            try:
                processing_time = run_tesseract(input_image=input_image_path, 
                                                output_file=output_text_path, 
                                                lang=model, is_colab=is_colab)
                print(f"Processed: {benchmark_input_path + folder_path + '/' + filename} (Processing Time: {processing_time:.2f} seconds)")
            except RuntimeError as e:
                print(f"Failed to process {filename}: {e}")

    print("All images processed.")