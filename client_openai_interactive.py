from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Mock weather function
def get_weather(location):
    """Mock function to get weather for a location"""
    # In a real implementation, this would call a weather API
    weather_data = {
        "Paris": {"temperature": 15, "condition": "Partly cloudy", "humidity": 65},
        "London": {"temperature": 12, "condition": "Rainy", "humidity": 80},
        "New York": {"temperature": 8, "condition": "Clear", "humidity": 45},
        "Tokyo": {"temperature": 18, "condition": "Sunny", "humidity": 55},
        "Sydney": {"temperature": 22, "condition": "Sunny", "humidity": 70},
        "Berlin": {"temperature": 10, "condition": "Overcast", "humidity": 75},
        "Mumbai": {"temperature": 28, "condition": "Hot and humid", "humidity": 85},
        "Toronto": {"temperature": 5, "condition": "Snowy", "humidity": 60}
    }
    
    if location in weather_data:
        data = weather_data[location]
        return f"The weather in {location} is {data['condition']} with a temperature of {data['temperature']}°C and {data['humidity']}% humidity."
    else:
        return f"Weather data not available for {location}. Available cities: {', '.join(weather_data.keys())}."

def chat_with_weather_tool(user_message):
    """Process a user message that might require weather information"""
    messages = [{"role": "user", "content": user_message}]
    
    # First API call
    reply = client.chat.completions.create(
        model="gpt-4o",
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "get_weather",
                    "description": "Return the weather for a given location",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The city name"
                            }
                        },
                        "required": ["location"]
                    }
                }
            }
        ],
        messages=messages
    )
    
    # Check if the model wants to use a tool
    if reply.choices[0].message.tool_calls:
        # Process each tool call (could be multiple)
        messages.append(reply.choices[0].message)
        
        for tool_call in reply.choices[0].message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            print(f"🔧 Calling {function_name}({function_args['location']})")
            
            if function_name == "get_weather":
                result = get_weather(function_args["location"])
                
                # Add the tool response
                messages.append({
                    "role": "tool",
                    "content": result,
                    "tool_call_id": tool_call.id
                })
        
        # Get final response
        final_reply = client.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )
        
        return final_reply.choices[0].message.content
    else:
        # No tool calls needed
        return reply.choices[0].message.content

# Interactive loop
print("Weather Chat Bot 🌤️")
print("Ask me about the weather in any city!")
print("Type 'quit' to exit.\n")

while True:
    user_input = input("You: ")
    
    if user_input.lower() in ['quit', 'exit', 'bye']:
        print("Goodbye! ☀️")
        break
    
    response = chat_with_weather_tool(user_input)
    print(f"Bot: {response}\n")