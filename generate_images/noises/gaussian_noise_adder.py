from skimage.util import random_noise
from noises.noise_adder import INoiseAdder, np, Image

class GaussianNoiseAdder(INoiseAdder):
    def __init__(self):
        super().__init__()
    
    def _augment_img_gaussian(self, img: Image):
        gauss_img = random_noise(np.array(img), mode='gaussian', clip=True)
        noise_im = np.array(255 * gauss_img, dtype='uint8')
        image = Image.fromarray(np.array(noise_im))
        return image
        
    
    def add_noise(self, img: Image):
        return self._augment_img_gaussian(img)
    