import os
import logging

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"),format='%(asctime)s %(name)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource

from traceloop.sdk import Traceloop

from models.nim import Nim
from pipeline.basic import Basic
from pipeline.rag import Rag
from pipeline.agentic import Agentic
from utils import format_message
from utils.secrets import read_secret

os.environ['TRACELOOP_TELEMETRY'] = "false"
os.environ['OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE'] = "delta"

token = read_secret("otel_event")
dynatrace_oltp_url = os.environ['DYNATRACE_OLTP_URL']
dynatrace_api_token = "Api-Token " + os.environ['DYNATRACE_API_TOKEN']
headers = {"Authorization": dynatrace_api_token}


Traceloop.init(
    app_name="nim-example",
    api_endpoint=dynatrace_oltp_url,
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
rag = Rag()
agentic = Agentic()

pipelines = {
    "basic": basic,
    "rag": rag,
    "agentic": agentic,
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
    with trace.get_tracer("travel-advisor").start_as_current_span(name="/api/v1/completion", kind=trace.SpanKind.SERVER) as span:
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
    logger.info("Startup - dynatrace_oltp_url = " + dynatrace_oltp_url)
    app.mount("/", StaticFiles(directory="./public", html=True), name="public")
    uvicorn.run(app, host="0.0.0.0", port=8080)
