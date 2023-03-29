from pathlib import Path
from typing import Optional

from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import DirectoryLoader
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)


def create_prompt(system_template: Optional[str] = None) -> ChatPromptTemplate:
    """
    An auxiliary function to create prompts for the chatbot.
    Making it explicit for prompt experimentation.
    """

    if system_template is None:
        system_template = """Use the following pieces of context to answer the users question.
        If you don't know the answer, just say that you don't know, don't try to make up an answer. Also, return the output
        in markdown format.
        ----------------
        {context}"""

    messages = [
        SystemMessagePromptTemplate.from_template(system_template),
        HumanMessagePromptTemplate.from_template("{question}"),
    ]
    chat_prompt = ChatPromptTemplate.from_messages(messages)

    return chat_prompt


def query_documentation(query: str, persist_directory: str, verbose: bool = False) -> str:
    """
    Queries the current database for an answer to the question.

    The procedure under the hood is the following. The question is first sent to the vector store to find the
    related chunks. Those chunks as combined with the question in an `in-context-learning` or
    `retrieval-augmented-generation` manner and sent to the OpenAI language model.

    The language model then generates an answer which is then provided as an output.

    Parameters
    ----------
    query : str
        A question described in natural language.
    persist_directory : str
        The directory where the vectorstore database is located.
    verbose : bool, false by default:
        If True, the function will print the intermediate steps.

    Returns
    -------
    str
        An answer to the query question.
    """
    persist_directory = Path(persist_directory)
    assert persist_directory.exists() and persist_directory.is_dir()

    embedings = OpenAIEmbeddings()
    chroma_vectorstore = Chroma(persist_directory=str(persist_directory), embedding_function=embedings)
    model_name = "gpt-3.5-turbo"  # Cheaper than default davinci
    max_tokens = None
    llm = ChatOpenAI(temperature=0, model_name=model_name, max_tokens=max_tokens)
    retriever = chroma_vectorstore.as_retriever()
    chat_prompt = create_prompt()
    chain_type_kwargs = dict(prompt=chat_prompt)
    question_and_answer_chain = RetrievalQA.from_chain_type(
        llm, chain_type_kwargs=chain_type_kwargs, retriever=retriever, verbose=verbose
    )

    return question_and_answer_chain.run(query)


def generate_chroma_database(read_the_docs_path: str, persist_directory: str) -> None:
    """
    Auxiliary function to generate the croma database (vectorstore).

    Parameters
    ----------
    read_the_docs_path : str
        The paths with the read the docs documentation in html
    persist_directory : str
        The directory where the vectorstore database is located.

    """
    read_the_docs_path = Path(read_the_docs_path)
    assert read_the_docs_path.exists() and read_the_docs_path.is_dir()

    loader = DirectoryLoader(read_the_docs_path, glob="**/*.html")
    docs = []
    for loader in [loader]:
        docs.extend(loader.load())
    sub_docs = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0).split_documents(docs)

    embedings = OpenAIEmbeddings()
    chroma_vectorstore = Chroma.from_documents(sub_docs, embedding=embedings, persist_directory=persist_directory)
    chroma_vectorstore.persist()
    chroma_vectorstore = None
