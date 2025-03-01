from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from mistralai import Mistral
from dotenv import dotenv_values

config = dotenv_values('.env')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MISTRAL_API_KEY = config["MISTRAL_API_KEY"]
LLM_MODEL = config["LLM_MODEL"]

model_instructions = """
You are an AI chatbot designed to assist journalists in drafting articles.

Your task is to generate an article in Markdown format while engaging in a conversation with the journalist in plain text format.

Your responses must always be structured in the following format:

Your response to the journalist in raw text format.
---
Your generated article in Markdown format.

No text, no notes and no explanations after the article.
"""

client = Mistral(api_key=MISTRAL_API_KEY)

def chat_streaming(user_prompt: str):
    messages = [
        {
            "role": "system",
            "content": model_instructions,
        },
        {
            "role": "user",
            "content": user_prompt,
        }
    ]

    # either one of the following
    # return with_sync_streaming(messages)
    return with_async_streaming(messages)

def with_sync_streaming(messages: str):
    try:
        for i, chunk in enumerate(client.chat.stream(model=LLM_MODEL, messages=messages)):
            content = chunk.data.choices[0].delta.content
            if content:
                print(f"Chunk {i}: {repr(content)}")
                escaped_content = content.replace("\n", "\\n")
                yield f"data: {escaped_content}\n\n"
            else:
                print(f"Chunk {i}: <empty content>")

        yield "event: done\ndata: \n\n"
    except Exception as e:
        print(f"Error in with_sync_streaming: {e}")
        yield f"data: Error occurred: {str(e)}\n\n"
        yield "event: done\ndata: \n\n"

async def with_async_streaming(messages: str):
    try:
        i = 0
        async for chunk in await client.chat.stream_async(model=LLM_MODEL, messages=messages):
            content = chunk.data.choices[0].delta.content
            if content:
                print(f"Chunk {i}: {repr(content)}")
                escaped_content = content.replace("\n", "\\n")
                yield f"data: {escaped_content}\n\n"
            else:
                print(f"Chunk {i}: <empty content>")
            i += 1

        yield "event: done\ndata: \n\n"
    except Exception as e:
        print(f"Error in with_async_streaming: {e}")
        yield f"data: Error occurred: {str(e)}\n\n"
        yield "event: done\ndata: \n\n"

@app.get("/ai")
async def chat(prompt: str):
    print(f"GET /ai?prompt={prompt}")

    return StreamingResponse(
        chat_streaming(user_prompt=prompt),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "http://localhost:3000",
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
