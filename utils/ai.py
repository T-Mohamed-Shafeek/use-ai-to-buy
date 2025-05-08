import os
import groq

def groq_chat_completion(messages):
    """Send messages to Groq API and return the response."""
    client = groq.Groq(api_key=os.getenv("GROQ_API_KEY"))
    response = client.chat.completions.create(
        messages=messages,
        model="llama-3.3-70b-versatile",
        temperature=0.7,
        max_tokens=1024,
        top_p=1,
        stream=False
    )
    return response.choices[0].message.content 