import os
import requests
from dotenv import load_dotenv
from google import genai

load_dotenv()

# Get OpenAPI and convert to tools
def get_tools():
    openapi = requests.get("http://localhost:8001/openapi.json").json()
    tools = []
    
    for path, methods in openapi["paths"].items():
        for method, details in methods.items():
            if method == "post":
                schema_ref = details["requestBody"]["content"]["application/json"]["schema"]["$ref"]
                model_name = schema_ref.split("/")[-1]
                model_schema = openapi["components"]["schemas"][model_name]
                
                tools.append({
                    "function_declarations": [{
                        "name": path.strip("/"),
                        "description": details.get("summary", ""),
                        "parameters": {
                            "type": "object",
                            "properties": model_schema["properties"],
                            "required": model_schema.get("required", [])
                        }
                    }]
                })
    
    return tools

# Call API
def call_api(path, args):
    return requests.post(f"http://localhost:8001/{path}", json=args).json()

# Chat loop
def chat():
    client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
    tools = get_tools()
    history = []
    
    print("Chat started! (type 'quit' to exit)\n")
    
    while True:
        user_msg = input("You: ")
        if user_msg.lower() in ['quit', 'exit', 'q']:
            break
        
        history.append({"role": "user", "parts": [{"text": user_msg}]})
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=history,
            config={
                "system_instruction": "You are helpful. Use tools when needed.",
                "tools": tools
            }
        )
        
        # Handle function call
        part = response.candidates[0].content.parts[0]
        if hasattr(part, 'function_call') and part.function_call:
            func = part.function_call
            result = call_api(func.name, dict(func.args))
            
            history.append({"role": "model", "parts": [{"function_call": func}]})
            history.append({"role": "user", "parts": [{"function_response": {"name": func.name, "response": result}}]})
            
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=history,
                config={"system_instruction": "You are helpful. Use tools when needed.", "tools": tools}
            )
        
        history.append({"role": "model", "parts": [{"text": response.text}]})
        print(f"Assistant: {response.text}\n")

if __name__ == "__main__":
    try:
        requests.get("http://localhost:8001/openapi.json")
    except:
        print("Error: Start FastAPI server first (python main.py)")
        exit(1)
    
    chat()