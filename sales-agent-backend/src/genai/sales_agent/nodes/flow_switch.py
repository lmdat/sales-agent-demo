from ..states.sales_agent_state import SalesAgentState
from logger import logger

TOPIC_FLOW_MAP = {
    "greeting": "greeting",
    "off_topic": "off_topic",
    "company_info": "company_info",
    "product_qna": "product_qna",
    "make_order": "make_order",
    "wanna_exit": "wanna_exit"
}

def flow_switch_node(state: SalesAgentState):
    selected_flow = TOPIC_FLOW_MAP[state['topic'].name]
    logger.info(f"Selected flow: {selected_flow}")

    return {
        "selected_flow": selected_flow
    }

def get_selected_flow(state: SalesAgentState):
    return state.get('selected_flow', TOPIC_FLOW_MAP['off_topic'])