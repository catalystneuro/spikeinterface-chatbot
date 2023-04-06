
# Spikeinterface questions
A chatbot to answer documentations in spikeinterface.

This is a flask app that uses LangChain and OpenAI model for answering questions using the documentation of spikeinterface.

## How to run the app locally?
```bash
flask --app spikeinterface_chatbot.app run
```

Note that for running the app locally your OpenAI key should be an environment variable:

```bash
export OPENAI_API_KEY="your_key_goes_here"
export QDRANT_API_KEY="your_quadrant_api_key_goes_here"
```

## Docker

### How to build the docker image
```bash
docker build -t spikeinterface_chatbot_container .
```
Where the -t adds the name as a tag of the docker file so it can be referenced later.

### How to run the app from docker
```bash
docker run -d -p 5000:80  spikeinterface_chatbot_container
```
Where the -d is the detach command (so you get back your terminal) and the -p is mapping port 5000 in the local computer to port 80 on the container.

Note that for running the docker container locally you will need to pass your OpenAI key as an environment variable:

```bash
docker run -d -p 5000:80 -e OPENAI_API_KEY=your_key_goes_here -e QDRANT_API_KEY=your_quadrant_api_key_goes_here spikeinterface_chatbot_container
```

### How to push a docker container to github register container
```bash
docker tag spikeinterface_chatbot_container ghcr.io/catalystneuro/spikeinterface_chatbot_container:latest
docker push ghcr.io/catalystneuro/spikeinterface_chatbot_container:latest
```
