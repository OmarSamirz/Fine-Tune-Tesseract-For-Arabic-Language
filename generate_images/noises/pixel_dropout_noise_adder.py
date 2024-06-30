import albumentations as A
from noises.noise_adder import NoiseAdder, np, cv2, random, Image


class PixelDropoutNoiseAdder(NoiseAdder):
    
    def __init__(self):
        self.dropout_prob = 0.12
        self.drop_value = 255
    
    def _augment_img_PixelDropout_white(self, img: Image):
        img = np.asarray(img)     #convert to numpy
        transform = A.Compose([
        #add white pixels noise: PixelDropout
        A.PixelDropout(dropout_prob=self.dropout_prob, drop_value=self.drop_value, p=1)
        ])
        img = transform(image=img)['image']
        image = Image.fromarray(img)
        return image
    
    def add_noise(self, img: Image):
        return self._augment_img_PixelDropout_white(img)