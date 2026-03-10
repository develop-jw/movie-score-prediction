#from fastapi import FastAPI
#from settings import settings
#from model.router import router as model_router


#app = FastAPI()
#app.include_router(model_router)


#@app.get("/")
#async def get_health() -> dict[str, str]:
#    return {"message": "new version ok"}


#if __name__ == "__main__":
#    import uvicorn

#    uvicorn.run("main:app", host=settings.server_host, port=settings.server_port)


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from settings import settings
from model.router import router as model_router


app = FastAPI()

# 브라우저에서 API 호출 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(model_router)

# static 폴더 안의 파일들을 서빙
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def get_health():
    # localhost:8000 접속하면 UI 페이지를 보여줌
    return FileResponse("static/index.html")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host=settings.server_host, port=settings.server_port)