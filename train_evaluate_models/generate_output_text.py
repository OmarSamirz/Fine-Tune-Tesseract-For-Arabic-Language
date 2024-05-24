import os
import time
import subprocess

# best value for oem_number was 3 and best value for psm_number was 6
def run_tesseract(input_image : str, output_file : str, lang='ara', oem_number='3', psm_number='6', is_colab=False) -> float:
    command = f'tesseract {input_image} {output_file} --oem {oem_number} --psm {psm_number} -l {lang} --tessdata-dir ./our_models'
    
    if is_colab == False:
        command = f'tesseract {input_image} {output_file} --oem {oem_number} --psm {psm_number} -l {lang}'
    
    print(f'{input_image} {output_file}')
    start_time=time.time()
    process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    end_time=time.time()
    if process.returncode != 0:
        err = process.stderr.decode()
        raise RuntimeError(f'Error running tesseract: {err}')
    
    return end_time - start_time


def process_images(folder_path : str, output_folder_path : str, model='ara', is_colab=False, is_yarmouk=False, is_combination=False, oem_number='3', psm_number='6') -> None:
    if is_yarmouk == True:
        splitted_yarmouk_name = folder_path.split('/')[-1]
        if is_combination == True:
            output_folder_path = os.path.join(output_folder_path, 'yarmouk_' + splitted_yarmouk_name + 
                                          '_output' + f'_{oem_number}_{psm_number}')
        else:
            output_folder_path = os.path.join(output_folder_path, 'yarmouk_' + 
                                            splitted_yarmouk_name + '_output')
        
        
        
    command = f'mkdir {output_folder_path}'
    subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(model)
    
    for img_num, filename in enumerate(os.listdir(folder_path)):
        if filename.endswith('.png') or filename.endswith('.tiff') or filename.endswith('.tif'):
            input_image_path = os.path.join(folder_path, filename)
            output_text_path = os.path.join(output_folder_path, os.path.splitext(filename)[0] + '.output')

            try:
                processing_time = run_tesseract(input_image=input_image_path, 
                                                output_file=output_text_path, 
                                                lang=model, is_colab=is_colab,
                                                oem_number=oem_number, psm_number=psm_number)
                print(f"Processed image {img_num + 1}: {folder_path + '/' + filename} (Processing Time: {processing_time:.2f} seconds)")
            except RuntimeError as e:
                print(f"Failed to process {filename}: {e}")

    print("All images processed.")