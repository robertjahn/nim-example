import os

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource

from traceloop.sdk import Traceloop

from models.nim import Nim
from pipeline.basic import Basic
from pipeline.langchain import LangChain
from utils import format_message
from utils.secrets import read_secret

os.environ['TRACELOOP_TELEMETRY'] = "false"
os.environ['OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE'] = "delta"

token = read_secret("otel_event")
headers = {"Authorization": f"Api-Token {token}"}

Traceloop.init(
    app_name="nim-example",
    api_endpoint="https://xbw95514.dev.dynatracelabs.com/api/v2/otlp",
    disable_batch=True,
    headers=headers,
    should_enrich_metrics=True,
)

## End NeMo config

nim = Nim()
ai_models = {
    "nim": nim,
}

basic = Basic()
langchain = LangChain()

pipelines = {
    "none": basic,
    "langchain": langchain,
}

app = FastAPI()

resource = Resource.create(
    {"service.name": "langgraph-travel-advisor", "service.version": "0.1.0"}
)


@app.exception_handler(HTTPException)
async def validation_exception_handler(request, exc):
    return JSONResponse(exc.detail, status_code=500)


####################################
@app.get("/api/v1/completion")
def submit_completion(framework: str, prompt: str):
    with trace.get_tracer("bedrock-travel-advisor").start_as_current_span(name="/api/v1/completion", kind=trace.SpanKind.SERVER) as span:
        clean_prompt = prompt.lower().strip()
        f = framework.lower()
        if not f in pipelines:
            raise HTTPException(
                status_code=404,
                detail=format_message("Sorry, the selected framework doesn't exist"),
            )
        pipeline = pipelines[f]
        try:
            return pipeline.start(nim, clean_prompt)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=format_message("Sorry, there was an error: " + e.message),
            )


if __name__ == "__main__":

    app.mount("/", StaticFiles(directory="./public", html=True), name="public")
    uvicorn.run(app, host="0.0.0.0", port=8080)
