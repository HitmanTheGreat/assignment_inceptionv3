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
import base64
#header
st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    body {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    
    st.markdown(page_bg_img, unsafe_allow_html=True)
    return

set_png_as_page_bg('background.png')
st.markdown("<center><h1 style='text-shadow:3px 3px 4px blue'><b><u>Object Detection Machine Learning</u> </b></h1></center>",unsafe_allow_html=True)
#converting image into array
def load_image(image_path):
    img = Image.open(image_path )
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
    return(preds)
#deleing  video to save space on the server
def delete_uploaded_file():
    try:
        os.remove(videopath)
        return 1
    except:
        return 0
#saving video
def save_uploaded_file(uploaded_file,type=["mp4","avi","webm","mov",""]):
    try:
        with open(os.path.join('static/videos',uploaded_file.name),'wb') as f:
            f.write(uploaded_file.getbuffer())
        return 1    
    except:
        return 0
#put queries here
search = st.text_input("Type The Name Of Search Object....")
#setting upload file whith required video types
uploaded_file = st.file_uploader("Upload Video",type=["mkv","mp4",'avi','flv','webm','vob','mov','ogg','wmv','3gp'])
#handling uploads
if uploaded_file is not None:
    notfound = True # search flag
    if save_uploaded_file(uploaded_file):#handling saving and video proccessing
        capture = cv2.VideoCapture(os.path.join('static/videos',uploaded_file.name))
        global videopath 
        videopath = os.path.join('static/videos',uploaded_file.name)
        st.video(os.path.join('static/videos',uploaded_file.name))
        file_ = open(os.path.join('static/images/loading.gif'), "rb")
        contents = file_.read()
        data_url = base64.b64encode(contents).decode("utf-8")
        file_.close()

        st.markdown(
            f'<center><img src="data:image/gif;base64,{data_url}" alt="cat gif"></center>',
            unsafe_allow_html=True,
        )
        frameNr = 0
        success, frame = capture.read()
        while (success):
        
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
                    pic = cv2.putText(disp_img, search + " Is On this Frame", (40,40), cv2.FONT_HERSHEY_TRIPLEX , 1.8, (0,0,0))
                    st.image(pic)
                    st.success("Other Items Detected : " + str(predition_names))
                    os.remove(os.path.join(f'static/images/{frameNr}.jpg'))#deleting the image to savespace 
                    break
            else:
                break
        
            frameNr = frameNr+1
        
        capture.release()
        time.sleep(20) # delay b4 deleting the video
        if notfound :
            st.warning("Item you searched was not found ")
            st.success("Other Items Detected : " + str(predition_names))
        st.success("Code Executed Successfully !!!!!!!!!!")
        delete_uploaded_file()

