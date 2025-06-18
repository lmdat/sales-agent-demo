from genai.sales_agent.agent import build_graph
from config import APP_ROOT_PATH

if __name__ == "__main__":
    graph = build_graph()
    print(graph.get_graph(xray=True).draw_mermaid(), file=open(f"{APP_ROOT_PATH}/storage/graph.mmd", "w"))