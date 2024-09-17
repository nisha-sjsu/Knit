from fastapi import FastAPI
from fastapi.routing import APIRoute
from api.main import api_router

def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"

app = FastAPI(
    title="Knit.ai",
    openapi_url=f"/api/v1/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
)

app.include_router(api_router)

@app.on_event("startup")
async def startup_event():
    print("Server running at http://127.0.0.1:8000")
    print(f"OpenAPI schema available at http://127.0.0.1:8000{app.openapi_url}")
