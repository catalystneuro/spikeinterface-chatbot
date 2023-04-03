from pathlib import Path
from typing import Optional, List, Set, Tuple

from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.schema import Document

from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

from .database_services import retrieve_qdrant_database


def query_documentation(query: str, verbose: bool = False) -> Tuple[str, List[str]]:
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
    verbose : bool, false by default:
        If True, the function will print the intermediate steps.

    Returns
    -------
    str
        An answer to the query question.
    """

    vectorstore = retrieve_qdrant_database()
    model_name = "gpt-3.5-turbo"  # Cheaper than default davinci
    max_tokens = None  # Exposed to experiment with different values
    llm = ChatOpenAI(temperature=0, model_name=model_name, max_tokens=max_tokens)
    retriever = vectorstore.as_retriever()
    chat_prompt = create_prompt()
    return_source_documents = True
    chain_type_kwargs = dict(prompt=chat_prompt)
    question_and_answer_chain = RetrievalQA.from_chain_type(
        llm,
        chain_type_kwargs=chain_type_kwargs,
        retriever=retriever,
        return_source_documents=return_source_documents,
        verbose=verbose,
    )

    chain_response = question_and_answer_chain(query)
    answer_to_query = chain_response["result"]
    source_documents = chain_response["source_documents"]

    # Get link to sources
    web_links = return_links_from_sources(source_documents)
    return answer_to_query, web_links


def return_links_from_sources(source_documents: List[Document]) -> List[str]:
    source_metadata = (source.metadata for source in source_documents)
    local_links_to_documentation = (metadata["source"] for metadata in source_metadata)
    web_links_to_documentation = {transform_local_link_to_web_url(link) for link in local_links_to_documentation}

    return list(web_links_to_documentation)


def transform_local_link_to_web_url(local_link: str) -> str:
    local_directory_location = "rtdocs"
    local_link = local_link.split(local_directory_location)[1][1:]  # Remove leading slash
    web_link = f"https://{local_link}"

    return web_link


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
