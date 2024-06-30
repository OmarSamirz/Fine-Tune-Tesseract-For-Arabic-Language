from noises.noise_adder import NoiseAdder, np, cv2, random, Image


class ErosionNoiseAdder(NoiseAdder):
    
    def __init__(self):
        self.left_morph = 3
        self.right_morph = 3
    
    def _augment_img_erode(self, img: Image):
        img = np.asarray(img)     #convert to numpy
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(self.left_morph, self.right_morph))
        # erosion because the image is not inverted
        img = cv2.dilate(img, kernel,iterations=random.randint(1, 2))
        image = Image.fromarray(img)   
        return image
    
    def add_noise(self, img: Image):
        return self._augment_img_erode(img)