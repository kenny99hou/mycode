from openai import OpenAI

# You need to set your API key first
# Option 1: Set environment variable OPENAI_API_KEY
# Option 2: Pass it directly: client = OpenAI(api_key="your-key-here")

client = OpenAI(api_key="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")

try:
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Use accessible model
        messages=[
            {"role": "user", "content": "write a haiku about ai"}
        ]
    )
    
    # Print the response
    print(completion.choices[0].message.content)
    
except Exception as e:
    print(f"Error: {e}")
    print("Make sure you have set your OpenAI API key")