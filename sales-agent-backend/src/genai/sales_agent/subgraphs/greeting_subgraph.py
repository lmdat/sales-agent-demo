from langgraph.graph import StateGraph, END
from ..nodes.subgraph.greeting_nodes import greeting_node
from ..nodes.clear_topic import clear_topic_node
from ..states.sales_agent_state import SalesAgentState

def build_greeting_subgraph():
    graph = StateGraph(SalesAgentState)
    graph.add_node('greeting', greeting_node)
    graph.add_node('clear_topic', clear_topic_node)
    graph.set_entry_point('greeting')
    graph.add_edge('greeting', 'clear_topic')
    graph.add_edge('clear_topic', END)
    return graph.compile()