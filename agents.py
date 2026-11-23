
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from prompts import (
    SUMMARY_PROMPT,
    CONCEPT_PROMPT,
    SLIDE_PROMPT,
    VIVA_PROMPT
)

llm = ChatOllama(
    model="llama3.2",
    temperature=0.3
)

def generate_response(system_prompt, context):

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "Research Paper Content:\n{context}")
    ])

    chain = prompt | llm | StrOutputParser()

    return chain.invoke({"context": context})


def summarize_paper(text):
    return generate_response(SUMMARY_PROMPT, text)


def extract_concepts(text):
    return generate_response(CONCEPT_PROMPT, text)


def generate_slides(text):
    return generate_response(SLIDE_PROMPT, text)


def generate_viva(text):
    return generate_response(VIVA_PROMPT, text)
