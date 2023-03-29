import os

from flask import Flask, request, render_template

from spikeinterface_chatbot.lang_chain_machinery import query_documentation

app = Flask(__name__)


@app.route("/process_message", methods=["POST"])
def process_message():
    message = request.form["message"]
    persist_directory = "./data/chroma_database"
    response = query_documentation(query=message, persist_directory=persist_directory)
    return response


@app.route("/", methods=["GET"])
def chat():
    return render_template("chat.html")


if __name__ == "__main__":
    app.run()
