from langgraph.graph import StateGraph, END
from ..nodes.subgraph.company_info_nodes import company_info_node
from ..nodes.clear_topic import clear_topic_node
from ..states.sales_agent_state import SalesAgentState

def build_company_info_subgraph():
    graph = StateGraph(SalesAgentState)
    graph.add_node('company_info', company_info_node)
    graph.add_node('clear_topic', clear_topic_node)
    graph.set_entry_point('company_info')
    graph.add_edge('company_info', 'clear_topic')
    graph.add_edge('clear_topic', END)
    return graph.compile()