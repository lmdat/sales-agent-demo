import os
from datetime import datetime
from textwrap import dedent
from dotenv import load_dotenv, find_dotenv
from langchain_core.messages import AIMessage
from ...states.sales_agent_state import SalesAgentState
from litellm import completion
from logger import logger
from ...utils.helpers import parsing_messages_to_history, remove_think_tag
from ...utils.const_prompts import (
    CONST_ASSISTANT_NAME,
    CONST_ASSISTANT_ROLE,
    CONST_ASSISTANT_SKILLS,
    CONST_ASSISTANT_TONE,
    CONST_FORM_ADDRESS_IN_VN,
    CONST_ASSISTANT_SCOPE_OF_WORK,
    CONST_ASSISTANT_PRIME_JOB
)
from config import LLM_MODELS

load_dotenv(find_dotenv())

def wanna_exit_node(state: SalesAgentState):
    user_input = state.get('human_input', '')    
    chat_history = parsing_messages_to_history(state.get('messages', ''))

    prompt =f"""
    # Role
    {CONST_ASSISTANT_ROLE}

    # Skills
    {CONST_ASSISTANT_SKILLS}
    
    # Tone
    {CONST_ASSISTANT_TONE}

    # Tasks
    - The User does not want to talk anymore. Assistant HAVE TO reply gently and try to retain the User for another chance to purchase the products in the future.

    # Constraints
    - Assistant MUST keep the answer concise and clear. Highly recommend under 100 words.
    - Assistant MUST use the same language as the User's language to reply.
    {CONST_FORM_ADDRESS_IN_VN}

    Chat History:
    ```
    {chat_history}
    ```

    User's Input: {user_input}
    Answer:
    """

    prompt = dedent(prompt)

    response = completion(
        api_key=os.environ["GROQ_API_KEY"],
        model=LLM_MODELS['exit_subgraph']['exit_node'],
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]        
    )

    logger.info(f"Usage Tokens: {response.usage}")

    usage_tokens = state.get('usage_tokens')
    usage_tokens.input += response.usage.prompt_tokens
    usage_tokens.output += response.usage.completion_tokens
    usage_tokens.total += response.usage.total_tokens
    
    ai_message = AIMessage(
        content=remove_think_tag(response.choices[0].message.content),
        additional_kwargs={
            "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "usage_tokens": usage_tokens.model_dump()
        }
    )

    return {
        "messages": ai_message,
        "ai_reply": ai_message,
        "usage_tokens": usage_tokens,
        "product_requirement": None,
        "order_info": None,
        "delivery_info": None,
        "product_chat_history": None,
        "order_chat_history": None,
        "order_payload": None,
        "items_not_in_stock": []
    }
