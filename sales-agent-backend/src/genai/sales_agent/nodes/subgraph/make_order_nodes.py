import os
import json
import re
import httpx
from datetime import datetime
from textwrap import dedent
from dotenv import load_dotenv, find_dotenv
from ...states.sales_agent_state import SalesAgentState
from ...utils.helpers import (
    parsing_messages_to_history,
    remove_think_tag,
    extract_json_from_triple_backticks
)
from ...utils.const_prompts import (
    CONST_ASSISTANT_ROLE,
    CONST_ASSISTANT_SKILLS,
    CONST_ASSISTANT_TONE,
    CONST_FORM_ADDRESS_IN_VN,
    CONST_COMPANY_HOTLINE,
    CONST_COMPANY_NAME
)
from litellm import completion
from logger import logger
from pydantic.tools import parse_obj_as
from langchain_core.messages import AIMessage
from langgraph.types import Command
from ...schemas.order import OrderInfoSchema
from pinecone import Pinecone
from config import LLM_MODELS
import uuid

load_dotenv(find_dotenv())

EMAIL_REGEX = r"^([a-zA-Z0-9._%-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6})*$"
VN_PHONE_REGEX = r"^(0?)(3[2-9]|5[6|8|9]|7[0|6-9]|8[0-6|8|9]|9[0-4|6-9])[0-9]{7}$"



def check_product_chat_history_node(state: SalesAgentState):
    logger.debug(">>>check_product_chat_history_node called!")
    product_chat_history = state.get('product_chat_history', None)
    if product_chat_history is None or product_chat_history == "":
        transfer_to = "product_qna_subgraph"
        return Command(
            goto=transfer_to,
            graph=Command.PARENT
        )


