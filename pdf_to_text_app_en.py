import streamlit as st
import fitz  # PyMuPDF, a library to handle PDF files
import os

def save_uploaded_file(uploaded_file):
    """Save the uploaded file to disk."""
    try:
        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return uploaded_file.name
    except Exception as e:
        return st.error(f"Failed to save file: {e}")

def pdf_to_text(pdf_path):
    """Convert PDF file content to text."""
    doc = fitz.open(pdf_path)
    text = ""
    # Iterate through each page
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

def main():
    st.title("PDF to Text Converter")
    
    # File uploader
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    # Show the "Start Conversion" button
    if st.button("Start Conversion",type="primary"):
        if uploaded_file is not None:
            # Save the uploaded PDF file to a temporary file
            saved_file = save_uploaded_file(uploaded_file)
            if saved_file:
                try:
                    text = pdf_to_text(saved_file)
                    st.write("PDF Text Content:")
                    st.text_area("Text", value=text, height=300)
                    # Provide a download text feature
                    st.download_button(label="Download Text", data=text, file_name="converted_text.txt", mime="text/plain")
                except Exception as e:
                    st.error(f"Error reading PDF file: {e}")
                finally:
                    # Delete the temporary file
                    os.remove(saved_file)
        else:
            # If no file is uploaded, show a warning message
            st.warning("Please upload a PDF file first!")

    # Feature Description
    st.subheader("Feature Description")
    st.write("""
        - This application allows users to upload a PDF file and convert its content to text.
        - Users can initiate the conversion process by clicking the 'Start Conversion' button.
        - After conversion, the text is displayed, and there is an option to download the text.
    """)
    
    # Usage Instructions
    st.subheader("Usage Instructions")
    st.write("""
        1. Click 'Choose a PDF file' to upload your PDF file.
        2. Click 'Start Conversion' to begin the conversion process.
        3. Once the conversion is complete, the text will be displayed below.
        4. Click 'Download Text' to download the converted text to your local machine.
    """)

if __name__ == "__main__":
    main()
