import os
from dotenv import load_dotenv, find_dotenv
from config import APP_ROOT_PATH
from langgraph.graph import StateGraph
from .states.sales_agent_state import SalesAgentState
from .nodes.router import router_node
from .nodes.flow_switch import flow_switch_node, get_selected_flow
from .subgraphs.greeting_subgraph import build_greeting_subgraph
from .subgraphs.off_topic_subgraph import build_off_topic_subgraph
from .subgraphs.company_info_subgraph import build_company_info_subgraph
from .subgraphs.product_qna_subgraph import build_product_qna_subgraph
from .subgraphs.make_order_subgraph import build_make_order_subgraph
from .subgraphs.exit_subgraph import build_exit_subgraph

# from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
from config import APP_ROOT_PATH


load_dotenv(find_dotenv())

GRAPH_PATH_MAP = {
    'greeting': 'greeting_subgraph',
    'off_topic': 'off_topic_subgraph',
    'company_info': 'company_info_subgraph',
    'product_qna': 'product_qna_subgraph',
    'make_order': 'make_order_subgraph',
    'wanna_exit': 'wanna_exit_subgraph'
}

def build_graph():
    graph = StateGraph(SalesAgentState)
    graph.add_node('router', router_node)
    graph.add_node('flow_switch', flow_switch_node)
    graph.add_node('greeting_subgraph', build_greeting_subgraph())
    graph.add_node('off_topic_subgraph', build_off_topic_subgraph())
    graph.add_node('company_info_subgraph', build_company_info_subgraph())
    graph.add_node('product_qna_subgraph', build_product_qna_subgraph())
    graph.add_node('make_order_subgraph', build_make_order_subgraph())
    graph.add_node('wanna_exit_subgraph', build_exit_subgraph())

    graph.set_entry_point('router')
    graph.add_edge('router', 'flow_switch')
    graph.add_conditional_edges(
        'flow_switch',
        get_selected_flow,
        GRAPH_PATH_MAP   
    )

    # Use MemorySaver to save the graph to memory
    # memory = MemorySaver()

    # Use SqliteSaver to save the graph to a sqlite database
    checkpoint_db_path = os.path.join(APP_ROOT_PATH, 'sqlite', os.getenv('SALES_AGENT_CHECKPOINTS', 'sales_agent_checkpoints.db'))
    memory = SqliteSaver(sqlite3.connect(checkpoint_db_path, check_same_thread=False))

    return graph.compile(checkpointer=memory)


class SalesAgentSingleton:
    _instance = None
    def __init__(self):
        self.graph = build_graph()

    def __new__(cls, *args, **kwargs):
        if cls._instance == None:
            cls._instance = super(SalesAgentSingleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance 