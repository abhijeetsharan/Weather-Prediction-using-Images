from keras.models import load_model
import numpy as np
from keras.preprocessing.image import load_img , img_to_array
import pandas as pd


imgWidth = 256
imgHeight = 256

classes = ["cloudy","foggy","rainy","shine","sunrise"]

model = load_model('C:/Users/devil/OneDrive/Desktop/PROJECTS/Weather Prediction using Images/bestWeatherModel.keras')

print(model.summary())

def prepareImage(ImagePath):
    image = load_img(ImagePath, target_size=(imgHeight,imgWidth))
    imgResult = img_to_array(image)
    imgResult = np.expand_dims(imgResult, axis = 0)
    imgResult = imgResult / 255.
    return imgResult


testImagesFolder = "C:/Users/devil/OneDrive/Desktop/PROJECTS/Weather Prediction using Images/Test"
testImagesNameDF = pd.read_csv("C:/Users/devil/OneDrive/Desktop/PROJECTS/Weather Prediction using Images/test.csv")
testImagesList = []

#create list of images with its full names

testDFList = testImagesNameDF['Image_id'].tolist()

# print(testDFList)

for item in testDFList:
    tempName = testImagesFolder + "/" + str(item)
    testImagesList.append(tempName)

print("The list of the images : ")
print(testImagesList)

#The first element
ImagesArray = prepareImage(testImagesList[0])

#from the second till the end
for imgName in testImagesList[1: ]:
    print("preparing image : " + imgName)
    processedImage = prepareImage(imgName)
    ImagesArray = np.append(ImagesArray, processedImage, axis=0)

print("Images shape: ")
print(ImagesArray.shape)

#save the np array
np.save("C:/Users/devil/OneDrive/Desktop/PROJECTS/Weather Prediction using Images/ImageArray.npy", ImagesArray)

#predict all the images in the array
resultArray = model.predict(ImagesArray, batch_size=16, verbose=1)
answers = np.argmax(resultArray, axis = 1)
print("Answers : ")
print(answers)

yTrue = testImagesNameDF['labels']
yPred = answers

num = 0
for imgName in testImagesList:
    print("Image : " + imgName + "     True Value : " + classes[yTrue[num]] + "      Predictions: " + classes[yPred[num]])
    num = num + 1 