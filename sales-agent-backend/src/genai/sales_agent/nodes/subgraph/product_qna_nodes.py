import os
import json
from textwrap import dedent
from dotenv import load_dotenv, find_dotenv
from datetime import datetime
from ...states.sales_agent_state import SalesAgentState
from ...utils.helpers import (
    parsing_messages_to_history,
    remove_think_tag,
    extract_json_from_triple_backticks,
    extract_vectordb_results
)
from ...utils.const_prompts import (
    CONST_ASSISTANT_ROLE,
    CONST_ASSISTANT_SKILLS,
    CONST_ASSISTANT_TONE,
    CONST_FORM_ADDRESS_IN_VN,
    CONST_COMPANY_HOTLINE,
    CONST_PRODUCT_CATEGORY_DESCRIPTION
)
from litellm import completion
from logger import logger
from pydantic.tools import parse_obj_as
from langchain_core.messages import AIMessage
from langgraph.types import Command
from ...schemas.product_requirement import ProductRequirementSchema
from pinecone import Pinecone
from config import LLM_MODELS

load_dotenv(find_dotenv())

def _search_pinecone_vectordb(query: str, category: str='', price_condition: str='', limit_result: int=2):
    pinecone_client = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index = pinecone_client.Index(os.getenv("PINECONE_INDEX_NAME"))

    query_payload = {
        "inputs": {"text": query}, 
        "top_k": limit_result,
        "filter": {}
    }

    if price_condition != '':
        aparts = price_condition.split('|')
        conditions = []
        for item in aparts:
            item_aparts = item.split(':')
            conditions.append({
                f"{item_aparts[0]}": int(item_aparts[1])
            })

        if len(conditions) == 1:
            query_payload['filter'] = {
                "price": conditions[0]
            }
        else:
            query_payload['filter'] = {
                "$and": [{"price": cond} for cond in conditions]
            }
    
    if category != '':
        query_payload['filter']['category'] = category

    logger.info(query_payload)

    results = index.search_records(
        namespace=os.getenv("PINECONE_NAMESPACE_PRODUCT", "product-info"),
        query=query_payload,
        fields=["title", "category", "price", "chunk_content"],        
    )
    logger.info(results)
    return results.to_dict()


def analyze_product_requirement_node(state: SalesAgentState):
    logger.debug(">>>analyze_product_requirement_node called!")
    # user_input = state['messages'][-1].content
    user_input = state.get('human_input', '')
    # chat_history = parsing_messages_to_history(state.get('messages', ''))
    product_chat_history = state.get('product_chat_history', '')

    json_output_example = {
        'requirement': 'Yêu cầu về sản phẩm của User',
        'category': 'Loại sản phẩm',
        'price_condition': 'Điều kiện giá sản phẩm của User'
    }

    prompt = f"""
    # Role
    - Assistant là một chuyên gia phân tích, trích xuất nội dung văn bản với 10 năm kinh nghiệm.

    # Skills
    - Assistant có kỹ năng Sales, kỹ năng phân tích dữ liệu. 
    - Assistant biết định dạng dữ liệu JSON.
    
    # Tasks
    - Dựa vào User's input, Assistant MUST tạo content bằng định dạng JSON gồm có các field dữ liệu sau:
    1. User Requirement:
        - Field name: requirement
        - Description: User đang tìm sản phẩm gì? Tên sản phẩm đó là gì? Hoặc tìm một sản phẩm có đặc tính như thế nào? Các vấn đề User cần giải quyết bằng các sản phẩm skincare: Đầu bị gàu; Da mặt bị dầu/nhờn/mụn; Thanh lọc không khí; Khử mùi hiệu quả.

    
    2. Category:
        - Field name: category
        - Description: 
            - Assistant MUST phân loại sản phẩm mà User muốn tìm vào các loại sau:
                {CONST_PRODUCT_CATEGORY_DESCRIPTION}
            - Nếu Assistant không phân loại được, return ""

    3. Price Condition:
        - Field name: price_condition
        - Description: Điều kiện về mức giá sản phẩm mà User muốn tìm. Nếu User không đề cập gì về mức giá, return ""
        - Example:
            - Có dầu gội đầu nào trị gàu dưới 100000 không? Return "$lt:100000"
            - Có nước hoa nào khoảng tầm 500000 không? Return "$lte:500000"
            - Có nước hoa nào khoảng 1000000 đổ lại không? Return "$lte:1000000"
            - Có nước hoa nào khoảng tầm 500000 đến 1000000 không? Return "$gte:500000|$lte:1000000"
            - Có sữa tắm nào khoảng 200000 - 800000 không? Return "$gte:200000|$lte:800000"
    
    # Output
    - Assistant MUST trả lời bằng JSON format với các field như sau:
    ```
    {json.dumps(json_output_example, ensure_ascii=False)}
    ```

    # Constraints
    - Assistant MUST chú ý đến Product Chat History, User's input để phân tích và trích xuất đúng dữ liệu.
    - Assistant DO NOT sử dụng example data để tạo câu trả lời, AVOID create the content yourself.
    - Assistant MUST use the same language as the User's language to reply.
    - Assistant MUST chú ý cách viết tắt về giá, số tiền của User trong tiếng Việt:
        - 1k = 1000 VND
        - 100k = 100000 VND
        - 1 cành = 1000 VND
        - 100 cành = 100000 VND
        - 1 lít = 100000 VND
        - 1 củ = 1000000 VND
        - 1 chai = 1000000 VND

    Product Chat History:
    ```
    {product_chat_history}
    ```

    User's input: {user_input}
    Answer:
    """

    prompt = dedent(prompt)

    response = completion(
        api_key=os.environ["GROQ_API_KEY"],
        model=LLM_MODELS['product_qna_subgraph']['analyze_product_node'],
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        # response_format=ProductRequirementSchema
    )

    
    logger.info(f"Raw Product Requirement Response: {response.choices[0].message.content}")
    msg_content = remove_think_tag(response.choices[0].message.content)
    logger.info(f"Product Requirement Response: {msg_content}")
    
    product_requirement =  parse_obj_as(ProductRequirementSchema, extract_json_from_triple_backticks(msg_content))
    # product_requirement =  parse_obj_as(ProductRequirementSchema, json.loads(msg_content))
    if product_requirement.requirement == "":
        product_requirement.requirement = user_input

    logger.success(f"Product Requirement: {product_requirement}")

    logger.info(f"Usage Tokens: {response.usage}")

    usage_tokens = state.get('usage_tokens')
    usage_tokens.input += response.usage.prompt_tokens
    usage_tokens.output += response.usage.completion_tokens
    usage_tokens.total += response.usage.total_tokens

    return {
        "product_requirement": product_requirement,
        "usage_tokens": usage_tokens
    }

