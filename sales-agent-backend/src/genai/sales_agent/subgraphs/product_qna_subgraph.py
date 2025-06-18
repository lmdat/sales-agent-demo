from langgraph.graph import StateGraph, END
from ..nodes.subgraph.product_qna_nodes import (
    analyze_product_requirement_node,
    product_qna_node,
    update_product_chat_history_node
)
from ..nodes.clear_topic import clear_topic_node
from ..states.sales_agent_state import SalesAgentState

def build_product_qna_subgraph():
    graph = StateGraph(SalesAgentState)
    graph.add_node('analyze_product_requirement', analyze_product_requirement_node)
    graph.add_node('product_qna', product_qna_node)
    graph.add_node('update_product_chat_history', update_product_chat_history_node)
    graph.add_node('clear_topic', clear_topic_node)
    
    graph.set_entry_point('analyze_product_requirement')
    graph.add_edge('analyze_product_requirement', 'product_qna')
    graph.add_edge('product_qna', 'update_product_chat_history')
    graph.add_edge('update_product_chat_history', 'clear_topic')
    graph.add_edge('clear_topic', END)
    return graph.compile()