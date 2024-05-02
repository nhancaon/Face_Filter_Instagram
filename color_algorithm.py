import cv2
import numpy as np

def apply_filter(image, filter_type, kernel_size, sig=0):
    if filter_type == 'mean':
        return cv2.blur(image, (kernel_size, kernel_size))
    elif filter_type == 'median':
        return cv2.medianBlur(image, kernel_size)
    elif filter_type == 'gaussian':
        return cv2.GaussianBlur(image, (kernel_size, kernel_size), sig)
    else:
        print("Invalid filter type.")
        return None
    
def compOut(x, r1, s2):
    if x <= r1:
        result = (s2 / r1) * x
    else:
        result = ((255 - s2) / (255 - r1)) * (x - r1) + s2
    return result.astype(np.uint8)

def MeanFiltered(img, kernel):
    mean_filtered = apply_filter(img, 'mean', kernel)
    return mean_filtered

def MedianFiltered(img, kernel):
    median_filtered = apply_filter(img, 'median', kernel)
    return median_filtered

def GaussianFiltered(img, kernel, sig):
    gaussian_filtered = apply_filter(img, 'gaussian', kernel, sig)
    return gaussian_filtered

def Histogram(img, clip_limit):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(8, 8))
    equalized = clahe.apply(gray)
    return equalized

def Negative(img):
    img_neg = 256-1-img
    img_neg = cv2.resize(img_neg, None, fx=0.7, fy=0.7)
    return img_neg

def log_c(img_bgr, scale_value):
    img = np.array(img_bgr, 'float')
    log_image = scale_value * (np.log(img + 1))
    log_image = np.array(log_image, dtype=np.uint8)
    return log_image

def gamma(img, gamma, c):
    img1 = img.astype(np.float32) / 255.0
    gamma_corrected = np.power(img1, gamma)
    gamma_corrected = 255 * c * gamma_corrected
    img2 = np.uint8(gamma_corrected)
    return img2

def piecewise_linear(img, r1, s2):
    new_image = np.zeros_like(img)

    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            for c in range(3):
                output = compOut(img[y, x, c], r1, s2)
                new_image[y, x, c] = np.uint8(np.clip(output, 0, 255))

    new_image = cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB)
    return new_image