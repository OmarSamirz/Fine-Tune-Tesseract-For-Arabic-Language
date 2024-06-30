from noises.noise_adder import NoiseAdder, np, cv2, random, Image


class DilateNoiseAdder(NoiseAdder):
    
    def __init__(self):
        self.left_morph = 2
        self.right_morph = 3
    
    def _augment_img_dilate(self, img: Image):
        img = np.asarray(img)     #convert to numpy
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(self.left_morph, self.right_morph))
        # dilation because the image is not inverted
        img = cv2.erode(img, kernel, iterations=random.randint(2, 2))
        image = Image.fromarray(img)
        return image
    
    def add_noise(self, img: Image):
        return self._augment_img_dilate(img)