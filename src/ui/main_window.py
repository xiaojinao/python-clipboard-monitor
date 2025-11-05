import sys
import os
from datetime import datetime
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                              QHBoxLayout, QTextEdit, QPushButton, 
                              QLabel, QMessageBox, QFileDialog, QListWidgetItem,
                              QCheckBox, QGroupBox, QFormLayout, QMenu)
from PySide6.QtCore import Qt, QTimer, Signal, QSize
from PySide6.QtGui import QTextCursor, QFont, QIcon, QAction, QKeySequence
from PySide6.QtWidgets import QSystemTrayIcon

from ..core.clipboard_manager import ClipboardManager
from ..core.clipboard_watcher import ClipboardMonitor
from ..utils.hotkey_listener import GlobalHotkeyListener
from .list_widget import ClipboardListWidget
from .list_item import ClipboardListItem
from .tray_icon import TrayIconManager


class ClipboardApp(QMainWindow):
    """主应用程序窗口"""
    def __init__(self):
        super().__init__()
        self.clipboard_manager = ClipboardManager()
        self.clipboard_monitor = ClipboardMonitor()
        self.clipboard_monitor.clipboard_changed.connect(self.on_clipboard_changed)
        
        self.tray_manager = TrayIconManager(self)
        self.minimize_to_tray = True
        
        self.global_hotkey_listener = GlobalHotkeyListener(self)
        self.global_hotkey_listener.hotkey_pressed.connect(self.toggle_window_visibility)
        
        self.init_ui()
        self.init_tray()
        self.init_shortcuts()  
        self.update_history_list()
        
        self.clipboard_monitor.start()
        
        self.global_hotkey_listener.start()
        
    def init_tray(self):
        """初始化系统托盘"""
        if not self.tray_manager.setup_tray(self):
            self.minimize_to_tray = False
            
    def init_shortcuts(self):
        """初始化快捷键"""
        # 创建Ctrl+空格快捷键，用于显示/隐藏主窗口
        # self.shortcut = QAction(self)
        # self.shortcut.setShortcut(QKeySequence("Ctrl+Space"))
        # self.shortcut.triggered.connect(self.toggle_window_visibility)
        # self.addAction(self.shortcut)
        
    def toggle_window_visibility(self):
        """切换窗口显示/隐藏状态"""
        if self.isVisible():
            self.hide()
        else:
            self.showNormal()
            self.raise_()
            self.activateWindow()
        
    def closeEvent(self, event):
        """窗口关闭事件处理"""
        if self.minimize_to_tray and self.tray_manager.is_visible():
            event.ignore()  
            self.hide()     
            self.tray_manager.show_notification(
                "剪贴板监听工具", 
                "程序已最小化到系统托盘，双击托盘图标可恢复窗口",
                QSystemTrayIcon.Information, 2000)
        else:
            self.tray_manager.hide_tray()
                
            self.clipboard_monitor.quit()
            self.clipboard_monitor.wait()
            self.global_hotkey_listener.stop()
            
            self.clipboard_manager.save_history_index()
            
            event.accept()
            QApplication.quit()
            
    def quit_app(self):
        """完全退出应用程序"""
        self.tray_manager.hide_tray()
            
        self.clipboard_monitor.quit()
        self.clipboard_monitor.wait()
        self.global_hotkey_listener.stop()
        
        self.clipboard_manager.save_history_index()
        
        QApplication.quit()
        
    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle("剪贴板监听工具")
        self.setGeometry(100, 100, 800, 600)
        
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        
        info_label = QLabel("剪贴板内容将自动保存到本地文件")
        info_label.setStyleSheet("font-weight: bold; color: #2c3e50; padding: 5px;")
        main_layout.addWidget(info_label)
        
        settings_group = QGroupBox("设置")
        settings_layout = QFormLayout()
        
        self.minimize_checkbox = QCheckBox("关闭窗口时最小化到系统托盘")
        self.minimize_checkbox.setChecked(True)
        self.minimize_checkbox.stateChanged.connect(self.on_minimize_changed)
        settings_layout.addRow("", self.minimize_checkbox)
        
        settings_group.setLayout(settings_layout)
        main_layout.addWidget(settings_group)
        
        shortcut_label = QLabel("提示：使用 Ctrl+空格 快速显示/隐藏窗口")
        shortcut_label.setStyleSheet("color: #7f8c8d; font-style: italic; padding: 5px;")
        main_layout.addWidget(shortcut_label)
        
        middle_layout = QHBoxLayout()
        
        left_layout = QVBoxLayout()
        history_label = QLabel("剪贴板历史:")
        left_layout.addWidget(history_label)
        
        self.history_list = ClipboardListWidget()
        self.history_list.currentItemChanged.connect(self.on_history_item_clicked)
        self.history_list.copy_requested.connect(self.copy_content_to_clipboard)
        self.history_list.delete_requested.connect(self.delete_history_item)  # 连接删除信号
        left_layout.addWidget(self.history_list)
        
        tip_label = QLabel("点击列表项查看内容 | 点击复制按钮复制")
        tip_label.setStyleSheet("color: #666; font-size: 10px; padding: 5px;")
        left_layout.addWidget(tip_label)
        
        right_layout = QVBoxLayout()
        content_label = QLabel("内容预览:")
        right_layout.addWidget(content_label)
        
        self.content_display = QTextEdit()
        self.content_display.setReadOnly(True)
        self.content_display.setFont(QFont("Consolas", 10))
        right_layout.addWidget(self.content_display)
        
        middle_layout.addLayout(left_layout, 1)
        middle_layout.addLayout(right_layout, 2)
        main_layout.addLayout(middle_layout)
        
        button_layout = QHBoxLayout()
        
        self.copy_button = QPushButton("复制到剪贴板")
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        button_layout.addWidget(self.copy_button)
        
        self.export_button = QPushButton("导出历史")
        self.export_button.clicked.connect(self.export_history)
        button_layout.addWidget(self.export_button)
        
        self.clear_button = QPushButton("清空历史")
        self.clear_button.clicked.connect(self.clear_history)
        button_layout.addWidget(self.clear_button)
        
        self.exit_button = QPushButton("退出程序")
        self.exit_button.clicked.connect(self.quit_app)
        button_layout.addWidget(self.exit_button)
        
        main_layout.addLayout(button_layout)
        
        self.statusBar().showMessage("就绪")
        
        # 如果系统不支持托盘，禁用相关选项
        if not self.tray_manager.is_system_tray_available():
            self.minimize_checkbox.setEnabled(False)
            self.minimize_checkbox.setChecked(False)
            self.minimize_to_tray = False
    
    def on_minimize_changed(self, state):
        """最小化设置改变"""
        self.minimize_to_tray = (state == Qt.Checked)
    
    def on_clipboard_changed(self, content):
        """剪贴板内容变化处理"""
        item = self.clipboard_manager.add_item(content)
        self.update_history_list()
        self.statusBar().showMessage(f"已保存新的剪贴板内容: {len(content)} 字符")
        
        if not self.isVisible() and self.minimize_to_tray:
            self.tray_manager.show_notification(
                "剪贴板监听工具", 
                f"已保存新的剪贴板内容: {len(content)} 字符",
                QSystemTrayIcon.Information, 2000)
    
    def update_history_list(self):
        """更新历史列表"""
        self.history_list.clear()
        
        for item in self.clipboard_manager.history:
            list_item = QListWidgetItem()
            list_item.setData(Qt.UserRole, item)
            
            list_item_widget = ClipboardListItem(item)
            list_item_widget.copy_requested.connect(self.copy_content_to_clipboard)  # 连接复制信号
            list_item.setSizeHint(QSize(0, 60))  
            
            self.history_list.addItem(list_item)
            self.history_list.setItemWidget(list_item, list_item_widget)
    
    def on_history_item_clicked(self, current_item, previous_item):
        """历史项点击事件"""
        if current_item:
            clipboard_item = current_item.data(Qt.UserRole)
            if clipboard_item:
                self.content_display.setText(clipboard_item.content)
    
    def delete_history_item(self, item_id):
        """删除历史项"""
        item = self.clipboard_manager.get_item_by_id(item_id)
        if item and self.clipboard_manager.delete_item(item_id):
            self.update_history_list()
            self.statusBar().showMessage(f"已删除历史项: {item.content[:20]}...")
    
    def copy_content_to_clipboard(self, content):
        """复制内容到剪贴板"""
        self.clipboard_monitor.ignore_next_change = True
        
        clipboard = QApplication.clipboard()
        clipboard.setText(content)
        self.statusBar().showMessage(f"已复制内容: {len(content)} 字符")
        
        if not self.isVisible() and self.minimize_to_tray:
            self.tray_manager.show_notification(
                "剪贴板监听工具", 
                f"已复制内容: {len(content)} 字符",
                QSystemTrayIcon.Information, 2000)
    
    def copy_to_clipboard(self):
        """复制当前选中项到剪贴板"""
        current_item = self.history_list.currentItem()
        if current_item:
            clipboard_item = current_item.data(Qt.UserRole)
            if clipboard_item:
                self.copy_content_to_clipboard(clipboard_item.content)
    
    def export_history(self):
        """导出历史记录"""
        if not self.clipboard_manager.history:
            QMessageBox.information(self, "提示", "没有可导出的历史记录")
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self, "导出剪贴板历史", 
            f"clipboard_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            "文本文件 (*.txt);;所有文件 (*)")
            
        if file_path:
            try:
                self.clipboard_manager.export_history(file_path)
                self.statusBar().showMessage(f"历史记录已导出到: {file_path}")
                QMessageBox.information(self, "成功", "历史记录导出成功")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"导出失败: {str(e)}")
    
    def clear_history(self):
        """清空历史记录"""
        reply = QMessageBox.question(
            self, "确认", "确定要清空所有历史记录吗？\n这将删除所有已保存的文件。",
            QMessageBox.Yes | QMessageBox.No)
            
        if reply == QMessageBox.Yes:
            # 清空内存中的历史记录
            self.clipboard_manager.history.clear()
            
            # 删除所有历史文件
            import shutil
            if os.path.exists(self.clipboard_manager.save_dir):
                shutil.rmtree(self.clipboard_manager.save_dir)
                self.clipboard_manager.ensure_save_dir()
            
            # 更新界面
            self.update_history_list()
            self.content_display.clear()
            self.statusBar().showMessage("历史记录已清空")