from fastapi import FastAPI, BackgroundTasks, WebSocket
from ws_router import router as ws_router

app = FastAPI()

app.include_router(ws_router, tags=["ws"])

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.post("/connect")
async def connect(name: str):
    return {"message": f"Hello {name}"}


def write_notification(email: str, message: str):
    with open("logs/log.txt", "a") as email_file:
        content = f"notification {email}: {message}\n"
        email_file.write(content)


@app.get("/notifications")
async def notifications():
    with open("logs/log.txt", "r") as email_file:
        content = email_file.read()
        return { "message": content}

@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message=f"new visitor")
    return {"message": "Notification sent in the background"}
