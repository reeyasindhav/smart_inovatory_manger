from langgraph.graph import StateGraph, END
from app.services.chatbot.state import ChatState
from app.services.chatbot.intents import classify_intent

from app.services.chatbot.nodes.greet import greet_node
from app.services.chatbot.nodes.inventory_qna import inventory_qna_node
from app.services.chatbot.nodes.analytics import inventory_insights_node
from app.services.chatbot.nodes.purchase import (
    purchase_node,
    purchase_overview_node,
    purchase_recommendation_node,
    sales_overview_node,
    profit_node,
)
from app.services.chatbot.nodes.confirmation import confirmation_node
from app.services.chatbot.nodes.semantic import semantic_node
from app.services.chatbot.nodes.assistant import assistant_node

def build_chat_graph():
    print("called build_chat_graph")
    graph = StateGraph(ChatState)

    # 🔹 Nodes
    graph.add_node("classify_intent", classify_intent)
    graph.add_node("greet", greet_node)
    graph.add_node("inventory_qna", inventory_qna_node)
    graph.add_node("inventory_insights", inventory_insights_node)
    graph.add_node("purchase_overview", purchase_overview_node)
    graph.add_node("sales_overview", sales_overview_node)
    graph.add_node("profit", profit_node)
    graph.add_node("purchase", purchase_node)
    graph.add_node("confirmation", confirmation_node)
    graph.add_node("semantic", semantic_node)
    graph.add_node("purchase_recommendation", purchase_recommendation_node)

    graph.add_node("assistant", assistant_node)
    graph.set_entry_point("classify_intent")
    print("Added nodes to graph")

    graph.add_conditional_edges(
        "classify_intent",
        lambda s: s["intent"],
        {
            "GREETING": "greet",
            "CONFIRMATION_YES": "confirmation",
            "CONFIRMATION_NO": "confirmation",
            "SEMANTIC": "semantic",   # 🔥 everything else
        }
    )
    print("Added classify_intent edges")

    # 🔥 Semantic routing — ONE source of truth
    graph.add_conditional_edges(
        "semantic",
        lambda s: s["intent"],
        {
            "INVENTORY_STATUS": "inventory_qna",
            "INVENTORY_RISK": "inventory_insights",
            "SALES_OVERVIEW": "sales_overview",
            "PROFIT_ANALYSIS": "profit",
            "PURCHASE_OVERVIEW": "purchase_overview",
            "PURCHASE_RECOMMENDATION": "purchase_recommendation",
            "PURCHASE_CREATE": "purchase",
            "FORECAST": "inventory_insights",
            "WHAT_IF_SIMULATION": "inventory_insights",
            "EXPLANATION": "inventory_insights",
        }
    )

    print("Added semantic edges")

    graph.add_edge("inventory_qna", "assistant")
    graph.add_edge("inventory_insights", "assistant")
    graph.add_edge("sales_overview", "assistant")
    graph.add_edge("purchase_overview", "assistant")
    graph.add_edge("profit", "assistant")
    graph.add_edge("purchase_recommendation", "assistant")
    graph.add_edge("greet", "assistant")
    graph.add_edge("assistant", END)


    return graph.compile()
