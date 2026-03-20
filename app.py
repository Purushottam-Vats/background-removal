import streamlit as st
from rembg import remove
from PIL import Image, ImageDraw
import io
from streamlit_image_comparison import image_comparison

st.set_page_config(page_title="AI BG Remover Studio", layout="centered")

st.title("🖼️ AI Creator Studio - Background Remover")
st.write("Upload an image, remove background, customize & download!")

# Upload single image (stable version)
uploaded_file = st.file_uploader(
    "Upload Image",
    type=["png", "jpg", "jpeg"]
)

# Background option
bg_option = st.selectbox(
    "Choose Background",
    ["Transparent", "White", "Black", "Custom Color"]
)

bg_color = "#ffffff"
if bg_option == "Custom Color":
    bg_color = st.color_picker("Pick Background Color", "#ffffff")

# Text overlay
text = st.text_input("Add Text on Image (optional)")

# Download format
format_option = st.selectbox("Download Format", ["PNG", "JPG"])

# Process only when button clicked
if uploaded_file and st.button("🚀 Remove Background"):

    # FIX: Safe file reading (avoids UnicodeDecodeError)
    file_bytes = uploaded_file.read()

    try:
        input_image = Image.open(io.BytesIO(file_bytes)).convert("RGBA")
    except Exception as e:
        st.error(f"Error loading image: {e}")
        st.stop()

    st.subheader("📷 Original Image")
    st.image(input_image, use_column_width=True)

    # Resize for faster processing
    input_image.thumbnail((512, 512))

    # Convert to bytes
    input_bytes = io.BytesIO()
    input_image.save(input_bytes, format="PNG")

    # Remove background (FAST MODEL)
    with st.spinner("Removing background..."):
        output_bytes = remove(input_bytes.getvalue())

    output_image = Image.open(io.BytesIO(output_bytes)).convert("RGBA")

    # Apply background
    if bg_option != "Transparent":
        color_map = {
            "White": "#ffffff",
            "Black": "#000000",
            "Custom Color": bg_color
        }
        bg = Image.new("RGBA", output_image.size, color_map.get(bg_option, "#ffffff"))
        bg.paste(output_image, (0, 0), output_image)
        output_image = bg

    # Add text
    if text:
        draw = ImageDraw.Draw(output_image)
        draw.text((20, 20), text, fill="white")

    # Compare
    st.subheader("🔍 Before vs After")
    image_comparison(
        img1=input_image,
        img2=output_image,
        label1="Original",
        label2="Processed"
    )

    # Show result
    st.subheader("✅ Result")
    st.image(output_image, use_column_width=True)

    # Prepare download
    buf = io.BytesIO()
    if format_option == "PNG":
        output_image.save(buf, format="PNG")
        mime_type = "image/png"
        file_ext = "png"
    else:
        output_image.convert("RGB").save(buf, format="JPEG")
        mime_type = "image/jpeg"
        file_ext = "jpg"

    st.download_button(
        label="📥 Download Image",
        data=buf.getvalue(),
        file_name=f"edited.{file_ext}",
        mime=mime_type
    )
