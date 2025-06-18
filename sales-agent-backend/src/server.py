from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from api.conversation.routers import router as chat_routers
import uvicorn
import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

app = FastAPI()

# Routers
app.include_router(chat_routers)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
) # First


def main():
    print(".::.Sales AI Agent API service is running...")
    try:
        uvicorn.run(
            app="server:app",
            reload=eval(os.getenv('UVICORN_RELOAD')),
            host=os.getenv('UVICORN_HOST'),
            port=int(os.getenv('UVICORN_PORT'))
        )
    except KeyboardInterrupt:
        print("\n.::.Service terminated!")
        exit(0)

if __name__ == "__main__":
    main()