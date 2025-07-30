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
        "Tokyo": {"temperature": 18, "condition": "Sunny", "humidity": 55}
    }
    
    if location in weather_data:
        data = weather_data[location]
        return f"The weather in {location} is {data['condition']} with a temperature of {data['temperature']}°C and {data['humidity']}% humidity."
    else:
        return f"Weather data not available for {location}. Try Paris, London, New York, or Tokyo."

# First API call to get the tool call
messages = [
    {"role": "user", "content": "What's the weather in Paris right now?"}
]

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
    # Get the tool call
    tool_call = reply.choices[0].message.tool_calls[0]
    function_name = tool_call.function.name
    function_args = json.loads(tool_call.function.arguments)
    
    print(f"Model wants to call: {function_name} with args: {function_args}")
    
    # Execute the function
    if function_name == "get_weather":
        result = get_weather(function_args["location"])
        print(f"Function result: {result}")
        
        # Add the assistant's message with tool call to the conversation
        messages.append(reply.choices[0].message)
        
        # Add the tool response to the conversation
        messages.append({
            "role": "tool",
            "content": result,
            "tool_call_id": tool_call.id
        })
        
        # Make another API call to get the final response
        final_reply = client.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )
        
        print(f"\nFinal response: {final_reply.choices[0].message.content}")
else:
    # If no tool calls, just print the response
    print(f"Response: {reply.choices[0].message.content}")