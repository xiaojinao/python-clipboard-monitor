from PySide6.QtWidgets import (QListWidget, QMenu, QAbstractItemView)
from PySide6.QtCore import Qt, Signal
from ..core.history_item import ClipboardHistoryItem


class ClipboardListWidget(QListWidget):
    """自定义列表控件，支持一键复制功能"""
    copy_requested = Signal(str)  
    delete_requested = Signal(str) 
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setDragEnabled(False)
        self.setContextMenuPolicy(Qt.CustomContextMenu)  
        self.customContextMenuRequested.connect(self.show_context_menu)
        
    def mousePressEvent(self, event):
        """鼠标点击事件处理"""
        super().mousePressEvent(event)
        
        if event.button() == Qt.RightButton:
            item = self.itemAt(event.position().toPoint())
            if item:
                self.show_context_menu(event.globalPosition().toPoint(), item)
                    
    def show_context_menu(self, position, item=None):
        """显示上下文菜单"""
        
        if item is None:
            item = self.itemAt(self.mapFromGlobal(position))
            
        if not item:
            return
            
        menu = QMenu(self)
        
        copy_action = menu.addAction("复制内容")
        copy_action.triggered.connect(lambda: self.copy_item_content(item))
        
        delete_action = menu.addAction("删除此项")
        delete_action.triggered.connect(lambda: self.delete_item(item))
        
        menu.exec(position)
        
    def copy_item_content(self, item):
        """复制项目内容"""
        clipboard_item = item.data(Qt.UserRole)
        if clipboard_item:
            self.copy_requested.emit(clipboard_item.content)
            
    def delete_item(self, item):
        """删除项目"""
        clipboard_item = item.data(Qt.UserRole)
        if clipboard_item:
            self.delete_requested.emit(clipboard_item.id)