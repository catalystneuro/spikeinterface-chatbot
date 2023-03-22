import os

from flask import Flask, request, render_template

from spikeinterface_chatbot.lang_chain_machinery import query_documentation

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        chat_history = [] if not locals().get("chat_history") else chat_history  # Hack to initalize, TODO: Improve
        message = request.form["message"]
        persist_directory = "./data/chroma_database"
        response = query_documentation(query=message, chat_history=chat_history, persist_directory=persist_directory)
        chat_history.append(message)
        return response
    else:
        return render_template("chat.html")


if __name__ == "__main__":
    app.run()
