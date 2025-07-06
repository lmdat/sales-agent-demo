import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

APP_ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Config các LLM models sử dụng trong ứng dụng
LLM_MODELS = {
    "router": {
        "router_node": os.getenv('GROQ_LLM_MODEL_LLAMA_70B')
    },
    "greeting_subgraph": {
        "greeting_node": os.getenv('GROQ_LLM_MODEL_GEMMA2_9B')
    },
    "company_info_subgraph": {
        "company_info_node": os.getenv('GROQ_LLM_MODEL_GEMMA2_9B')
    },
    "off_topic_subgraph": {
        "off_topic_node": os.getenv('GROQ_LLM_MODEL_GEMMA2_9B')
    },
    "product_qna_subgraph": {
        "analyze_product_node": os.getenv('GROQ_LLM_MODEL_DEEPSEEK_R1'),
        "product_qna_node": os.getenv('GROQ_LLM_MODEL_GEMMA2_9B')
    },
    "make_order_subgraph": {
        "analyze_order_node": os.getenv('GROQ_LLM_MODEL_DEEPSEEK_R1'),
        "inform_items_not_in_stock": os.getenv('GROQ_LLM_MODEL_LLAMA_70B'),
        "collect_order_info_node": os.getenv('GROQ_LLM_MODEL_GEMMA2_9B'),
        "order_confirmation_node": os.getenv('GROQ_LLM_MODEL_GEMMA2_9B'),
        "create_order_summary_node": os.getenv('GROQ_LLM_MODEL_GEMMA2_9B')
    },
    "exit_subgraph": {
        "exit_node": os.getenv('GROQ_LLM_MODEL_LLAMA_70B')
    }
}