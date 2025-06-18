from langgraph.graph import StateGraph, END
from ..nodes.subgraph.exit_nodes import wanna_exit_node
from ..nodes.clear_topic import clear_topic_node
from ..states.sales_agent_state import SalesAgentState

def build_exit_subgraph():
    graph = StateGraph(SalesAgentState)
    graph.add_node('wanna_exit', wanna_exit_node)
    graph.add_node('clear_topic', clear_topic_node)
    graph.set_entry_point('wanna_exit')
    graph.add_edge('wanna_exit', 'clear_topic')
    graph.add_edge('clear_topic', END)
    return graph.compile()