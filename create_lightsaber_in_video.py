import pylab
import imageio
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from videoreader import VideoReader
import cv2
import skimage as sk
import numpy as np
from skimage.morphology import disk, ball
import imageio
import sys
import os
import imageUnion

RED = 0
GREEN = 1
BLUE = 2
LIGHTSABERCOLOR = BLUE

## Processing Frame And Andded Gaussian Effect on LightSaber Color Pixels
def AddGaugasianEffectToHighlighColor(frame):
    # Create Colors Channels 
    redChannel = frame[:,:, RED]
    greenChannel = frame[:,:, GREEN]
    blueChannel = frame[:,:, BLUE]
    
    # Selected Color Highlight 
    colorHighlight = None
    if(LIGHTSABERCOLOR == RED) :
        colorHighlight = redChannel - greenChannel/2 - blueChannel/2
    elif (LIGHTSABERCOLOR == GREEN) :
        colorHighlight = greenChannel - blueChannel/2 - redChannel/2
    elif (LIGHTSABERCOLOR == BLUE) :
        colorHighlight = blueChannel - greenChannel/2 - redChannel/2

    # Create a binary image with the lightsaber pixels based on the pre-established threshold.
    Threshold = None
    if(LIGHTSABERCOLOR == RED) :
        Threshold = 42
    elif (LIGHTSABERCOLOR == GREEN) :
        Threshold = 12
    elif (LIGHTSABERCOLOR == BLUE) :
        Threshold = 24

    segmentedImage = colorHighlight > Threshold

    # Creating Gaussian Filters For Each Color Channel
    redSigma = 8.0 if LIGHTSABERCOLOR == RED else 1.0 
    greenSigma = 8.0 if LIGHTSABERCOLOR == GREEN else 1.0 
    blueSigma = 8.0 if LIGHTSABERCOLOR == BLUE else 1.0 

    redGaussianFilter = sk.filters.gaussian(segmentedImage, sigma=redSigma)
    greenGaussianFilter = sk.filters.gaussian(segmentedImage, sigma=greenSigma)
    blueGaussianFilter = sk.filters.gaussian(segmentedImage, sigma=blueSigma)

    # Normalizing pixel values in the range [0...255].
    redGaussianFilter *= 255/redGaussianFilter.max()
    greenGaussianFilter *= 255/greenGaussianFilter.max()
    blueGaussianFilter *= 255/blueGaussianFilter.max()

    # Creating Frames with Color Channels
    gaussianFrame = np.dstack((redGaussianFilter.astype(int), greenGaussianFilter.astype(int), blueGaussianFilter.astype(int)))

    # Adding the Gaussian Filter with the Color Channels
    redFilteredChannel = imageUnion(redGaussianFilter, redChannel)
    greenFilteredChannel = imageUnion(greenGaussianFilter, greenChannel)
    blueFilteredChannel = imageUnion(blueGaussianFilter, blueChannel)

    # Creating Frames with Color Channels
    filteredFrame = np.dstack((redFilteredChannel.astype(int), greenFilteredChannel.astype(int), blueFilteredChannel.astype(int)))

     # Convert SegmentedImage Matrix in a Image and Show
    plt.subplot(131)
    plt.imshow(colorHighlight)
    plt.subplot(132)
    plt.imshow(segmentedImage, cmap='Greys',  interpolation='nearest')
    plt.subplot(133)
    plt.imshow(gaussianFrame, cmap='Greys',  interpolation='nearest')
    plt.savefig('FrameProcess.png')
    #plt.show()

    return filteredFrame

# Leitura e escrita do arquivo.
filename = './Original_Blue.mp4'
originalVideo = imageio.get_reader(filename)
outVideo = imageio.get_writer('LightSaberVideo.mp4', fps=24)

# Iteração entre os frames.
for i, frame in enumerate(originalVideo):
    # Print Percentage

    percent = float((i/originalVideo.count_frames()) * 100)
    print(f'{percent:.2f}% processing...')

    # Processa o frame atual para aplicar o efeito do sabre de luz.
    filteredFrame = AddGaugasianEffectToHighlighColor(frame)
    outVideo.append_data(filteredFrame)

        
# Salva o vídeo
outVideo.close()

print("Effect added to the original video in the file LightSaberVideo.mp4!")
print("done!")