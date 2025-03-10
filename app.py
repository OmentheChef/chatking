import streamlit as st
import openai
import PyPDF2
from io import BytesIO

# Set up OpenAI API key
openai.api_key = 'your_openai_api_key'

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

# Function to query the OpenAI model
def get_response_from_model(query, document_text=None):
    prompt = query
    if document_text:
        prompt = f"Based on the following document, answer the question: \n\n{document_text}\n\nQuestion: {query}"
    
    response = openai.Completion.create(
        model="text-davinci-003",  # or "claude" if available via API
        prompt=prompt,
        max_tokens=500,
        temperature=0.7,
    )
    return response.choices[0].text.strip()

# Function to generate a screenplay
def generate_screenplay(scene_description):
    prompt = f"Write a screenplay scene based on this description: {scene_description}. Ensure the screenplay follows proper formatting, only showing what is visible, with action-based writing and dialogue with subtext."
    response = openai.Completion.create(
        model="text-davinci-003",  # or another model
        prompt=prompt,
        max_tokens=500,
        temperature=0.7,
    )
    return response.choices[0].text.strip()

# Streamlit UI setup
def app():
    st.title("Document Chatbot & Screenplay Generator")

    st.sidebar.title("Options")
    mode = st.sidebar.radio("Choose Mode", ["Chat with Document", "Screenplay Writer"])

    if mode == "Chat with Document":
        # File upload
        uploaded_file = st.file_uploader("Upload a document (PDF)", type="pdf")
        if uploaded_file is not None:
            # Extract text from the PDF
            document_text = extract_text_from_pdf(uploaded_file)
            st.write("Document loaded successfully. You can now ask questions.")

            # User input
            query = st.text_input("Ask me anything about the document:")
            if query:
                response = get_response_from_model(query, document_text=document_text)
                st.write(response)
        else:
            st.write("Please upload a PDF document to begin.")

    elif mode == "Screenplay Writer":
        # Input for screenplay description
        scene_description = st.text_area("Enter scene description:")
        if scene_description:
            # Generate screenplay based on description
            screenplay = generate_screenplay(scene_description)
            st.write("Generated Screenplay:")
            st.write(screenplay)

# Run the Streamlit app
if __name__ == "__main__":
    app()
