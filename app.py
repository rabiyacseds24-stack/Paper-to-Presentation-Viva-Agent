
import streamlit as st

from pdf_reader import read_pdf
from rag import create_database
from router import detect_intent
from sample_paper import SAMPLE_PAPER
from ppt_generator import create_ppt

from agents import (
    summarize_paper,
    extract_concepts,
    generate_slides,
    generate_viva
)

st.set_page_config(
    page_title="Paper-to-Presentation & Viva Agent",
    page_icon="📚"
)

st.title("📚 Paper-to-Presentation & Viva Agent")

st.write(
    "Upload a research paper and generate summaries, "
    "concepts, slides and viva questions."
)

option = st.radio(
    "Choose Research Paper",
    ["Upload PDF", "Use Sample Paper"]
)

uploaded_file = None

if option == "Upload PDF":
    uploaded_file = st.file_uploader(
        "Upload Research Paper",
        type=["pdf"]
    )
 
if option == "Use Sample Paper":

    st.success("Sample research paper selected!")

    if st.button("Process Research Paper"):
        st.session_state.paper_text = SAMPLE_PAPER
        st.session_state.db = create_database(SAMPLE_PAPER)

        st.success("Sample paper processed successfully!")

elif uploaded_file is not None:

    st.success("PDF uploaded successfully!")

    if st.button("Process Research Paper"):

        with st.spinner("Reading and processing PDF..."):

            paper_text = read_pdf(uploaded_file)

            if paper_text.strip():
                st.session_state.paper_text = paper_text
                st.session_state.db = create_database(paper_text)

                st.success("Research paper processed successfully!")

            else:
                st.error("No text found in the PDF.")
if "db" in st.session_state:

    st.subheader("Ask Your Research Paper")

    question = st.text_input(
        "What would you like to generate?"
    )

    if st.button("Generate Answer"):

        if question.strip():

            intent = detect_intent(question)

            docs = st.session_state.db.similarity_search(
                question,
                k=4
            )

            context = "\n\n".join(
                doc.page_content for doc in docs
            )

            with st.spinner("Generating response..."):

                if intent == "summary":
                    answer = summarize_paper(context)

                elif intent == "concepts":
                    answer = extract_concepts(context)

                elif intent == "slides":
                    answer = generate_slides(context)

                elif intent == "viva":
                    answer = generate_viva(context)

                else:
                    answer = st.session_state.db.similarity_search(
                        question, k=4
                    )

                    answer = "\n\n".join(
                        doc.page_content for doc in answer
                    )

            st.subheader("Generated Result")
            st.write(answer)
            if intent == "slides":

                ppt_file = create_ppt(answer)

                with open(ppt_file, "rb") as file:
                    st.download_button(
                        label="Download PowerPoint",
                        data=file,
    file_name="Research_Presentation.pptx",
                        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                    )           

        

        else:
            st.warning("Please enter your question.")
