import asyncio
from .chunk import get_chunks
import chromadb
import os
from dotenv import load_dotenv
from .qwen_embed import QwenEmbedding
from openai import OpenAI, AsyncOpenAI

LLM_MODEL = "deepseek-chat"

class DeepSeekRag:
    def __init__(self):
        load_dotenv()
        self.deepseek_client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")
        self.async_deepseek_client = AsyncOpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")
        self.chromadb_client = chromadb.PersistentClient("./chroma.db")
        self.chromadb_collection = self.chromadb_client.get_or_create_collection("lhc")
        self.qwen_embed = QwenEmbedding(os.getenv("DASHSCOPE_API_KEY"))
        if self.chromadb_collection.count() == 0:
            self.init_db()
    
    def embed(self, text: str) -> list[float]:
        print(f"embed: {text}")
        return self.qwen_embed.get_single_embedding(text)

    def init_db(self) -> None:
        for idx, c in enumerate(get_chunks()):
            print(f"Process: {c}")
            embeding = self.embed(c)
            self.chromadb_collection.upsert(ids=str(idx), documents=c,embeddings=embeding)

    def query_db(self, question: str) -> list[str]:
        question_embedding = self.embed(question)
        result = self.chromadb_collection.query(
            query_embeddings=question_embedding,
            n_results=5
        )
        assert result["documents"]
        return result["documents"][0]
    
    def call(self, question: str):
        chunks = self.query_db(question)
        prompt = "Please answer user's question according to context\n"
        prompt += f"Question: {question}\n"
        prompt += "Context:\n"
        for c in chunks:
            prompt += f"{c}\n"
            prompt += "-------------\n"
        
        response = self.deepseek_client.chat.completions.create(
            model=LLM_MODEL, 
            messages=
            [
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": prompt},
            ],
            stream=False
        )

        return response.choices[0].message.content
    
    async def stream_call(self, question: str):
        chunks = self.query_db(question)
        prompt = "Please answer user's question according to context\n"
        prompt += f"Question: {question}\n"
        prompt += "Context:\n"
        for c in chunks:
            prompt += f"{c}\n"
            prompt += "-------------\n"
        
        stream = await self.async_deepseek_client.chat.completions.create(
            model=LLM_MODEL, 
            messages=
            [
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": prompt},
            ],
            stream=True
        )

        async for event in stream:
            yield event.choices[0].delta.content

async def main():
    question = "令狐冲领悟了什么魔法？"
    rag = DeepSeekRag()
    async for msg in rag.stream_call(question=question):
        print(msg, end="", flush=True)

if __name__ == '__main__':
    asyncio.run(main())