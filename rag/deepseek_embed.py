import requests
from typing import List, Union

class DeepSeekEmbedding:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.deepseek.com/v1/embeddings"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def get_embedding(self, 
                     text: Union[str, List[str]], 
                     model: str = "deepseek-embedder") -> List[dict]:
        """
        获取文本嵌入向量
        
        Args:
            text: 单条文本或文本列表
            model: 使用的模型名称
            
        Returns:
            List[dict]: 包含嵌入向量的字典列表
        """
        if isinstance(text, str):
            text = [text]
        
        payload = {
            "model": model,
            "input": text,
            "encoding_format": "float"
        }
        
        try:
            response = requests.post(
                self.base_url, 
                headers=self.headers, 
                json=payload, 
                timeout=30
            )
            response.raise_for_status()
            return response.json()["data"]
            
        except requests.exceptions.RequestException as e:
            print(f"API调用错误: {e}")
            return []
    
    def get_single_embedding(self, text: str) -> List[float]:
        """获取单条文本的嵌入向量"""
        result = self.get_embedding(text)
        if result:
            return result[0]["embedding"]
        return []
    
    def batch_embedding(self, 
                       texts: List[str], 
                       batch_size: int = 32,
                       model: str = "deepseek-embedder") -> List[List[float]]:
        """批量处理文本嵌入"""
        all_embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            print(f"处理批次 {i//batch_size + 1}/{(len(texts)-1)//batch_size + 1}")
            
            batch_results = self.get_embedding(batch, model)
            batch_embeddings = [item["embedding"] for item in batch_results]
            all_embeddings.extend(batch_embeddings)
        
        return all_embeddings
