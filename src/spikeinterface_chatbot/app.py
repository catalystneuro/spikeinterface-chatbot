import os

from flask import Flask, request, render_template, jsonify

from spikeinterface_chatbot.lang_chain_machinery import query_documentation

app = Flask(__name__)


@app.route("/process_message", methods=["POST"])
def process_message():
    message = request.form["message"]
    answer_to_query, web_links = query_documentation(query=message)

    response = {"answer": answer_to_query, "links": web_links}

    return jsonify(response)


@app.route("/", methods=["GET"])
def chat():
    return render_template("chat.html")


if __name__ == "__main__":
    app.run()
