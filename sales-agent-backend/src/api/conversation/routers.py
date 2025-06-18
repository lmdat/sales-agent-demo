import os
from dotenv import load_dotenv, find_dotenv
from datetime import datetime
from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from .schemas import (
    MessagePayload,
    HistoryMessagesPayload,
    CheckpointPayload
)
from langchain_core.messages import (
    AIMessage,
    HumanMessage
)
from genai.sales_agent.agent import SalesAgentSingleton
from genai.sales_agent.schemas.usage_tokens import UsageTokensSchema
from logger import logger
from markdown import markdown
import uuid

router = APIRouter(
    prefix="/ai"
)

agent = SalesAgentSingleton()

@router.post("/conversation")
async def conversation(payload: MessagePayload):

    cfg = {
        "configurable": {
            "thread_id": payload.thread_id        
        }
    }

    try:
        response = agent.graph.invoke(
            {
                "messages": [
                    HumanMessage(
                        content=payload.message,
                        additional_kwargs={"current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                    )
                ]
            },
            config=cfg
        )

        ai_reply = response.get('ai_reply', None)
        answer_payload = {}
        if ai_reply is None:
            answer_payload = {
                'id': str(uuid.uuid4()),
                'role': 'ai',
                'content': '---Unknown---',
                'usage_tokens': UsageTokensSchema(input=0, output=0, total=0).model_dump(),
                'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        else:
            assert isinstance(ai_reply, AIMessage)
            answer_payload = {
                'id': ai_reply.id,
                'role': 'ai',
                'content': markdown(ai_reply.content),
                'usage_tokens': ai_reply.additional_kwargs.get('usage_tokens'),
                'time': ai_reply.additional_kwargs.get('current_time', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            }

        return JSONResponse(
            content={
                'message': answer_payload,
                'format': 'html', # html or json
            }
        )

    except Exception as err:
        logger.error(err)
        return JSONResponse(
            content={
                'message': {
                    'content': f"{repr(err)}",
                },
                'format': 'html', # html or json
                'error_message': f"{repr(err)}"
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
@router.post("/history")
async def history(payload: HistoryMessagesPayload):

    cfg = {
        "configurable": {
            "thread_id": payload.thread_id        
        }
    }
    history_messages = []

    try:
        snapshot = agent.graph.get_state(config=cfg)
                
        for message in snapshot.values.get('messages', []):
            if isinstance(message, HumanMessage):
                history_messages.append({
                    'id': message.id,
                    'role': 'human',
                    'content': markdown(message.content),
                    'time': message.additional_kwargs.get('current_time', '')
                })
            elif isinstance(message, AIMessage):
                history_messages.append({
                    'id': message.id,
                    'role': 'ai',
                    'content': markdown(message.content),
                    'usage_tokens': message.additional_kwargs.get('usage_tokens', UsageTokensSchema(input=0, output=0, total=0).model_dump()),                    
                    'time': message.additional_kwargs.get('current_time', '')
                })

        return JSONResponse(
            content={
                'history_messages': history_messages
            }
        )
    except Exception as err:
        logger.error(err)
        return JSONResponse(
            content={
                'message': {
                    'content': f"{repr(err)}"
                },
                'format': 'html', # html or json
                'error_message': f"{repr(err)}"
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
@router.post("/delete-conversation")
async def clear_checkpoint(payload: CheckpointPayload):
    
    try:
        conn = agent.graph.checkpointer.conn
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM checkpoints WHERE thread_id = '{payload.thread_id}'")
        cursor.execute(f"DELETE FROM writes WHERE thread_id = '{payload.thread_id}'")
        cursor.close()
        conn.commit()

        logger.info(f"Deleted thread: {payload.thread_id}")

        return JSONResponse(
            content={
                'history_messages': []
            }
        )
    except Exception as err:
        logger.error(err)
        return JSONResponse(
            content={                
                'error_message': f"{repr(err)}"
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )