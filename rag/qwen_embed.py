import dashscope
from http import HTTPStatus

from typing import List, Union

class QwenEmbedding:
    def __init__(self, api_key: str):
        dashscope.api_key = api_key
    
    def get_embedding(self, 
                     text: Union[str, List[str]], 
                     model: str = "text-embedding-v4") -> List[float]:
        resp = dashscope.TextEmbedding.call(
            model=model,
            input=text,
            dimension=1024,  # 指定向量维度（仅 text-embedding-v3及 text-embedding-v4支持该参数）
            output_type="dense&sparse"
        )

        if resp.status_code == HTTPStatus.OK:
            return resp.output["embeddings"]
        else:
            return None
        
    def get_single_embedding(self, text: str) -> List[float]:
        """获取单条文本的嵌入向量"""
        result = self.get_embedding(text)
        if result:
            return result[0]["embedding"]
        return []
    