def analyze_order_requirement_node(state: SalesAgentState):
    logger.debug(">>>analyze_order_requirement_node called!")
    user_input = state.get('human_input', '')
    product_chat_history = state.get('product_chat_history', '')
    order_chat_history = state.get('order_chat_history', '')

    # Get delivery info
    delivery_info = state.get('delivery_info', {})
    logger.info(f"Delivery Info: {delivery_info}")
        
    delivery_default = 'NORMAL'
    delivery_list = []
    for key, delivery in delivery_info.items():
        delivery_list.append(f"-{key}: {delivery.get('description', '')}")
        if delivery.get('is_default', 'No') == 'Yes':
            delivery_default = key
            
    

    json_output_example = {
        'customer_name': 'Trần Văn Hùng, Trang Nguyễn',
        'customer_phone': '0123456789',
        'customer_address': '123 Nguyễn Văn Tráng, Quận 1, TP.HCM',
        'customer_email': 'user@example.com',
        'delivery_type': 'NORMAL',
        'order_confirmation': 'No',
        'order_items': [
            {
                'product_name': 'Sữa rửa mặt Senka',
                'category': 'facial-cleanser',
                'sku': 'SUA-RUA-MT-IF-004',
                'ordered_qty': 1,
                'price': 100000.0
            },
            {
                'product_name': 'Dầu gội đầu Biotin',
                'category': 'shampoo',
                'sku': 'DAU-GOI-BC-006',
                'ordered_qty': 4,
                'price': 200000.0
            }
        ]        
    }

    prompt = f"""
    # Role
    - Assistant là một chuyên gia phân tích và trích xuất dữ liệu với 10 năm kinh nghiệm.

    # Skills
    - Assistant có kỹ năng Sales và kỹ năng phân tích dữ liệu.
    - Assistant biết định dạng dữ liệu JSON.

    # Context
    ## Product QnA History
    ```
    {product_chat_history}
    ```

    ## Order Chat History
    ```
    {order_chat_history}
    ```
    
    # Tasks
    - Assistant MUST đọc và phân tích thật kỹ nội dung Product QnA History, Order Chat History trong mục Context và User's input để ensure là các field bên dưới đã được cung cấp dữ liệu:

    1. Customer Name:
        - Field name: customer_name
        - Description: Họ tên của User
        - Default value: là empty string nếu Assistant không tìm thấy dữ liệu trong Context
        - Example: "Trần Văn Hùng", "Trâm Nguyễn", "Phong"
        - Mandatory: Yes

    2. Customer Phone:
        - Field name: customer_phone
        - Description: Số phone của User
        - Default value: là empty string nếu Assistant không tìm thấy dữ liệu trong Context
        - Example: "0909123456"
        - Mandatory: Yes

    3. Customer Address:
        - Field name: customer_address
        - Description: Địa chỉ của User
        - Default value: là empty string nếu Assistant không tìm thấy dữ liệu trong Context
        - Example: "123 Trần Hưng Đạo, Q1, TPHCM"
        - Mandatory: Yes

    4. Customer Email:
        - Field name: customer_email
        - Description: Email của User
        - Default value: là empty string nếu Assistant không tìm thấy dữ liệu trong Context
        - Example: "phong@abc.com", "ba@xyz.net"
        - Mandatory: Yes

    5. Product Name:
        - Field name: product_name
        - Description: Tên sản phẩm mà User muốn mua
        - Default value: là empty string nếu Assistant không tìm thấy dữ liệu trong Context
        - Example: "Tinh dầu xông phòng oải hương nguyên chất Soapberry", "Dầu gội đầu Pantene Pro-V ngăn rụng tóc"
        - Mandatory: Yes

    5. Product Category:
        - Field name: category
        - Description: Loại sản phẩm
        - Default value: là empty string nếu Assistant không tìm thấy dữ liệu trong Context
        - Example: "perfume", "shower-gel"
        - Mandatory: Yes

    6. Product SKU:
        - Field name: sku
        - Description: Mã SKU của sản phẩm mà User muốn mua
        - Default value: là empty string nếu Assistant không tìm thấy dữ liệu trong Context
        - Example: "SUA-RUA-MT-IF-004", "SUA-TAY-MT-IF-005"
        - Mandatory: Yes

    7. Ordered Quantity:
        - Field name: ordered_qty
        - Description: Số lượng của từng sản phẩm mà User muốn mua
        - Default value: là 0 nếu Assistant không tìm thấy dữ liệu trong Context
        - Mandatory: Yes

    8. Price:
        - Field name: price
        - Description: Giá của từng sản phẩm mà User muốn mua
        - Default value: là 0 nếu Assistant không tìm thấy dữ liệu trong Context
        - Mandatory: Yes

    9. Delivery Type:
        - Field name: delivery_type
        - Description: Phương thức giao hàng là một trong 3 phương thức sau:
            {'\n'.join(delivery_list)}
        - Default value: là "{delivery_default}" nếu Assistant không tìm thấy dữ liệu trong Context
        - Mandatory: Yes

    10. Order Confirmation:
        - Field name: order_confirmation
        - Description: User đồng ý xác nhận thông tin đơn hàng là đúng và đầy đủ sau khi Assistant gửi summary order cho User.
        - Default value: là "No" nếu Assistant không tìm thấy dữ liệu trong Context
        - Mandatory: Yes

    # Output
    - Assistant MUST trả lời bằng JSON format với các field như sau:
    ```    
    {json.dumps(json_output_example, ensure_ascii=False)}
    ```  

    # Constraints
    - Assistant MUST reply by JSON format ONLY như trong mục Output. No need explaination.
    - Assistant DO NOT use the example data in the Task and Output section to create JSON content. Assistant MUST looks the data in the Context, User's input to extract accurate data. If Assistant cannot extract data, leave it as default value.
        
    User's input: {user_input}
    Answer:
    """

    prompt = dedent(prompt)
        
    response = completion(
        api_key=os.environ["GROQ_API_KEY"],
        model=LLM_MODELS['make_order_subgraph']['analyze_order_node'],
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        # response_format=OrderInfoSchema
    )

    logger.info(f"Raw Order Info Response: {response.choices[0].message.content}")
    msg_content = remove_think_tag(response.choices[0].message.content)
    logger.info(f"Order Info Response: {msg_content}")

    order = parse_obj_as(OrderInfoSchema, extract_json_from_triple_backticks(msg_content))
    logger.success(f"Order Info: {order}")

    logger.info(f"Usage Tokens: {response.usage}")

    usage_tokens = state.get('usage_tokens')
    usage_tokens.input += response.usage.prompt_tokens
    usage_tokens.output += response.usage.completion_tokens
    usage_tokens.total += response.usage.total_tokens
    
    return {
        'order_info': order,
        "usage_tokens": usage_tokens
    }


