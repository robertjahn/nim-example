

## Setup 

1. Create Dynatrace API token with the [scope required](https://docs.dynatrace.com/docs/shortlink/otel-getstarted-otlpexport#authentication-export-to-activegate) for the OLTP API.
1. Set these environment variables locallu or in the `deploment\nim-example.yaml` file

    ```
    # example
    export NIM_MODEL="meta/llama-3.3-70b-instruct" \
    export NIM_EMBEDDING_MODEL="text-embedding-ada-002" \
    export CLIENT_BASE_URL="http://llama-33-70b-instruct.nim-service:8000/v1/" \
    export LANGCHAIN_LLM_BASE_URL="http://llama-33-70b-instruct.nim-service:8000/v1/" \
    export LANGCHAIN_EMBEDDING_BASE_URL="http://llama-33-70b-instruct.nim-service:8000/v1/" \
    export DYNATRACE_OLTP_URL="https://"**ADJUST**/api/v2/otlp" \
    export DYNATRACE_API_TOKEN=""**ADJUST**"
    ```

## Build

Example with [Podman](https://podman.io/) and [Dockerhub](https://hub.docker.com) as the tools.

```
podman login docker.io
podman build -t dtdemos/nim-example:0.1.0 --platform=linux/amd64 .
podman push dtdemos/nim-example:0.1.0 docker://docker.io/dtdemos/nim-example:0.1.0
```