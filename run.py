import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from agent.agent import Item, DeepSeekAgent
from rag.rag import DeepSeekRag

agent = DeepSeekAgent()
rag = DeepSeekRag()
history = []

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # 允许的前端来源
    allow_credentials=True,          # 允许携带凭证（cookies）
    allow_methods=["*"],             # 允许所有 HTTP 方法（包括 OPTIONS）
    allow_headers=["*"],             # 允许所有头
)

@app.post("/chat")
def chat(item: Item):
    global history
    response = agent.run_sync(item.question, history=history)
    history = list(response.all_messages())
    return {"answer": response.response.text}

@app.post("/chat-rag")
def chat_rag(item: Item):
    response = rag.call(item.question)
    return {"answer": response}

def format_sse(data: str):
    return f"data: {data}\n\n"

@app.get("/chat-stream")
async def chat_stream(q: str):
    async def event_generator():
        async for msg in rag.stream_call(question=q):
            # 只输出 refined（优化后的）文本 token
            yield format_sse(msg)
        # 结束标记
        yield format_sse("[DONE]")

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
    )

if __name__ == "__main__":
    uvicorn.run("run:app", host="0.0.0.0", port=8000, workers=1, reload=True)