def get_order_info_json_node(state: SalesAgentState):
    logger.debug(">>>get_order_info_json_node called!")
    order_info = state.get('order_info', {})
    delivery_info = state.get('delivery_info', {})

    data = order_info.model_dump()
    data['id'] = str(uuid.uuid4())
    data['shipping_fee'] = delivery_info[order_info.delivery_type]['shipping_fee']
    data['created_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data['updated_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for item in data['order_items']:
        item['id'] = str(uuid.uuid4())
        item['order_id'] = data['id']
        item['created_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        item['updated_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    order_items = data.pop('order_items')

    order_payload = {
        "order": data,
        "order_items": order_items
    }
    
    logger.success(f"Order Payload: {order_payload}")
    
    return {
        'order_payload': order_payload
    }

def get_delivery_info_node(state: SalesAgentState):
    logger.debug(">>>get_delivery_info_node called!")
    delivery_info = state.get('delivery_info', None)
    if delivery_info is None:
        url = os.getenv('AGENT_RESOURCE_DELIVERY_URL')
        response = httpx.get(url)
        json_data = response.json()
        
        return {
            'delivery_info': json_data['data']
        }


def is_continue_check_in_stock(state: SalesAgentState):
    order_info = state.get('order_info', None)

    if len(order_info.order_items) > 0:
        return 'CHECK_IN_STOCK'
    return 'NEXT'


def check_items_in_stock_node(state: SalesAgentState):
    logger.debug(">>>check_items_in_stock_node called!")
    order_info = state.get('order_info', None)

    url = os.getenv('AGENT_RESOURCE_STOCK_URL')
    payload = {
        "order_items": [{'sku': item.sku, 'ordered_qty': item.ordered_qty} for item in order_info.order_items] 
    }
    logger.info(f"Check Stock Payload: {payload}")
    
    response = httpx.post(url, json=payload)
    logger.info(f"Check Stock Result: {response}")
    json_data = response.json()
    logger.info(f"Check Stock Result Json: {json_data}")
    
    logger.info(f"Check Stock Results: {json_data['data']}")

    items_not_in_stock = []
    for item in json_data['data']:
        if item['status'] != 'IN_STOCK':
            items_not_in_stock.append(item)
        
    return {
        'items_not_in_stock': items_not_in_stock
    }

def validate_all_items_in_stock(state: SalesAgentState):
    items_not_in_stock = state.get('items_not_in_stock', {})
    logger.info(f"Items Not In Stock: {items_not_in_stock}")

    if len(items_not_in_stock) > 0:
        return 'NOT_ALL_IN_STOCK'
    else:
        return 'NEXT'

def validate_order_info(state: SalesAgentState):
    logger.debug(">>>validate_order_info called!")
    order_info = state.get('order_info', None)

    decision = 'NEXT'
    if order_info is not None:
        if order_info.customer_name == '':
            logger.debug(">>>order_info.customer_name == ''")
            decision = 'LACK'
        elif order_info.customer_address == '':
            logger.debug(">>>order_info.customer_address == ''")
            decision = 'LACK'
        elif order_info.customer_email == '' or re.match(EMAIL_REGEX, order_info.customer_email) is None:
            logger.debug(">>>order_info.customer_email == ''")
            decision = 'LACK'
        elif order_info.customer_phone == '' or re.match(VN_PHONE_REGEX, order_info.customer_phone) is None:
            logger.debug(">>>order_info.customer_phone == ''")
            decision = 'LACK'
        elif len(order_info.order_items) == 0:
            logger.debug(">>>len(order_info.order_items) == 0")
            decision = 'LACK'
        else:
            for order_item in order_info.order_items:
                if order_item.product_name == '' or order_item.sku == '' or order_item.ordered_qty == 0 or order_item.price == 0:
                    logger.debug(f">>>{order_item}")
                    decision = 'LACK'
                    break

    else:
        logger.debug(">>>order_info is None")
        decision = 'LACK'

    logger.info(f"Decision: {decision}")
    return decision


def validate_order_comfirmation(state: SalesAgentState):
    order_info = state.get('order_info', None)
    
    if order_info is not None and order_info.order_confirmation == 'Yes':
        return 'NEXT'
    return 'NOT_CONFIRMED'
    

def inform_items_not_in_stock_node(state: SalesAgentState):
    logger.debug(">>>inform_items_not_in_stock_node called!")
    items_not_in_stock = state.get('items_not_in_stock', {})
    product_chat_history = state.get('product_chat_history', '')
    
    prompt = f"""
    # Role
    {CONST_ASSISTANT_ROLE}

    # Skills
    {CONST_ASSISTANT_SKILLS}
    - Assistant có kỹ năng quản lý kho hàng.

    # Tone
    {CONST_ASSISTANT_TONE}

    # Context
    ## Stock Results
    ```   
    {items_not_in_stock}
    ```

    ## Product QnA History
    ```
    {product_chat_history}
    ```

    # Tasks
    - There is the description of stock results:
    1. sku: product SKU
    2. ordered_qty: the order quantity of the selected product.
    3. stock_qty: the current quantity in the stock of the selected product.
    4. stock_status: 
        - IN_STOCK: the quantity of product is in stock, ready for sales.
        - OUT_STOCK: the quantity of product is out.
        - NOT_ENOUGH_QUANTITY: the quantity of product is in stock, but not enough to sell.

    - Assistant MUST classify these selected products into 2 kinds: 
    1. Ready to sales: status is IN_STOCK. 
    2. Not available: status is OUT_STOCK or NOT_ENOUGH_QUANTITY

    - If the status of selected products is not "IN_STOCK", Assistant MUST suggest User again these kind of products in the Products QnA History except:
        - The ones are "OUT_STOCK" or "NOT_ENOUGH_QUANTITY"
        - The ones that User has selected.
    - If Assistant CANNOT find the alternative products, Assistant MUST NOT suggest any products.

    # Constraints
    {CONST_FORM_ADDRESS_IN_VN}
    - Assistant MUST focus on the stock's status to classify corectly.
    - MUST INCLUDE the stock_qty for the current quantity in the stock.
    - ALWAYS collect the latest information in the context above.
    - MUST Keep the answer concise and clear. Highly recommend response in bullet point format.
    - Assistant MUST use the same language as the User's language to reply.
    """

    prompt = dedent(prompt)

    response = completion(
        api_key=os.environ["GROQ_API_KEY"],
        model=LLM_MODELS['make_order_subgraph']['inform_items_not_in_stock'],
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
        'ai_reply': ai_message,
        "usage_tokens": usage_tokens
    }

def collect_order_info_node(state: SalesAgentState):
    logger.debug(">>>collect_order_info_node called!")
    user_input = state.get('human_input', '')
    order_info = state.get('order_info', None)

    delivery_info = state.get('delivery_info', {})

    delivery_default = 'NORMAL'
    delivery_list = []
    for key, delivery in delivery_info.items():
        delivery_list.append(f"-{key}: {delivery.get('description', '')}")
        if delivery.get('is_default', 'No') == 'Yes':
            delivery_default = key
        
    
    prompt = f"""
    # Role
    {CONST_ASSISTANT_ROLE}

    # Skills
    {CONST_ASSISTANT_SKILLS}

    # Tone
    {CONST_ASSISTANT_TONE}
    

    # Context
    ```   
    {order_info.model_dump_json()}
    ```

    # Tasks
    - Assistant MUST validate the json data in the Context above to ensure these fields are filled (NOT EMPTY) or VALID FORMAT:
    1. Customer Name:
        - Field name: customer_name
        - Description: Họ tên của User
        - Example: "Trần Văn Hùng", "Trâm Nguyễn", "Phong"
        - Mandatory: Yes

    2. Customer Phone:
        - Field name: customer_phone
        - Description: Số phone của User
        - Example: "0909123456"
        - Validate format: "{VN_PHONE_REGEX}"
        - Mandatory: Yes

    3. Customer Address:
        - Field name: customer_address
        - Description: Địa chỉ của User
        - Example: "123 Trần Hưng Đạo, Q1, TPHCM"
        - Mandatory: Yes

    4. Customer Email:
        - Field name: customer_email
        - Description: Email của User
        - Example: "phong@abc.com", "hoang@xyz.net"
        - Validate format: "{EMAIL_REGEX}"
        - Mandatory: Yes

    5. Product Name:
        - Field name: product_name
        - Description: Tên sản phẩm mà User muốn mua
        - Example: "Tinh dầu xông phòng oải hương nguyên chất Soapberry", "Dầu gội đầu Pantene Pro-V ngăn rụng tóc"
        - Mandatory: Yes

    6. Product SKU:
        - Field name: sku
        - Description: Mã SKU của sản phẩm mà User muốn mua
        - Example: "SUA-RUA-MT-IF-004", "SUA-TAY-MT-IF-005"
        - Mandatory: Yes

    7. Ordered Quantity:
        - Field name: ordered_qty
        - Description: Số lượng của từng sản phẩm mà User muốn mua
        - Mandatory: Yes

    8. Price:
        - Field name: price
        - Description: Giá của từng sản phẩm mà User muốn mua
        - Mandatory: Yes

    9. Delivery Type:
        - Field name: delivery_type
        - Description: Phương thức giao hàng là một trong 3 phương thức sau:
            {delivery_info}
        - Mandatory: Yes
    
    - If the data fields are not full filled or INVALID FORMAT, Assistant MUST ask User again the MISSING data to collect the RIGHT information to complete the process.
    - Assistant will need to ask User a series of questions to collect needed information. So, Assistant MUST ask them smartly. Highly recommend list in bullet point format.
    - If Email or Phone number is invalid, so as not to confuse the User, Assistant MUST ONLY give the example to User, DO NOT show the regex format in the response.
    - Assistant MUST ALWAYS suggest/ask to the User to chose the delivery type with some information: delivery_type, description, shipping_fee, is_default. Highly recommend delivery type list in bullet point format. Nếu User không đề cập gì đến phương thức giao hàng, Assistant MUST dùng phương thức mặc định và không hỏi thêm gì nữa về phương thức giao hàng. 
    - Assistant MUST remember valid information and DO NOT ask those information again.

    # Constraints
    {CONST_FORM_ADDRESS_IN_VN}
    - Assistant MUST keep the answer concise and clear.
    - Assistant MUST use the same language as the User's language to reply.

    User's input: {user_input}
    Answer:
    """

    prompt = dedent(prompt)

    response = completion(
        api_key=os.environ["GROQ_API_KEY"],
        model=LLM_MODELS['make_order_subgraph']['collect_order_info_node'],
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
        'ai_reply': ai_message,
        'usage_tokens': usage_tokens
    }

def order_confirmation_node(state: SalesAgentState):
    logger.debug(">>>order_confirmation_node called!")
    delivery_info = state.get('delivery_info', {})
    order_info = state.get('order_info', None)

    json_order_info = order_info.model_dump()
    json_order_info['shipping_fee'] = delivery_info[order_info.delivery_type]['shipping_fee']
    
    prompt = f"""
    # Role
    {CONST_ASSISTANT_ROLE}

    # Skills
    {CONST_ASSISTANT_SKILLS}

    # Tone
    {CONST_ASSISTANT_TONE}
    
    # Context
    ```   
    {json_order_info}
    ```

    # Tasks
    - Assistant MUST require User to confirm the order summary information.
    - ONLY base on the Order Data in the Context, Assistant MUST create the summary of the order by following these steps:
        1. Tính thành tiền trên mỗi sản phẩm: sub_total = ordered_qty * price
        2. Tính Tổng tiền: total = sum of sub_total + shipping_fee
    - Đơn vị tiền tệ là VND
    - shipping_fee = 0 nghĩa là "Phí giao hàng = 0 VND"
        
    # Output
    - Assistant MUST reply the summary of the order line by line in the following format:
    ```
        ## Thông Tin Đơn Hàng
        ---
        **Tên khách hàng:** customer_name<br>
        **Số điện thoại:** customer_phone<br>
        **Email:** customer_email<br>
        **Địa chỉ:** customer_address<br>
        **Danh sách sản phẩm:**<br>
            **Tên sản phẩm:** product_name<br>
            **SKU:** sku<br>
            **Số lượng:** ordered_qty<br>
            **Đơn giá:** price<br>
            **Thành tiền:** sub_total<br>
            --------------------<br>
            **Tên sản phẩm:** product_name<br>
            **SKU:** sku<br>
            **Số lượng:** ordered_qty<br>
            **Đơn giá:** price<br>
            **Thành tiền:** sub_total<br>
            --------------------<br>
        **Phương thức giao hàng:** delivery_type<br>
        **Phí giao hàng:** shishipping_fee<br>
        **Tổng tiền:** total
    ```

    # Constraints
    {CONST_FORM_ADDRESS_IN_VN}
    - Assistant MUST keep the answer concise and clear.
    - Assistant MUST use the same language as the User's language to reply.
    - The order summary MUST be illustrated in markdown format.
    """

    prompt = dedent(prompt)

    response = completion(
        api_key=os.environ["GROQ_API_KEY"],
        model=LLM_MODELS['make_order_subgraph']['order_confirmation_node'],
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
        'ai_reply': ai_message,
        'usage_tokens': usage_tokens
    }

def upsert_order_data_node(state: SalesAgentState):
    logger.debug(">>>upsert_order_data_node called!")
    order_payload = state.get('order_payload', {})

    try:        
        # Save Order to jsonbin
        url = os.getenv('JSONBIN_URL')
        headers = {
            'Content-Type': 'application/json',
            # 'X-Master-Key': os.getenv('JSONBIN_API_KEY'),
            'X-Access-Key': os.getenv('JSONBIN_API_KEY'),
            'X-Collection-Id': os.getenv('JSONBIN_ORDERS_COLLECTION_ID')
        }

        response = httpx.post(url, headers=headers, json=order_payload)
        logger.success(f"Order saved to jsonbin.io: {response.json()}")  

    except Exception as err:
        logger.error(f"Failed to save order to jsonbin: {err}")

def upsert_google_sheet_data_node(state: SalesAgentState):
    logger.debug(">>>upsert_google_sheet_data_node called!")
    order_payload = state.get('order_payload', {})

    try:        
        # Save Order to Google Sheet
        url = os.getenv('AGENT_RESOURCE_ORDER_URL')
        headers = {
            'Content-Type': 'application/json'
        }

        response = httpx.post(url, headers=headers, json=order_payload)
        logger.success(f"Order saved to Google Sheet: {response.json()}")  
        
    except Exception as err:
        logger.error(f"Failed to save order to Google Sheet: {err}")

        

def create_order_summary_node(state: SalesAgentState):
    logger.debug(">>>create_order_summary_node called!")
    order_payload = state.get('order_payload', {})

    prompt = f"""
    # Role
    {CONST_ASSISTANT_ROLE}

    # Skills
    {CONST_ASSISTANT_SKILLS}

    # Tone
    {CONST_ASSISTANT_TONE}
    
    # Context
    ## Order Data
    ```
    {order_payload}
    ```

    # Tasks
    - ONLY base on the Order Data in the Context. Assistant MUST create the summary of the order by following these steps:
        1. Tính thành tiền trên mỗi sản phẩm: sub_total = ordered_qty * price
        2. Tính tổng tiền: total = sum of sub_total + shipping_fee
    - Đơn vị tiền tệ là VND
    - shipping_fee = 0 nghĩa là "Phí giao hàng = 0 VND"

    # Output
    - Assistant MUST reply the summary of the order line by line in the following format:
    ```
        ## Thông Tin Đơn Hàng
        ---
        **Mã đơn hàng:** order_id<br>
        **Tên khách hàng:** customer_name<br>
        **Số điện thoại:** customer_phone<br>
        **Email:** customer_email<br>
        **Địa chỉ:** customer_address<br>
        **Danh sách sản phẩm:**<br>
            **Tên sản phẩm:** product_name<br>
            **SKU:** sku<br>
            **Số lượng:** ordered_qty<br>
            **Đơn giá:** price<br>
            **Thành tiền:** sub_total<br>
            --------------------<br>
            **Tên sản phẩm:** product_name<br>
            **SKU:** sku<br>
            **Số lượng:** ordered_qty<br>
            **Đơn giá:** price<br>
            **Thành tiền:** sub_total<br>
            --------------------<br>
        **Phương thức giao hàng:** delivery_type<br>
        **Phí giao hàng:** shishipping_fee<br>
        **Tổng tiền:** total<br>
        **Thời gian tạo đơn hàng:** created_at        
    ```
    - Assistant MUST inform cho User là đơn hàng của User đã được lưu vào hệ thống thành công, đồng thời cảm ơn User đã mua hàng của bên công ty {CONST_COMPANY_NAME}.
    - Assistant MUST suggest User to call the hotline của công ty: {CONST_COMPANY_HOTLINE} nếu User cần support thêm.

    # Constraints:
    {CONST_FORM_ADDRESS_IN_VN}
    - Assistant MUST reply by ONLY using the data in the Context. AVOID create content outside the Context.
    - The order summary MUST be illustrated in markdown format.
    """

    prompt = dedent(prompt)
    # logger.info(f"Order Summary Prompt: {prompt}")

    response = completion(
        api_key=os.environ["GROQ_API_KEY"],
        model=LLM_MODELS['make_order_subgraph']['create_order_summary_node'],
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
        'ai_reply': ai_message,
        "usage_tokens": usage_tokens
    }

def update_order_chat_history_node(state: SalesAgentState):
    logger.debug(">>>update_order_chat_history_node called!")
    user_input = state.get('human_input', '')
    order_chat_history = state.get('order_chat_history', '')
    ai_reply = state.get('ai_reply', None)

    if ai_reply is not None and isinstance(ai_reply, AIMessage):
        order_chat_history += f"""User: {user_input}
        Supporter: {ai_reply.content}\n\n
        """

    return {
        "order_chat_history": order_chat_history
    }

def clear_temp_data_node(state: SalesAgentState):
    logger.debug(">>>clear_temp_data_node called!")
    return {
        "product_requirement": None,
        "order_info": None,
        "delivery_info": None,
        "product_chat_history": None,
        "order_chat_history": None,
        "order_payload": None,
        "items_not_in_stock": []
    }

def do_nothing_node(state: SalesAgentState):
    logger.debug(">>>do_nothing_node called!")
    return {}