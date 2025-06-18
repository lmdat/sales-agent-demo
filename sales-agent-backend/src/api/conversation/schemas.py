from pydantic import BaseModel

class MessagePayload(BaseModel):
    thread_id: str = None
    message: str = None

class HistoryMessagesPayload(BaseModel):
    thread_id:str = None

class CheckpointPayload(BaseModel):
    thread_id:str = None