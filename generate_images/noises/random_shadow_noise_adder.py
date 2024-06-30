import albumentations as A
from noises.noise_adder import NoiseAdder, np, cv2, random, Image


class RandomShadowNoiseAdder(NoiseAdder):
    
    def __init__(self, ):
        self.shadow_dimension = 10
    
    def _augment_img_RandomShadow(self, img: Image):
        img = np.asarray(img)     #convert to numpy
        transform = A.Compose([
        #add black pixels noise: RandomShadow
        A.RandomShadow(p=1,shadow_dimension=10, shadow_roi=(0, 0, 1, 1)),
        ])
        img = transform(image=img)['image']
        image = Image.fromarray(img)
        return image
    
    def add_noise(self, img: Image):
        return self._augment_img_RandomShadow(img)