def product_qna_node(state: SalesAgentState):
    logger.debug(">>>product_qna_node called!")
    user_input = state.get('human_input', '')
    product_requirement = state.get('product_requirement', None)

    results = _search_pinecone_vectordb(
        query=product_requirement.requirement,
        category=product_requirement.category,
        price_condition=product_requirement.price_condition,
        limit_result=3
    )
    context_data = extract_vectordb_results(results, None)

    logger.info(f"Context Data: {context_data}")

    prompt = f"""
    # Role
    {CONST_ASSISTANT_ROLE}

    # Skills
    {CONST_ASSISTANT_SKILLS}

    # Tone
    {CONST_ASSISTANT_TONE}
    {CONST_FORM_ADDRESS_IN_VN}

    # Context
    ```
    {context_data}
    ```

    # Tasks
    - Dựa vào data trong mục Context, Assistant MUST thực hiện các nhiệm vụ sau:
    1. Assistant MUST recommend sản phẩm cho User với full information.
    2. Nếu không có sản phẩm phù hợp (hoặc không tìm thấy trong mục Context), Assistant MUST reply là không có sản phẩm phù hợp.
    3. Assistant ALWAYS suggest User to place an order and ask for the User's phone number when giới thiệu sản phẩm.
    4. Assistant MUST giới thiệu tất cả các sản phẩm trong mục Context mà phù hợp với User's input.

    # Output
    - Assistant MUST reply the list of products by the following format:
    ```
    **Tên sản phẩm:** product_name<br>
    **SKU:** sku<br>
    **Loại sản phẩm:** category<br>
    **Giá:** price<br>
    **Mô tả:** description<br>
    **Link sản phẩm:** url<br>
    --------------------<br>
    **Tên sản phẩm:** product_name<br>
    **SKU:** sku<br>
    **Loại sản phẩm:** category<br>
    **Giá:** price<br>
    **Mô tả:** description<br>
    **Link sản phẩm:** url<br>
    ```

    # Constraints
    - List of products MUST be illustrated in markdown format.  
    - The Description of each product MUST be shortened (keep under 30 words) but still keep enough meaning.
    - Assistant MUST ONLY sử dụng dữ liệu được cung cấp trong mục Context để reply, AVOID create the content yourself.
    - Assistant MUST keep the answer concise and focused to the question.
    - IN ALL CIRCUMSTANCES, khi Assistant không có câu trả lời (không tìm được nội dung trong phần Context hoặc no data in Context) cho những câu hỏi của User, Assistant MUST reply là mình chưa có thông tin cụ thể về câu hỏi của User, đồng thời Assistant MUST suggest User liên hệ số hotline: {CONST_COMPANY_HOTLINE} để được hỗ trợ thêm.
    - Assistant MUST use the same language as the User's language to reply.    
    
    User's input: {user_input}
    Answer:
    """

    prompt = dedent(prompt)

    response = completion(
        api_key=os.environ["GROQ_API_KEY"],
        model=LLM_MODELS['product_qna_subgraph']['product_qna_node'],
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

    logger.info(f"Product QnA Response: {response.choices[0].message.content}")
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

def update_product_chat_history_node(state: SalesAgentState):
    user_input = state.get('human_input', '')
    product_chat_history = state.get('product_chat_history', '')
    ai_reply = state.get('ai_reply', None)

    if ai_reply is not None and isinstance(ai_reply, AIMessage):
        product_chat_history += f"""User: {user_input}
        Supporter: {ai_reply.content}\n\n
        """

    return {
        "product_chat_history": product_chat_history
    }

