from langchain_core.messages import AIMessage, HumanMessage
import re
import json

def parsing_messages_to_history(messages):
    if isinstance(messages, str) and messages == '':
        return ''    

    history = []
    for message in messages:
        if isinstance(message, HumanMessage):
            history.append(f"UserMessage: {message.content} | Time: {message.additional_kwargs['current_time']}\n")
        elif isinstance(message, AIMessage):
            history.append(f"AIMessage: {message.content} | Time: {message.additional_kwargs['current_time']}\n\n")    
    
    return "".join(history)

def remove_think_tag(content: str):
  pattern = r"<think>(.|\s)*?<\/think>"
  return re.sub(pattern, "", content).strip()

def extract_json_from_triple_backticks(content: str):
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass

    pattern = r"```(?:json)?\s*([\s\S]*?)```"
    match = re.search(pattern, content)
    if match:
        return json.loads(match.group(1).strip())
    return None

def extract_vectordb_results(results: dict, limit_score: float = 0.2):
    search_content_results = []
    
    for item in results['result']['hits']:
        if isinstance(limit_score, float) and item['_score'] < limit_score:
            continue
        search_content_results.append(item['fields']['chunk_content'])
    
    if len(search_content_results) > 0:
        return "\n\n".join(search_content_results)
    
    return ""
