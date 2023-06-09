import streamlit as st
import cv2
import io
import base64
from PIL import Image

def get_image_download_link(img, filename, text):
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:file/txt;base64,{img_str}" download="{filename}">{text}</a>'
    return href

def save_image(img):
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    byte_im = buf.getvalue()
    return byte_im

st.title('Template Matching')

temp_file_name = st.file_uploader("Choose a template image file", type=['jpg', 'png'])
if temp_file_name is not None:
    temp_image = cv2.imread('./images/' + temp_file_name.name)
    st.image(temp_image, use_column_width=None, channels="BGR")

main_file_name = st.file_uploader("Choose an image file", type=['jpg', 'png'])
if main_file_name is not None:
    main_image = cv2.imread('./images/' + main_file_name.name)
    st.image(main_image, use_column_width=None, channels="BGR")

st.header('Result:')
res_info = st.text('Select all files!')
if temp_file_name is not None and main_file_name is not None:
    temp_image_gray = cv2.cvtColor(temp_image, cv2.COLOR_BGR2GRAY)
    main_image_gray = cv2.cvtColor(main_image, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(temp_image_gray, main_image_gray, cv2.TM_CCOEFF_NORMED)
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(result)

    (startX, startY) = maxLoc
    endX = startX + temp_image.shape[1]
    endY = startY + temp_image.shape[0]

    res_image = cv2.rectangle(main_image, (startX, startY), (endX, endY), (255, 0, 0), 3)

    res_info.text('')

    st.image(res_image, use_column_width=None, channels="BGR")

    res_image = cv2.cvtColor(res_image, cv2.COLOR_BGR2RGB)
    save_img = Image.fromarray(res_image)
    st.markdown(get_image_download_link(save_img, 'test.jpg', 'Download test'), unsafe_allow_html=True)

    btn = st.download_button(
        label="Download Image",
        data=save_image(save_img),
        file_name="test.jpg",
        mime="image/jpeg",
    )