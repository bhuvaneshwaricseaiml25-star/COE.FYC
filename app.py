import streamlit as st
from PIL import Image, ImageOps, ImageEnhance
from io import BytesIO

# PDF conversion
import img2pdf

st.set_page_config(page_title="Document Scanner", layout="centered")

st.title("📄 Black & White Document Scanner")
st.write(
    "Upload a document image, convert it to black & white like Adobe Scan, "
    "then download it as a PDF."
)

uploaded_file = st.file_uploader(
    "Upload an image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:

    # Open image
    image = Image.open(uploaded_file)

    st.subheader("Original Image")
    st.image(image, use_container_width=True)

    # Convert button
    if st.button("Convert to Black & White PDF"):

        # Convert to grayscale
        gray = ImageOps.grayscale(image)

        # Increase contrast for scan-like effect
        enhancer = ImageEnhance.Contrast(gray)
        bw_image = enhancer.enhance(2.5)

        # Optional threshold for stronger black/white effect
        bw_image = bw_image.point(lambda x: 0 if x < 140 else 255, '1')

        st.subheader("Scanned Preview")
        st.image(bw_image, use_container_width=True)

        # Save processed image to memory
        img_bytes = BytesIO()
        bw_image.save(img_bytes, format="PNG")
        img_bytes.seek(0)

        # Convert image to PDF
        pdf_bytes = img2pdf.convert(img_bytes.getvalue())

        st.download_button(
            label="📥 Download PDF",
            data=pdf_bytes,
            file_name="scanned_document.pdf",
            mime="application/pdf"
        )
