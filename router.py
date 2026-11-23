
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="llama3.2",
    temperature=0
)

prompt = ChatPromptTemplate.from_template("""
Classify the user request into one category:
summary, concepts, slides, viva, chat.

Return only the category.

User request: {question}
""")

router_chain = prompt | llm | StrOutputParser()


def detect_intent(question):
    result = router_chain.invoke({
        "question": question
    })

    result = result.strip().lower()

    allowed = ["summary", "concepts", "slides", "viva", "chat"]

    if result not in allowed:
        return "chat"

    return result
