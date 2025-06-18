import os
from datetime import datetime
from textwrap import dedent
from dotenv import load_dotenv, find_dotenv
from langchain_core.messages import AIMessage
from ...states.sales_agent_state import SalesAgentState
from ...utils.const_prompts import (
    CONST_ASSISTANT_ROLE,
    CONST_ASSISTANT_SKILLS,
    CONST_ASSISTANT_TONE,
    CONST_FORM_ADDRESS_IN_VN,
    CONST_COMPANY_HOTLINE
)
from ...utils.helpers import parsing_messages_to_history, remove_think_tag, extract_vectordb_results
from litellm import completion
from logger import logger
from pinecone import Pinecone
from config import LLM_MODELS

load_dotenv(find_dotenv())



def _search_pinecone_vectordb(query: str, limit_result: int=2):
    pinecone_client = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index = pinecone_client.Index(os.getenv("PINECONE_INDEX_NAME"))

    query_payload = {
        "inputs": {"text": query}, 
        "top_k": limit_result,
    }

    results = index.search_records(
        namespace=os.getenv("PINECONE_NAMESPACE_COMPANY", "company-info"),
        query=query_payload,
        fields=["chunk_content"]
    )
    logger.info(results)
    return results.to_dict()


def company_info_node(state: SalesAgentState):
    user_input = state['messages'][-1].content

    results = _search_pinecone_vectordb(user_input)
    context_data = extract_vectordb_results(results)

    logger.info(context_data)

    prompt = f"""
    # Role
    {CONST_ASSISTANT_ROLE}

    # Skills
    {CONST_ASSISTANT_SKILLS}

    # Tone
    {CONST_ASSISTANT_TONE}
    
    # Context
    ```
    {context_data}
    ```

    # Tasks
    - User sẽ hỏi Assistant những nội dung liên quan đến company info hoặc dịch vụ của công ty. Assistant MUST đọc kỹ User's input và Chat history, sau đó sử dụng dữ liệu được cung cấp trong mục Context để reply.
    
    # Output
    - MUST keep the answers concise, clear and under 200 words.
    - The answers MUST be formatted in an easy to read manner, highly recommend list in bullet point format.

    # Constraints
    - Assistant MUST sử dụng dữ liệu được cung cấp trong mục Context để reply, AVOID create the content yourself.
    - IN ALL CIRCUMSTANCES, khi Assistant không có câu trả lời (không tìm được nội dung trong phần Context) cho những câu hỏi của User, Assistant MUST reply là mình chưa có thông tin cụ thể về câu hỏi của User, đồng thời Assistant MUST suggest User liên hệ số hotline: {CONST_COMPANY_HOTLINE} để được hỗ trợ thêm.
    - Assistant MUST use the same language as the User's language to reply.
    {CONST_FORM_ADDRESS_IN_VN}
    
    User's input: {user_input}
    Answer:  
    """

    prompt = dedent(prompt)

    response = completion(
        api_key=os.environ["GROQ_API_KEY"],
        model=LLM_MODELS['company_info_subgraph']['company_info_node'],
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
