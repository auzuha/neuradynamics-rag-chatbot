from typing import Annotated, TypedDict

from langgraph.graph import START, END, StateGraph

from langgraph.graph.message import add_messages

from langchain_openai import ChatOpenAI

from langgraph.prebuilt import ToolNode, tools_condition

from services.tools import get_rag_response, get_weather

from langchain_core.messages import HumanMessage, AIMessage

class State(TypedDict):
    messages: Annotated[list, add_messages]

class Agent:
    MESSAGE_HISTORY_LIMIT = 10

    def __init__(self):

        

        self.llm = ChatOpenAI()

        tools = [get_rag_response, get_weather]

        self.llm_with_tools = self.llm.bind_tools(tools)

        graph_builder = StateGraph(State)

        tool_node = ToolNode(tools=tools)

        graph_builder.add_node("chatbot", self.chatbot)
        graph_builder.add_node("tools", tool_node)

        graph_builder.add_conditional_edges(
            "chatbot",
            tools_condition,
        )

        graph_builder.add_edge("tools", "chatbot")
        graph_builder.add_edge(START, "chatbot")

        self.graph = graph_builder.compile()

    def chatbot(self, state: State):
        return {"messages": [self.llm_with_tools.invoke(state["messages"])]}

    
    def get_bot_response(self, message, history):
        messages = []
        if len(history) > self.MESSAGE_HISTORY_LIMIT:
            history = history[len(history) - MESSAGE_HISTORY_LIMIT:]
        for msg in history:
            if msg['role'] == 'user':
                messages.append(HumanMessage(msg['content']))
            else:
                messages.append(AIMessage(msg['content']))        
        messages.append(HumanMessage(message))
        print(len(messages))
        response = self.graph.invoke({'messages': messages})

        return response['messages'][-1].content