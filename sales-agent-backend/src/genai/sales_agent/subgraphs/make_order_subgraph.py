from langgraph.graph import StateGraph, END
from ..nodes.subgraph.make_order_nodes import (
    get_delivery_info_node,
    analyze_order_requirement_node,
    validate_order_info,
    update_order_chat_history_node,
    collect_order_info_node,
    get_order_info_json_node,
    upsert_order_data_node,
    upsert_google_sheet_data_node,
    create_order_summary_node,
    check_product_chat_history_node,
    is_continue_check_in_stock,
    check_items_in_stock_node,
    validate_all_items_in_stock,
    inform_items_not_in_stock_node,
    do_nothing_node,
    validate_order_comfirmation,
    order_confirmation_node,
    clear_temp_data_node
    

)
from ..nodes.clear_topic import clear_topic_node
from ..states.sales_agent_state import SalesAgentState

def build_make_order_subgraph():
    graph = StateGraph(SalesAgentState)
    graph.add_node('check_product_chat_history', check_product_chat_history_node)
    graph.add_node('get_delivery_info', get_delivery_info_node)
    graph.add_node('analyze_order_requirement', analyze_order_requirement_node)
    
    graph.add_node('check_items_in_stock', check_items_in_stock_node)
    graph.add_node('inform_items_not_in_stock', inform_items_not_in_stock_node)
    graph.add_node('do_nothing_before_validate_order_info', do_nothing_node)
    graph.add_node('do_nothing_before_validate_order_confirmation', do_nothing_node)
    graph.add_node('order_confirmation', order_confirmation_node)
        
    graph.add_node('collect_order_info', collect_order_info_node)
    graph.add_node('get_order_info_json', get_order_info_json_node)
    graph.add_node('upsert_order_data', upsert_order_data_node)
    graph.add_node('upsert_google_sheet_data', upsert_google_sheet_data_node)
    graph.add_node('create_order_summary', create_order_summary_node)
    graph.add_node('clear_temp_data', clear_temp_data_node)
    graph.add_node('update_order_chat_history_after_collect', update_order_chat_history_node)
    # graph.add_node('update_order_chat_history_after_upsert', update_order_chat_history_node)
    graph.add_node('update_order_chat_history_after_inform', update_order_chat_history_node)
    graph.add_node('update_order_chat_history_after_confirm', update_order_chat_history_node)
    graph.add_node('clear_topic', clear_topic_node)
    
    graph.set_entry_point('check_product_chat_history')
    graph.add_edge('check_product_chat_history', 'get_delivery_info')
    graph.add_edge('get_delivery_info', 'analyze_order_requirement')

    graph.add_conditional_edges(
        'analyze_order_requirement',
        is_continue_check_in_stock,
        {
            'CHECK_IN_STOCK': 'check_items_in_stock',
            'NEXT': 'do_nothing_before_validate_order_info'
        }
    )

    graph.add_conditional_edges(
        'check_items_in_stock',
        validate_all_items_in_stock,
        {
            'NOT_ALL_IN_STOCK': 'inform_items_not_in_stock',
            'NEXT': 'do_nothing_before_validate_order_info'
        }
    )

    graph.add_conditional_edges(
        'do_nothing_before_validate_order_info',
        validate_order_info,
        {
            'LACK': 'collect_order_info',
            'NEXT': 'do_nothing_before_validate_order_confirmation'
        }
    )

    graph.add_conditional_edges(
        'do_nothing_before_validate_order_confirmation',
        validate_order_comfirmation,
        {
            'NOT_CONFIRMED': 'order_confirmation',
            'NEXT': 'get_order_info_json'
        }
    )
    
    graph.add_edge('get_order_info_json', 'upsert_order_data')
    graph.add_edge('upsert_order_data', 'upsert_google_sheet_data')
    graph.add_edge('upsert_google_sheet_data', 'create_order_summary')
    graph.add_edge('create_order_summary', 'clear_temp_data')
    graph.add_edge('clear_temp_data', 'clear_topic')
    graph.add_edge('clear_topic', END)

    graph.add_edge('collect_order_info', 'update_order_chat_history_after_collect')
    graph.add_edge('update_order_chat_history_after_collect', END)

    graph.add_edge('inform_items_not_in_stock', 'update_order_chat_history_after_inform')
    graph.add_edge('update_order_chat_history_after_inform', END)

    graph.add_edge('order_confirmation', 'update_order_chat_history_after_confirm')
    graph.add_edge('update_order_chat_history_after_confirm', END)
    
    return graph.compile()