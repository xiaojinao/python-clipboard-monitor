from datetime import datetime
import os
import json


class ClipboardHistoryItem:
    """剪贴板历史项"""
    def __init__(self, content, timestamp=None):
        self.content = content
        self.timestamp = timestamp or datetime.now()
        self.id = self.timestamp.strftime("%Y%m%d%H%M%S%f")
        
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'content': self.content,
            'timestamp': self.timestamp.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data):
        """从字典创建对象"""
        item = cls(data['content'], datetime.fromisoformat(data['timestamp']))
        item.id = data['id']
        return item