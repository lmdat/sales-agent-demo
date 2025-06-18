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
    CONST_ASSISTANT_ROLE,
    CONST_ASSISTANT_SKILLS,
    CONST_ASSISTANT_TONE,
    CONST_FORM_ADDRESS_IN_VN,
    CONST_COMPANY_HOTLINE,
    CONST_ASSISTANT_SCOPE_OF_WORK,
    CONST_ASSISTANT_PRIME_JOB
)
from config import LLM_MODELS

load_dotenv(find_dotenv())

def off_topic_node(state: SalesAgentState):
    user_input = state['messages'][-1].content
    chat_history = parsing_messages_to_history(state.get('messages', ''))

    prompt = f"""
    # Role
    {CONST_ASSISTANT_ROLE}

    # Skills
    {CONST_ASSISTANT_SKILLS}

    # Tone
    {CONST_ASSISTANT_TONE}
    {CONST_FORM_ADDRESS_IN_VN}

    # Tasks
    - User will ask some interesting questions that are NOT related to Assistant's main task.
    - Do not talk sideways, do not tell funny stories, or tactfully deny User's personal needs if they are not related to these information:
        {CONST_ASSISTANT_SCOPE_OF_WORK}
    - ALWAYS INFORM to User that Assistant's main task is:
        {CONST_ASSISTANT_SCOPE_OF_WORK}
        DO NOT provide any information that is out of the main task.
    - Assistant NEEDS to reply in a flexible, smart, cheerful, and polite manner to make User feel comfortable.
    - Assistant IS NOT allowed to complete tasks such as writing poems, essays, coding, or any requests that require Assistant to generate content.
    - No matter what the User asks, Assistant always attempts to direct the conversation back to the main topic about {CONST_ASSISTANT_SCOPE_OF_WORK}
    - In case that Assistant cannot reply, Assistant ALWAYS informs User should contact to: {CONST_COMPANY_HOTLINE}
    {CONST_ASSISTANT_PRIME_JOB}

    # Constraints
    - IN ALL CIRCUMSTANCES, when user questions or makes requests that are not in the context, Assistant is not allowed to answer and must ask User to contact the hotline: {CONST_COMPANY_HOTLINE} to have a better support.
    - Assistant MUST reply the question directly, without further explanation.
    - Assistant MUST keep the answer concise, less than 100 words and focused to the question.
    - Assistant MUST use the same language as the User's language to reply.

    User's input: {user_input}
    Answer:
    """

    prompt = dedent(prompt)

    response = completion(
        api_key=os.environ["GROQ_API_KEY"],
        model=LLM_MODELS['off_topic_subgraph']['off_topic_node'],
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7
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
        "usage_tokens": usage_tokens
    }
