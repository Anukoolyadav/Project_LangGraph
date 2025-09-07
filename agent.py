from typing import Literal, List, Any
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict, Annotated
from langgraph.graph import START, StateGraph, END
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from prompt_library.prompt import system_prompt
from utils.llms import LLMModel
from toolkit.toolkits import *

class Router(TypedDict):
    next: Literal["information_node", "booking_node", "FINISH"]

class AgentState(TypedDict):
    messages: Annotated[list[Any], add_messages]
    id_number: int

def get_last_user_message(messages: List[BaseMessage]) -> BaseMessage:
    for m in reversed(messages):
        if isinstance(m, HumanMessage):
            return m
    return HumanMessage(content="")

class DoctorAppointmentAgent:
    def __init__(self):
        llm_model = LLMModel()
        self.llm_model = llm_model.get_model()

    def supervisor_node(self, state: AgentState) -> dict:
        print("---SUPERVISOR---")
        full_prompt = [HumanMessage(content=system_prompt)] + state["messages"]
        response = self.llm_model.with_structured_output(Router).invoke(full_prompt)
        return {"next": response.get("next")}

    def information_node(self, state: AgentState) -> dict:
        print("---INFORMATION NODE---")
        information_agent = create_react_agent(
            model=self.llm_model,
            tools=[check_availability_by_doctor],
        )
        last_user_message = get_last_user_message(state["messages"])
        result = information_agent.invoke({"messages": [last_user_message]})
        return {"messages": [AIMessage(content=result["messages"][-1].content, name="information_node")]}

    def booking_node(self, state: AgentState) -> dict:
        print("---BOOKING NODE---")
        booking_agent = create_react_agent(
            model=self.llm_model,
            tools=[set_appointment, cancel_appointment],
        )
        last_user_message = get_last_user_message(state["messages"])
        result = booking_agent.invoke({"messages": [last_user_message]})
        return {"messages": [AIMessage(content=result["messages"][-1].content, name="booking_node")]}

    def workflow(self):
        graph = StateGraph(AgentState)
        graph.add_node("supervisor", self.supervisor_node)
        graph.add_node("information_node", self.information_node)
        graph.add_node("booking_node", self.booking_node)

        graph.add_edge(START, "supervisor")
        graph.add_conditional_edges(
            "supervisor",
            lambda x: x.get("next"),
            {
                "information_node": "information_node",
                "booking_node": "booking_node",
                "FINISH": END,
            },
        )
        graph.add_edge("information_node", "supervisor")
        graph.add_edge("booking_node", "supervisor")

        return graph.compile()
