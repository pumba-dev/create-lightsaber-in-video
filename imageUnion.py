
import numpy
import sys

MAXPIXELVALUE = 255
MINPIXELVALUE = 0

def imageUnion(firstImage, secondImage):
    imageWidth, imageHeight = firstImage.shape
    
    newImage = numpy.zeros((imageWidth, imageHeight))
    
    for x in range(imageWidth):
        for y in range(imageHeight):
            newPixelValue = secondImage[x,y] + firstImage[x,y]
            if newPixelValue > MAXPIXELVALUE:
                newImage[x,y] = MAXPIXELVALUE
            else:
                newImage[x,y] = newPixelValue

    return newImage

sys.modules[__name__] = imageUnion