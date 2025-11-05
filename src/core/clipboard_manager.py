import os
import json
from .history_item import ClipboardHistoryItem


class ClipboardManager:
    """剪贴板管理器"""
    def __init__(self, save_dir="clipboard_history"):
        self.history = []
        self.save_dir = save_dir
        self.ensure_save_dir()
        self.load_history()
        
    def ensure_save_dir(self):
        """确保保存目录存在"""
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
    
    def add_item(self, content):
        """添加剪贴板项"""
        item = ClipboardHistoryItem(content)
        self.history.insert(0, item) 
        self.save_item_to_file(item)
        self.save_history_index() 
        return item
    
    def delete_item(self, item_id):
        """删除指定ID的剪贴板项"""
        item_to_delete = None
        for item in self.history:
            if item.id == item_id:
                item_to_delete = item
                break
                
        if item_to_delete:
            self.history.remove(item_to_delete)
            filename = os.path.join(self.save_dir, f"clipboard_{item_id}.txt")
            if os.path.exists(filename):
                os.remove(filename)
            self.save_history_index() 
            return True
        return False
    
    def save_item_to_file(self, item):
        """保存单个项到文件"""
        filename = os.path.join(self.save_dir, f"clipboard_{item.id}.txt")
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(item.content)
    
    def load_history(self):
        """加载历史记录"""
        if not os.path.exists(self.save_dir):
            return
            
        index_file = os.path.join(self.save_dir, "history_index.json")
        if os.path.exists(index_file):
            try:
                with open(index_file, 'r', encoding='utf-8') as f:
                    index_data = json.load(f)
                    for item_data in index_data:
                        item = ClipboardHistoryItem.from_dict(item_data)
                        self.history.insert(0, item) 
            except Exception as e:
                print(f"加载历史记录失败: {e}")
    
    def get_item_by_id(self, item_id):
        """通过ID快速获取剪贴板项"""
        for item in self.history:
            if item.id == item_id:
                return item
        return None
    
    def save_history_index(self):
        """保存历史索引"""
        index_file = os.path.join(self.save_dir, "history_index.json")
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump([item.to_dict() for item in self.history], f, ensure_ascii=False, indent=2)
    
    def export_history(self, filepath):
        """导出历史记录"""
        with open(filepath, 'w', encoding='utf-8') as f:
            for i, item in enumerate(self.history):
                f.write(f"===== 剪贴板记录 {i+1} =====\n")
                f.write(f"时间: {item.timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"内容:\n{item.content}\n\n")