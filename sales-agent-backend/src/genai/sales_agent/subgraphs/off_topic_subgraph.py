from langgraph.graph import StateGraph, END
from ..nodes.subgraph.off_topic_nodes import off_topic_node
from ..nodes.clear_topic import clear_topic_node
from ..states.sales_agent_state import SalesAgentState

def build_off_topic_subgraph():
    graph = StateGraph(SalesAgentState)
    graph.add_node('off_topic', off_topic_node)
    graph.add_node('clear_topic', clear_topic_node)
    graph.set_entry_point('off_topic')
    graph.add_edge('off_topic', 'clear_topic')
    graph.add_edge('clear_topic', END)
    return graph.compile()
