from collections import deque
from flask import Flask, request, render_template

from spikeinterface_chatbot.lang_chain_machinery import query_documentation

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        chat_history = (
            deque(maxlen=3) if not locals().get("chat_history") else chat_history
        )  # Hack to initalize, TODO: Improve
        question = request.form["message"]
        persist_directory = "./data/chroma_database"
        anwser = query_documentation(query=question, chat_history=chat_history, persist_directory=persist_directory)
        chat_history.appendleft((question, anwser))

        return anwser
    else:
        return render_template("chat.html")


if __name__ == "__main__":
    app.run()
