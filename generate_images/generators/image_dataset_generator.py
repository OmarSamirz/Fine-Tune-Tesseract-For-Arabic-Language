import os
import numpy as np
from copy import copy
from noises.noise_adder import NoiseAdder
from trdg.generators import GeneratorFromStrings

class ImageDatasetGenerator:
    def __init__(self, font_size, dpi):
        self._font_size = font_size
        self._dpi = dpi
        
    @property
    def font_size(self):
        return self._font_size
    
    @font_size.setter
    def font_size(self, val):
        self._font_size = val
    
    @property
    def dpi(self):
        return self._dpi
    
    @dpi.setter
    def dpi(self, val):
        self._dpi = val
    
    def split_by_percent(self, batch: list[str], percent: float):
        shuffled_batch = copy(batch)
        np.random.shuffle(shuffled_batch)
        split_index = int(len(shuffled_batch) * percent)
        
        first_split = shuffled_batch[:split_index]
        second_split = shuffled_batch[split_index:]
        
        return first_split, second_split
        
    
    def split_into_n_batches(self, batch: list[str], n: int):
        shuffled_batch = copy(batch)
        np.random.shuffle(shuffled_batch)
        sublist_size = len(shuffled_batch) // n
        remainder = len(shuffled_batch) % n

        sublists = [shuffled_batch[i * sublist_size + min(i, remainder):(i + 1) * sublist_size + min(i + 1, remainder)] for i in range(n)]

        return sublists
    
    
    def create_generator(self, 
                        generator_name: str,
                        font_name: str,
                        font_path: str,
                        noise: NoiseAdder,
                        strings: list[str], 
                        skewing_angle: int = 0,
                        random_skew: bool = False,
                        blur: int = 0,
                        random_blur: bool = False,
                        distortion_type: int = 3,
                        background_type: int = 0, 
                        background_folder_path: str = os.path.join(
                            "..", os.path.split(os.path.realpath(__file__))[0], "images"),
    ):
        generator = GeneratorFromStrings(strings=strings, count=len(strings), 
                                         fonts=[os.path.join(font_path, font_name)], 
                                         skewing_angle=skewing_angle, random_skew=random_skew, 
                                         blur=blur, random_blur=random_blur, distorsion_type=distortion_type,
                                         background_type=background_type, image_dir=background_folder_path,
                                         size=self._font_size, rtl=True, fit=True,
                                         )
        
        return (generator_name, noise, generator)
    
    
    def generate_batch(self, 
                       batch_path: str, 
                       generators: list[tuple[str, GeneratorFromStrings]], 
    ):
        
        for batch_name, noise, generator in generators:
            final_path = os.path.join(batch_path, batch_name)
            
            for i, (img, lbl) in enumerate(generator):
                img = noise.add_noise(img)    
                image_info = img.info.copy()
                image_info['dpi'] = self._dpi
                img.save(f"{final_path}_{i+1}.tif", **image_info)
                with open(f"{final_path}_{i+1}.gt.txt", 'w') as f:
                    f.write(lbl)
        
    
    
        