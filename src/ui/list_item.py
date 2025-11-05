from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QSizePolicy
from PySide6.QtCore import Signal, Qt


class ClipboardListItem(QWidget):
    """自定义列表项，包含复制按钮"""
    copy_requested = Signal(str)  
    
    def __init__(self, clipboard_item, parent=None):
        super().__init__(parent)
        self.clipboard_item = clipboard_item
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)  
        layout.setSpacing(10)
        
        preview = clipboard_item.content[:50].replace('\n', ' ')
        if len(clipboard_item.content) > 50:
            preview += "..."
            
        display_text = f"{clipboard_item.timestamp.strftime('%m-%d %H:%M:%S')} - {preview}"
        self.content_label = QLabel(display_text)
        self.content_label.setWordWrap(True)
        self.content_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.content_label.setAlignment(Qt.AlignVCenter)  
        layout.addWidget(self.content_label)
        
        # 复制按钮
        self.copy_button = QPushButton("复制")
        self.copy_button.setFixedSize(60, 30)  
        self.copy_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 3px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
        """)
        self.copy_button.clicked.connect(self.copy_content)
        layout.addWidget(self.copy_button)
        
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
    
    def copy_content(self):
        """复制内容到剪贴板"""
        self.copy_requested.emit(self.clipboard_item.content)