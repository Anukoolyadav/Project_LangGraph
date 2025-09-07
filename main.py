from fastapi import FastAPI
from pydantic import BaseModel
from agent import DoctorAppointmentAgent
from langchain_core.messages import HumanMessage, AIMessage
from typing import List, Dict, Any

app = FastAPI()

class UserQuery(BaseModel):
    id_number: int
    messages: str
    conversation_history: List[Dict[str, Any]] = []

class AgentSingleton:
    def __init__(self):
        self.agent_instance = DoctorAppointmentAgent()
        self.app_graph = self.agent_instance.workflow()

singleton = AgentSingleton()

@app.post("/execute")
def execute_agent(user_input: UserQuery):
    history = []
    for msg in user_input.conversation_history:
        if msg.get("role") == "user":
            history.append(HumanMessage(content=msg.get("content")))
        elif msg.get("role") == "assistant":
            history.append(AIMessage(content=msg.get("content")))

    history.append(HumanMessage(content=user_input.messages))
    
    query_data = {
        "messages": history,
        "id_number": user_input.id_number,
    }

    response = singleton.app_graph.invoke(query_data, config={"recursion_limit": 25})
    
    # Convert response messages to a JSON-serializable format
    serializable_messages = []
    for msg in response["messages"]:
        serializable_messages.append({
            "type": msg.type,
            "content": msg.content
        })

    return {"messages": serializable_messages}
