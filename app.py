import streamlit as st
from rembg import remove
from PIL import Image
import io

st.set_page_config(page_title="BG Remover", layout="centered")

st.title("🖼️ AI Background Remover")
st.write("Upload an image and remove its background instantly!")

uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    input_image = Image.open(uploaded_file)

    st.subheader("Original Image")
    st.image(input_image, use_column_width=True)

    if st.button("Remove Background"):
        with st.spinner("Processing..."):
            input_bytes = io.BytesIO()
            input_image.save(input_bytes, format="PNG")
            output_bytes = remove(input_bytes.getvalue())

            output_image = Image.open(io.BytesIO(output_bytes))

        st.subheader("Result Image")
        st.image(output_image, use_column_width=True)

        # Download button
        buf = io.BytesIO()
        output_image.save(buf, format="PNG")
        byte_im = buf.getvalue()

        st.download_button(
            label="Download Image",
            data=byte_im,
            file_name="no_bg.png",
            mime="image/png"
        )