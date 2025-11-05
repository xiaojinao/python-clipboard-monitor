# 剪贴板监听工具

[中文](#中文) | [English](#english) | [Русский](#русский)

## 中文

一个使用PySide6开发的剪贴板监听工具，可以自动保存复制的内容，并提供查看、导出和复制功能。

## 功能特点

- **自动监听剪贴板**：实时监听剪贴板内容变化
- **自动保存**：每次复制内容都会自动保存到本地文件
- **历史记录**：保存所有剪贴板历史，可随时查看
- **内容预览**：在界面中预览剪贴板内容
- **一键复制**：可将历史记录中的内容复制回剪贴板
- **导出功能**：支持将所有历史记录导出为文本文件
- **清空历史**：可清空所有历史记录和文件
- **系统托盘**：支持最小化到系统托盘，方便后台运行
- **全局热键**：支持全局热键快速调用主窗口
- **实时索引**：历史记录索引实时更新，快速检索

## 安装与运行

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行程序

```bash
python main.py
```

## 使用方法

1. **启动程序**：运行`main.py`文件
2. **复制内容**：正常复制任何文本内容，程序会自动监听并保存
3. **查看历史**：在左侧列表中可以看到所有剪贴板历史记录（按时间倒序排列）
4. **预览内容**：点击列表中的任意项，右侧会显示完整内容
5. **复制到剪贴板**：选中列表项后，点击"复制到剪贴板"按钮
6. **导出历史**：点击"导出历史"按钮，选择保存位置
7. **清空历史**：点击"清空历史"按钮，确认后删除所有记录
8. **系统托盘**：关闭窗口时程序会最小化到系统托盘，右键托盘图标可以退出程序
9. **全局热键**：使用快捷键Ctrl+空格可以快速调出主窗口

## 文件结构

```
py剪贴板/
├── main.py              # 主程序入口
├── requirements.txt     # 依赖列表
├── README.md            # 说明文档
├── resources/          # 资源文件目录（图标、样式等）
├── clipboard_history/   # 自动创建的保存目录
│   ├── history_index.json  # 历史记录索引
│   └── clipboard_*.txt     # 各个剪贴板内容文件
└── src/                # 源代码目录
    ├── core/           # 核心功能模块
    │   ├── clipboard_manager.py  # 剪贴板管理器
    │   ├── clipboard_watcher.py   # 剪贴板监控器
    │   └── history_item.py       # 历史记录项
    ├── ui/             # 用户界面模块
    │   ├── main_window.py         # 主窗口
    │   ├── list_item.py           # 列表项
    │   ├── list_widget.py         # 列表控件
    │   └── tray_icon.py           # 托盘图标
    └── utils/          # 工具模块
        └── hotkey_listener.py     # 全局热键监听器
```

## 技术实现

- **GUI框架**：PySide6
- **剪贴板监听**：使用QTimer定期检查剪贴板变化
- **多线程**：使用QThread实现剪贴板监听，避免阻塞主界面
- **文件存储**：每个剪贴板内容保存为单独文件，并维护索引文件
- **模块化设计**：采用MVC架构，代码结构清晰，易于维护和扩展
- **实时索引**：历史记录索引实时更新，支持快速检索和排序
- **系统托盘集成**：支持最小化到系统托盘，提供右键菜单

## 注意事项

- 程序会自动创建`clipboard_history`目录用于存储剪贴板内容
- 每个剪贴板内容都会保存为单独的文本文件
- 历史记录索引保存在`history_index.json`文件中，并实时更新
- 清空历史会删除所有已保存的文件，请谨慎操作
- 程序关闭后会最小化到系统托盘，可通过托盘图标右键菜单完全退出
- 使用全局热键功能需要管理员权限（在某些系统上）

---

# Clipboard Monitor Tool

A clipboard monitoring tool developed with PySide6 that automatically saves copied content and provides viewing, exporting, and copying functionality.

## Features

- **Automatic Clipboard Monitoring**: Real-time monitoring of clipboard content changes
- **Automatic Saving**: Automatically saves each copied content to local files
- **History Tracking**: Saves all clipboard history for easy access
- **Content Preview**: Preview clipboard content in the interface
- **One-Click Copy**: Copy historical content back to clipboard with one click
- **Export Function**: Export all history records as text files
- **Clear History**: Clear all history records and files
- **System Tray**: Minimize to system tray for convenient background operation
- **Global Hotkey**: Support global hotkey for quick access to main window
- **Real-time Indexing**: History index updates in real-time for fast retrieval

## Installation and Running

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Program

```bash
python main.py
```

## Usage

1. **Start Program**: Run the `main.py` file
2. **Copy Content**: Copy any text content normally, the program will automatically monitor and save it
3. **View History**: All clipboard history records can be seen in the left list (ordered by time in reverse)
4. **Preview Content**: Click any item in the list to display the complete content on the right
5. **Copy to Clipboard**: Select a list item and click the "Copy to Clipboard" button
6. **Export History**: Click the "Export History" button and select a save location
7. **Clear History**: Click the "Clear History" button and confirm to delete all records
8. **System Tray**: When closing the window, the program will minimize to the system tray; right-click the tray icon to exit
9. **Global Hotkey**: Use the shortcut Ctrl+Space to quickly bring up the main window

## File Structure

```
clipboard_monitor/
├── main.py              # Main program entry
├── requirements.txt     # Dependency list
├── README.md            # Documentation
├── resources/          # Resource files directory (icons, styles, etc.)
├── clipboard_history/   # Automatically created save directory
│   ├── history_index.json  # History record index
│   └── clipboard_*.txt     # Individual clipboard content files
└── src/                # Source code directory
    ├── core/           # Core functionality modules
    │   ├── clipboard_manager.py  # Clipboard manager
    │   ├── clipboard_watcher.py   # Clipboard monitor
    │   └── history_item.py       # History record item
    ├── ui/             # User interface modules
    │   ├── main_window.py         # Main window
    │   ├── list_item.py           # List item
    │   ├── list_widget.py         # List widget
    │   └── tray_icon.py           # Tray icon
    └── utils/          # Utility modules
        └── hotkey_listener.py     # Global hotkey listener
```

## Technical Implementation

- **GUI Framework**: PySide6
- **Clipboard Monitoring**: Uses QTimer to periodically check for clipboard changes
- **Multithreading**: Uses QThread for clipboard monitoring to avoid blocking the main interface
- **File Storage**: Each clipboard content is saved as a separate file with an index file maintained
- **Modular Design**: Adopts MVC architecture with clear code structure for easy maintenance and extension
- **Real-time Indexing**: History index updates in real-time for fast retrieval and sorting
- **System Tray Integration**: Supports minimization to system tray with right-click menu

## Notes

- The program will automatically create a `clipboard_history` directory for storing clipboard content
- Each clipboard content is saved as a separate text file
- History index is saved in `history_index.json` file and updates in real-time
- Clearing history will delete all saved files, please operate with caution
- When the program is closed, it will minimize to the system tray and can be completely exited through the tray icon's right-click menu
- Using the global hotkey feature may require administrator privileges (on some systems)

---

# Инструмент мониторинга буфера обмена

Инструмент мониторинга буфера обмена, разработанный с использованием PySide6, который автоматически сохраняет скопированное содержимое и предоставляет функции просмотра, экспорта и копирования.

## Возможности

- **Автоматический мониторинг буфера обмена**: Отслеживание изменений содержимого буфера обмена в реальном времени
- **Автоматическое сохранение**: Автоматическое сохранение каждого скопированного содержимого в локальные файлы
- **История**: Сохранение всей истории буфера обмена для легкого доступа
- **Предварительный просмотр содержимого**: Просмотр содержимого буфера обмена в интерфейсе
- **Копирование в один клик**: Копирование исторического содержимого обратно в буфер обмена одним кликом
- **Функция экспорта**: Экспорт всех записей истории в виде текстовых файлов
- **Очистка истории**: Очистка всех записей истории и файлов
- **Системный трей**: Минимизация в системный трей для удобной фоновой работы
- **Глобальная горячая клавиша**: Поддержка глобальной горячей клавиши для быстрого доступа к главному окну
- **Индексация в реальном времени**: Индекс истории обновляется в реальном времени для быстрого поиска

## Установка и запуск

### Установка зависимостей

```bash
pip install -r requirements.txt
```

### Запуск программы

```bash
python main.py
```

## Использование

1. **Запуск программы**: Запустите файл `main.py`
2. **Копирование содержимого**: Копируйте любой текстовый контент обычным способом, программа автоматически отследит и сохранит его
3. **Просмотр истории**: Вся история буфера обмена отображается в списке слева (упорядочена по времени в обратном порядке)
4. **Предварительный просмотр содержимого**: Нажмите на любой элемент в списке, чтобы отобразить полное содержимое справа
5. **Копирование в буфер обмена**: Выберите элемент списка и нажмите кнопку "Копировать в буфер обмена"
6. **Экспорт истории**: Нажмите кнопку "Экспорт истории" и выберите место сохранения
7. **Очистка истории**: Нажмите кнопку "Очистить историю" и подтвердите удаление всех записей
8. **Системный трей**: При закрытии окна программа минимизируется в системный трей; щелкните правой кнопкой мыши по значку в трее для выхода
9. **Глобальная горячая клавиша**: Используйте сочетание клавиш Ctrl+Пробел для быстрого вызова главного окна

## Структура файлов

```
clipboard_monitor/
├── main.py              # Основная точка входа в программу
├── requirements.txt     # Список зависимостей
├── README.md            # Документация
├── resources/          # Каталог файлов ресурсов (значки, стили и т.д.)
├── clipboard_history/   # Автоматически создаваемый каталог для сохранения
│   ├── history_index.json  # Индекс записей истории
│   └── clipboard_*.txt     # Отдельные файлы содержимого буфера обмена
└── src/                # Каталог исходного кода
    ├── core/           # Модули основной функциональности
    │   ├── clipboard_manager.py  # Менеджер буфера обмена
    │   ├── clipboard_watcher.py   # Монитор буфера обмена
    │   └── history_item.py       # Элемент записи истории
    ├── ui/             # Модули пользовательского интерфейса
    │   ├── main_window.py         # Главное окно
    │   ├── list_item.py           # Элемент списка
    │   ├── list_widget.py         # Виджет списка
    │   └── tray_icon.py           # Значок в трее
    └── utils/          # Вспомогательные модули
        └── hotkey_listener.py     # Слушатель глобальной горячей клавиши
```

## Техническая реализация

- **GUI фреймворк**: PySide6
- **Мониторинг буфера обмена**: Использует QTimer для периодической проверки изменений буфера обмена
- **Многопоточность**: Использует QThread для мониторинга буфера обмена, чтобы избежать блокировки основного интерфейса
- **Файловое хранилище**: Каждое содержимое буфера обмена сохраняется как отдельный файл с поддержкой индексного файла
- **Модульный дизайн**: Принята архитектура MVC с четкой структурой кода для удобства обслуживания и расширения
- **Индексация в реальном времени**: Индекс истории обновляется в реальном времени для быстрого поиска и сортировки
- **Интеграция с системным треем**: Поддерживает минимизацию в системный трей с контекстным меню

## Примечания

- Программа автоматически создаст каталог `clipboard_history` для хранения содержимого буфера обмена
- Каждое содержимое буфера обмена сохраняется как отдельный текстовый файл
- Индекс истории сохраняется в файле `history_index.json` и обновляется в реальном времени
- Очистка истории удалит все сохраненные файлы, действуйте с осторожностью
- При закрытии программы она минимизируется в системный трей и может быть полностью закрыта через контекстное меню значка в трее
- Использование функции глобальной горячей клавиши может потребовать прав администратора (на некоторых системах)