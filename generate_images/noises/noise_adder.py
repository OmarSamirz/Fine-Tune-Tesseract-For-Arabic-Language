import cv2
import random
import numpy as np
from PIL import Image
from abc import ABC, abstractmethod


class NoiseAdder(ABC):
    
    @abstractmethod
    def add_noise(self, img: Image):
        return img
    
    
    
    