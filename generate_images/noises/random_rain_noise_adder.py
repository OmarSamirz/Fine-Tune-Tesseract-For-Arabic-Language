import albumentations as A
from noises.noise_adder import NoiseAdder, np, cv2, random, Image


class RandomRainNoiseAdder(NoiseAdder):
    
    def __init__(self):
        self.slant_lower = 20
        self.slant_upper = 20
        self.drop_length = 1
        self.brightness_coefficient = 1.0
        self.drop_length = 10
        self.drop_width = 2
        self.drop_color = (255, 255, 255)
        
    
    def _augment_img_RandomRain(self, img: Image):
        img = np.asarray(img)     #convert to numpy
        transform = A.Compose([
        #add white pixels noise: RandomRain
        A.RandomRain(slant_lower=self.slant_lower, slant_upper=self.slant_upper, 
                     brightness_coefficient=self.brightness_coefficient, drop_length=self.drop_length, 
                     drop_width=self.drop_width, drop_color=self.drop_color, blur_value=1, p=1)
        ])
        img = transform(image=img)['image']
        image = Image.fromarray(img)
        return image
    
    def add_noise(self, img: Image):
        return self._augment_img_RandomRain(img)
        