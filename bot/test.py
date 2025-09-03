from bot.LLMConversationValidator import LLMConversationValidator


#Define Schema

schema  = {
    "type": "object",
    "properties": {
        "tool_name": {"type": "string"},
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string"},
                "units": {"type": "string", "enum": ["metric", "imperial"]}
            },
            "required": ["city", "units"]
        }
    },
    "required": ["tool_name", "parameters"]
}

validator = LLMConversationValidator(schema)
"""
print("--- Scenario 1: InValid Conversation ---")


#Data to be validated
                                                               
data = {
  

      "tool_name": "get_weather",
      "parameters": {
        "city": "Berlin",
        "units": "metric"
      }
    
  ,
  "assistant_reply": "The temperature in Berlin is 20°C.",
  "tool_output": "Berlin: 20°C"
}


result = validator.validate_schema(data)

print(result)
"""
print("--- Scenario 2: InValid Conversation ---")

data = {
  

      "tool_name": "get_weather",
      "parameters": {
        "city": "Berlin",
        "units": "metric"
      }
    
  ,
  "assistant_reply": "The temperature in Berlin is 20°C.",
  "tool_output": "Berlin: 20°C"
}


data_example_1 = {
    "tool_name": "get_stock_price",
    "parameters": {
        "symbol": "AAPL"
    },
    "assistant_reply": "Apple's stock is currently at 175 USD.",
    "tool_output": "AAPL: 175 USD"
}

data_example_2 = {
    "tool_name": "get_weather",
    "parameters": {
        "city": "New York",
        "units": "metric"
    },
    "assistant_reply": "The temperature in New York is 28°C with clear skies.",
    "tool_output": "New York: 28°C"
}

data_example_3 = {
    "tool_name": "calculate_sum",
    "parameters": {
        "numbers": [5, 10, 20]
    },
    "assistant_reply": "The total sum of the numbers is 35.",
    "tool_output": "35"
}
question = f"What is the temperature in Berlin?"
context = context = f"""
Question: {question}
Tool: {data['tool_name']}
Parameters: {data['parameters']}
Tool Output: {data['tool_output']}
Explanation: The tool provides the temperature in Berlin in Celsius.
"""
value = validator.is_grounded(
    reply=data_example_1["assistant_reply"],
    tool_output=data_example_1["tool_output"]
)
print(value)