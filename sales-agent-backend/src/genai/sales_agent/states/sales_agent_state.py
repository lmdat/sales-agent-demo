from typing import TypedDict, Annotated
from langgraph.graph.message import AnyMessage, add_messages
from langchain_core.messages import AIMessage
from ..schemas.topic import TopicSchema
from ..schemas.usage_tokens import UsageTokensSchema
from ..schemas.product_requirement import ProductRequirementSchema
from ..schemas.order import OrderInfoSchema

class SalesAgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages] = None
    # reduced_messages: Annotated[list[AnyMessage], add_messages] = None
    human_input: str = ""
    ai_reply: AIMessage = None
    usage_tokens: UsageTokensSchema = None
    topic: TopicSchema = None
    selected_flow: str = None
    product_chat_history: str = None
    order_chat_history: str = None
    product_requirement: ProductRequirementSchema = None
    order_info: OrderInfoSchema = None 
    delivery_info: dict = None
    order_payload: dict = None
    items_not_in_stock: list = []
