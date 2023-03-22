from pathlib import Path

from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains.vector_db_qa.base import VectorDBQA
from langchain.llms.openai import OpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import DirectoryLoader


def query_documentation(query: str, persist_directory: str) -> str:
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
    llm = OpenAI(temperature=0, model_name=model_name)
    question_and_answer_chain = VectorDBQA.from_chain_type(llm, vectorstore=chroma_vectorstore)

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
