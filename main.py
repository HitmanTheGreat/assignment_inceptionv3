from typing_extensions import Required
import cv2
import os
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img,img_to_array
from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from tensorflow.python.keras import utils 
from PIL import Image
import PIL
import time
import streamlit as st

st.title(" **Object Detection** ")
#converting image into array
def load_image(image_path):
    img = Image.open( image_path )
    newImg = img.resize((299,299), PIL.Image.BILINEAR).convert("RGB")
    data = np.array( newImg.getdata() )
    return 2*( data.reshape( (newImg.size[0], newImg.size[1], 3) ).astype( np.float32 )/255 ) - 1
#setting path
current_path = os.getcwd()
#loading model
model = load_model(r'static/inception.h5')
#predicting code
def predictor(img_path): #
    image = load_image(img_path)
    image = np.expand_dims(image, axis=0)
    preds = model.predict(image)
    print('Predicted:', decode_predictions(preds))
    return(preds)
#saving video
def save_uploaded_file(uploaded_file,type=["mp4","avi","webm","mov",""]):

    try:

        with open(os.path.join('static/videos',uploaded_file.name),'wb') as f:

            f.write(uploaded_file.getbuffer())

        return 1    

    except:

        return 0
#put queries here
search = (st.text_input("Type The Name Of Search Object....")).lower()
uploaded_file = st.file_uploader("Upload Video",type=["mkv","mp4",'avi','flv','webm','vob','mov','ogg','wmv','3gp'])
if uploaded_file is not None:
    notfound = True
    img = Image.open(os.path.join('static/images/',"loading.jpg"))
    st.image("loading.....")
    if save_uploaded_file(uploaded_file):   	
        capture = cv2.VideoCapture(os.path.join('static/videos',uploaded_file.name))
        st.video(os.path.join('static/videos',uploaded_file.name))
        frameNr = 0
        
        while (True):
        
            success, frame = capture.read()
        
            if success:
                cv2.imwrite(f'static/images/{frameNr}.jpg', frame)
                prediction = predictor(os.path.join(f'static/images/{frameNr}.jpg'))
                prediction = decode_predictions(prediction)
                predition_names = []
                for each in prediction[0]:
                    predition_names.append(each[1])
                if search in predition_names : 
                    notfound = False
                    disp_img = cv2.imread(os.path.join(f'static/images/{frameNr}.jpg'))
                    #display prediction text over the image
                    pic = cv2.putText(disp_img, search, (20,20), cv2.FONT_HERSHEY_TRIPLEX , 0.8, (255,255,255))
                    st.image(pic)
                    st.text('Predictions :-')
                    st.text(prediction)
                    os.remove(os.path.join(f'static/images/{frameNr}.jpg'))#deleting the image to savespace 
                    break
            else:
                break
        
            frameNr = frameNr+1
        
    capture.release()
    time.sleep(120) # delay b4 deleting the video
    os.remove(os.path.join(f'static/videos/'+uploaded_file.name)
    if notfound :
        st.write("Item you searched was not found ")
        # display the image

