from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

import src.with_mistral as with_mistral

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


model_instructions = """
You are an AI chatbot designed to assist journalists in drafting articles.

Your task is to generate an article in Markdown format while engaging in a conversation with the journalist in plain text format.

Answer in JSON format with the following fields:
- message: The response to the journalist in plain text format.
- title: The title of the article in plain text format.
- article: The generated article in Markdown format.
"""


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
    # return with_mistral.with_sync_streaming(messages)
    return with_mistral.with_async_streaming(messages)

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
    # uvicorn src.main:app --reload
