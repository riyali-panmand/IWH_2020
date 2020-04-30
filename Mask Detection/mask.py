import streamlit as st
from os import listdir
from os.path import isfile, join
from PIL import Image
import test
st.sidebar.title("About")
st.sidebar.info("The application generates the high resolution of the selected low resolution image. It was built using a deep network with adversarial network-Generative Adversarial Networks")
onlyfiles = [f for f in listdir("C:\\Users\\Riyali\\Desktop\\Keras-SRGAN-master\\project\\data\\") if isfile(join("C:\\Users\\Riyali\\Desktop\\Keras-SRGAN-master\\project\\data\\", f))]
#imageselect = st.sidebar.selectbox("Pick an image.", onlyfiles)

st.title('Super Resolution')
st.subheader("Pick an image from the left. You'll be able to view the image.")
st.subheader("When you're ready, submit a prediction on the left.")

st.write("")
st.sidebar.title("Generate Image")
imageselect = st.sidebar.selectbox("Pick an image.", onlyfiles)
image = Image.open("C:\\Users\\Riyali\\Desktop\\Keras-SRGAN-master\\project\\data\\" + imageselect)
st.image(image, width=300)
if st.sidebar.button('Generate'):
	test.test_model_for_lr_images('data\\'+imageselect)
	#name = test_generated_image_0.png
	gan = Image.open("C:\\Users\\Riyali\\Desktop\\Keras-SRGAN-master\\project\\output\\high_res_result_image.png")
	st.image(gan, width=300)