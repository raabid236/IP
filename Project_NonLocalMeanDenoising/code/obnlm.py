# -*- coding: utf-8 -*-
"""
Python Code for the Non local filter (Speckle)
proposed for P. Coupe, P. Hellier, C. Kervrann and C. Barillot in
"Nonlocal Means-Based Speckle Filtering for
Ultrasound Images"

For Image Processing Denoising Project
"""

# Matplotlib library
import matplotlib.pyplot as plt
from matplotlib import cm

# Numpy library
import numpy as np

from skimage import util

from skimage import data
from skimage import img_as_float
from skimage.transform import resize

#  img - input image
#  t - search window
#  f - similarity window
#  h - degree of filtering

def obnlm(img,t,f,h):             # 
    img = img_as_float(img)
    [m, n]  = img.shape
    img_denoised = np.zeros((m,n))
    h = h*h

    # Normalization
    kernel=np.zeros((2*f+1,2*f+1))   
    for d in range(1,f+1) :
        value = 1. / ((2*d+1) * (2*d+1))
        for i in range (-d,d+1) :
            for j in range (-d,d+1) :
                kernel[f-i,f-j] = kernel[f-i,f-j] + value 

    kernel = kernel / f
    kernel = kernel / sum(sum(kernel))
    vkernel = np.reshape(kernel, (2*f+1)*(2*f+1) )


    pdimg = util.pad(img, ((f,f)) , mode='symmetric')     # padding

    # Denoising
    for i in range(0,m) :
        for j in range(0,n) :
            i1 = i + f
            j1 = j + f
                
            W1 = pdimg[range(i1-f,i1+f+1),:]
            W1 = W1[:,range(j1-f,j1+f+1)]
                         
            wmax = 0 
            average = 0;
            sweight = 0;
         
            rmin = max(i1-t,f)
            rmax = min(i1+t,m+f-1)
            smin = max(j1-t,f)
            smax = min(j1+t,n+f-1)
         
            # Find similarity between neighborhoods W1(center) and W2(surrounding)
            for r in range(rmin,rmax+1) :
                for s in range(smin,smax+1) :
                    if ((r==i1) and (s==j1)) :
                        continue
                    W2 = pdimg[range(r-f,r+f+1),:]
                    W2 = W2[:,range(s-f,s+f+1)]
                    # Use Pearson Distance
                    temp = np.reshape(((np.square(W1-W2))/W2), (2*f+1)*(2*f+1))
                    d = np.dot(vkernel,temp)
                    w =  np.exp(-d/h)                 
                    if (w>wmax) :
                        wmax=w
                
                    sweight = sweight + w
                    average = average + w*pdimg[r,s]
             
            average = average + wmax*pdimg[i1,j1]
            sweight = sweight + wmax               # Calculation of the weight
                   
            # Compute value of the denoised pixel 
            if (sweight > 0) :
                img_denoised[i,j] = average / sweight
            else :
                img_denoised[i,j] = img[i,j]
                
    return img_denoised            




# For Testing
img = data.camera();
img = resize(img,(100,100));              # Reduce the test runtime

# Choose img differently for applying NLM function on a different grayscale image

img_noisy = util.random_noise(img, mode='speckle');

# OBNLM Denoising
sigma = 0.1;
img_denoised = obnlm(img_noisy,5,2,sigma)

# Show results
plt.figure()
plt.title("original")
plt.imshow(img, cmap=cm.Greys_r)

plt.figure()
plt.title("noisy")
plt.imshow(img_noisy, cmap=cm.Greys_r)            

plt.figure()
plt.title("filtered")
plt.imshow(img_denoised, cmap=cm.Greys_r)

plt.figure()
plt.title("residuals")
plt.imshow(img_noisy-img_denoised, cmap=cm.Greys_r)





