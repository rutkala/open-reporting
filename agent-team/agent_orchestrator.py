from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
from litellm import completion
from dotenv import load_dotenv

# Load API keys
load_dotenv()


# Define the State
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    next_step: str

# Role definitions & priorities
AGENT_ROLES = {
    "orchestrator": ["groq/llama-3.3-70b-versatile"],
    "data_engineer": ["groq/llama-3.1-8b-instant"],
    "analytics_lead": ["gemini/gemini-1.5-flash"],
    "presenter": ["groq/llama-3.1-8b-instant"]
}

def estimate_complexity(prompt: str) -> str:
    """Uses a fast model to classify task complexity."""
    try:
        classifier_model = "groq/llama-3.1-8b-instant"
        prompt_with_instr = f"Classify the complexity of this task as 'low', 'medium', or 'high' based on required reasoning. Output only the word. Task: {prompt}"
        response = completion(model=classifier_model, messages=[{"role": "user", "content": prompt_with_instr}])
        return response.choices[0].message.content.strip().lower()
    except:
        return "medium"

def call_model(role: str, messages: list):
    # Normalize and find latest content
    latest_content = ""
    for msg in reversed(messages):
        if isinstance(msg, dict):
            if msg.get("role") == "user":
                latest_content = msg.get("content", "")
                break
        else:
            if getattr(msg, "type", "") == "human":
                latest_content = msg.content
                break
    
    complexity = estimate_complexity(latest_content) if latest_content else "medium"
    
    # Model selection based on complexity
    if complexity == "high":
        model = "groq/llama-3.3-70b-versatile"
    elif complexity == "medium":
        model = "groq/llama-3.1-8b-instant"
    else:
        model = "groq/llama-3.1-8b-instant"
    
    cleaned_messages = []
    for msg in messages:
        if isinstance(msg, dict):
            cleaned_messages.append({"role": msg.get("role", "user"), "content": msg.get("content", "")})
        else:
            role_type = "user" if getattr(msg, "type", "") == "human" else "assistant"
            cleaned_messages.append({"role": role_type, "content": msg.content})
    
    cleaned_messages = [m for m in cleaned_messages if m["content"]]
    
    try:
        print(f"[{role.upper()} | Complexity: {complexity}] Calling {model}...")
        response = completion(model=model, messages=cleaned_messages)
        return response.choices[0].message.content
    except Exception as e:
        print(f"Model {model} failed: {e}")
        return "Task processing failed."


# Define Nodes
def orchestrator_node(state: AgentState):
    print("Orchestrator active: Planning...")
    # This node will eventually route tasks dynamically
    return {"next_step": "data_engineer"}

def data_engineer_node(state: AgentState):
    print("Data Engineer active: Building pipelines...")
    response = call_model("data_engineer", state["messages"])
    return {"messages": [{"role": "assistant", "content": f"[Data Engineer]: {response}"}]}

def analytics_lead_node(state: AgentState):
    print("Analytics Lead active: Analyzing metrics...")
    response = call_model("analytics_lead", state["messages"])
    return {"messages": [{"role": "assistant", "content": f"[Analytics Lead]: {response}"}]}

def presenter_node(state: AgentState):
    print("Presenter active: Creating UI/Content...")
    response = call_model("presenter", state["messages"])
    return {"messages": [{"role": "assistant", "content": f"[Presenter]: {response}"}]}

# Build Graph
workflow = StateGraph(AgentState)
workflow.add_node("orchestrator", orchestrator_node)
workflow.add_node("data_engineer", data_engineer_node)
workflow.add_node("analytics_lead", analytics_lead_node)
workflow.add_node("presenter", presenter_node)

workflow.set_entry_point("orchestrator")
workflow.add_edge("orchestrator", "data_engineer")
workflow.add_edge("data_engineer", "analytics_lead")
workflow.add_edge("analytics_lead", "presenter")
workflow.add_edge("presenter", END)

# Initialize Checkpointer for state persistence
checkpointer = SqliteSaver.from_conn_string("checkpoints.sqlite")
# Wait, let's try direct instantiation if needed:
# checkpointer = SqliteSaver("checkpoints.sqlite") 
# But from_conn_string is often the recommended way. 
# Let's see if there's a non-context-manager way.
# Try this instead:
with SqliteSaver.from_conn_string("checkpoints.sqlite") as checkpointer:
    app = workflow.compile(checkpointer=checkpointer)
    
    # Example execution
    if __name__ == "__main__":
        initial_state = {"messages": [{"role": "user", "content": "Analyze the current state of the Polish labour market."}]}
        config = {"configurable": {"thread_id": "session_001"}}
        result = app.invoke(initial_state, config=config)
        print("Final result:", result["messages"][-1].content)
