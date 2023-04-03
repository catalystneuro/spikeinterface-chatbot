import os

from flask import Flask, request, render_template, jsonify, g

from spikeinterface_chatbot.lang_chain_machinery import query_documentation
from spikeinterface_chatbot.database_services import build_question_and_answer_retriever

app = Flask(__name__)


def get_retriever():
    """
    Returns the database object for the current session.
    Creates a new one if it doesn't exist.
    """
    if "retriever_chain" not in g:
        # Create the database object and store it in g
        g.retriever_chain = build_question_and_answer_retriever()

    return g.retriever_chain


@app.route("/process_message", methods=["POST"])
def process_message():
    retriever_chain = get_retriever()
    message = request.form["message"]
    query_response = query_documentation(query=message, retriever_chain=retriever_chain)

    response = {"answer": query_response["answer_to_query"], "links": list(query_response["web_links"])}

    return jsonify(response)


@app.route("/", methods=["GET"])
def chat():
    return render_template("chat.html")


if __name__ == "__main__":
    app.run()
