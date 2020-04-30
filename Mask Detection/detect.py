import streamlit as st
from os import listdir
from os.path import isfile, join
from PIL import Image
import object_detection as od

onlyfiles = [f for f in listdir("data\\") if isfile(join("data\\", f))]
#imageselect = st.sidebar.selectbox("Pick an image.", onlyfiles)

st.title('Face Mask Detection')
st.subheader("Pick an image from the left. You'll be able to view the image.")
st.subheader("When you're ready, submit a prediction on the left.")

st.write("")
st.sidebar.title("Generate Image")
imageselect = st.sidebar.selectbox("Pick an image.", onlyfiles)
image = Image.open("data\\" + imageselect)
st.image(image, width=300)
if st.sidebar.button('Generate'):
	od.path('data\\'+imageselect)
	gan = Image.open("mask-detected.jpg")
	st.image(gan)