from dotenv import dotenv_values
from mistralai import Mistral

config = dotenv_values('.env')

MISTRAL_API_KEY = config["MISTRAL_API_KEY"]
LLM_MODEL = config["LLM_MODEL"]

client = Mistral(api_key=MISTRAL_API_KEY)

def with_sync_streaming(messages: str):
    try:
        for i, chunk in enumerate(client.chat.stream(model=LLM_MODEL, messages=messages, response_format={ "type": "json_object" })):
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
        async for chunk in await client.chat.stream_async(model=LLM_MODEL, messages=messages, response_format={ "type": "json_object" }):
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
