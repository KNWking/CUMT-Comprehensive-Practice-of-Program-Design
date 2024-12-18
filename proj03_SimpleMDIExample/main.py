import warnings
import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from tkinter import messagebox, filedialog
import os
from PyQt6.QtGui import *
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import *
from qframelesswindow import *

# 忽略底层 PyQt6 库的警告
warnings.filterwarnings("ignore", category=DeprecationWarning)
# write_icon = QIcon("./resource/write.svg")
# about_icon = QIcon("./resource/write.svg")
# BOLD_ICON = QIcon("./resource/bold-24.svg")
# ITALIC_ICON = QIcon("./resource/italic-24.svg")

style_sheet = """
    QMenuBar {
        background-color: #323232;
    }
    QMenuBar::item {
        background-color: #323232;
        color: red;
    }
    QMenuBar::item::selected {
        background-color: #1b1b1b;
    }
    QMenu {
        background-color: rgb(49, 49, 49);
        color: red;
        border: 0px solid #000;
    }
    QMenu::item::selected {
        background-color: rgb(30, 30, 30);
    }
"""



class TWidget(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFont(QFont("Microsoft YaHei UI", 16))
        self.update_theme()

    def update_theme(self):
        if isDarkTheme():
            self.setStyleSheet("QTextEdit{background-color: #000000; color: white; border: 0;}")
            default_color = QColor("white")
        else:
            self.setStyleSheet("QTextEdit{background-color: white; color: black; border: 0;}")
            default_color = QColor("black")

        # 保存当前光标位置和选择状态
        cursor = self.textCursor()
        position = cursor.position()
        anchor = cursor.anchor()

        # 更新所有现有文本的颜色
        cursor.select(QTextCursor.SelectionType.Document)
        fmt = cursor.charFormat()
        fmt.setForeground(default_color)
        cursor.mergeCharFormat(fmt)

        # 恢复光标位置和选择状态
        cursor.setPosition(anchor)
        if position != anchor:
            cursor.setPosition(position, QTextCursor.MoveMode.KeepAnchor)
        self.setTextCursor(cursor)

        # 设置默认文本格式
        fmt = self.currentCharFormat()
        fmt.setForeground(default_color)
        self.setCurrentCharFormat(fmt)


# 标签栏界面
class TabInterface(QFrame):

    def __init__(self, text: str, icon, objectName, parent=None):
        super().__init__(parent=parent)
        self.iconWidget = IconWidget(icon, self)
        self.iconWidget.setFixedSize(120, 120)

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.vBoxLayout.setSpacing(30)

        self.setObjectName(objectName)


# 带有图标和标题的标签栏
class CustomTitleBar(MSFluentTitleBar):

    def __init__(self, parent):
        super().__init__(parent)

        # 添加按钮
        self.toolButtonLayout = QHBoxLayout()
        color = QColor(206, 206, 206) if isDarkTheme() else QColor(96, 96, 96)
        self.menuButton = TransparentToolButton(FIF.MENU, self)

        # <- 按钮
        self.backButton = TransparentToolButton(FIF.UP, self)
        self.backButton.clicked.connect(parent.find_previous)

        # -> 按钮
        self.forwardButton = TransparentToolButton(FIF.DOWN, self)
        self.forwardButton.clicked.connect(parent.find_next)

        self.toolButtonLayout.setContentsMargins(20, 0, 20, 0)
        self.toolButtonLayout.setSpacing(15)
        self.toolButtonLayout.addWidget(self.menuButton)
        self.toolButtonLayout.addWidget(self.backButton)
        self.toolButtonLayout.addWidget(self.forwardButton)

        self.hBoxLayout.insertLayout(4, self.toolButtonLayout)

        # 添加标签栏
        self.tabBar = TabBar(self)

        self.tabBar.setMovable(True)
        self.tabBar.setTabMaximumWidth(220)
        self.tabBar.setTabShadowEnabled(False)
        self.tabBar.setTabSelectedBackgroundColor(QColor(255, 255, 255, 125), QColor(255, 255, 255, 50))
        self.tabBar.setScrollable(True)
        self.tabBar.setCloseButtonDisplayMode(TabCloseButtonDisplayMode.ON_HOVER)

        self.tabBar.tabCloseRequested.connect(self.tabBar.removeTab)

        self.hBoxLayout.insertWidget(5, self.tabBar, 1)
        self.hBoxLayout.setStretch(6, 0)


        self.menu = RoundMenu("目录")
        self.menu.setStyleSheet("QMenu{color : red;}")

        file_menu = RoundMenu("文件", self)

        file_menu.setIcon(FIF.FOLDER)

        copy_action = Action(FIF.COPY, "复制")
        copy_action.setShortcut("Ctrl+C")
        copy_action.triggered.connect(parent.copy_text)
        file_menu.addAction(copy_action)

        paste_action = Action(FIF.PASTE, "粘贴")
        paste_action.setShortcut("Ctrl+V")
        paste_action.triggered.connect(parent.paste_text)
        file_menu.addAction(paste_action)

        cut_action = Action(FIF.CUT, "剪切")
        cut_action.setShortcut("Ctrl+X")
        cut_action.triggered.connect(parent.cut_text)
        file_menu.addAction(cut_action)

        undo_action = Action(FIF.CANCEL, "撤销")
        undo_action.setShortcut("Ctrl+Z")
        undo_action.triggered.connect(parent.undo_action)
        file_menu.addAction(undo_action)

        redo_action = Action(FIF.HISTORY, "重做")
        redo_action.setShortcut("Ctrl+Y")
        redo_action.triggered.connect(parent.redo_action)
        file_menu.addAction(redo_action)

        find_action = Action(FIF.SEARCH, "查找")
        find_action.setShortcut("Ctrl+F")
        find_action.triggered.connect(parent.find_text)
        file_menu.addAction(find_action)

        replace_action = Action(FIF.ZOOM, "替换")
        replace_action.setShortcut("Ctrl+Shift+R")
        replace_action.triggered.connect(parent.replace_text)
        file_menu.addAction(replace_action)

        file_menu.addSeparator()

        new_action = Action(FIF.ADD, "新建")
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(parent.onTabAddRequested)
        file_menu.addAction(new_action)

        open_action = Action(FIF.SEND_FILL, "打开")
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(parent.open_document)
        file_menu.addAction(open_action)

        save_action = Action(FIF.SAVE, "保存")
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(parent.save_document)
        file_menu.addAction(save_action)



        text_menu = RoundMenu("文字", self)

        text_menu.setIcon(FIF.EDIT)

        font_action = Action(FIF.FONT, "字体和大小")
        font_action.setShortcut("Alt+A")
        font_action.triggered.connect(parent.change_font)
        text_menu.addAction(font_action)

        # 欢迎去玩 palette 社的《纯白交响曲》！
        color_action = Action(FIF.PALETTE, "颜色")
        color_action.setShortcut("Alt+C")
        color_action.triggered.connect(parent.change_text_color)
        text_menu.addAction(color_action)

        text_menu.addSeparator()

        align_menu = RoundMenu("对齐", self)

        align_menu.setIcon(FIF.ALIGNMENT)

        left_align_action = Action(FIF.CARE_LEFT_SOLID, "左对齐")
        left_align_action.setShortcut("Alt+←")
        left_align_action.triggered.connect(parent.align_left)
        align_menu.addAction(left_align_action)

        center_align_action = Action(FIF.CARE_DOWN_SOLID, "居中对齐")
        center_align_action.setShortcut("Alt+↓")
        center_align_action.triggered.connect(parent.align_center)
        align_menu.addAction(center_align_action)

        right_align_action = Action(FIF.CARE_RIGHT_SOLID, "右对齐")
        right_align_action.setShortcut("Alt+→")
        right_align_action.triggered.connect(parent.align_right)
        align_menu.addAction(right_align_action)

        decoration_menu = RoundMenu("文本修饰", self)

        align_menu.setIcon(FIF.FONT_INCREASE)
        decoration_menu.setIcon(FIF.FONT_SIZE)

        bold_action = Action("粗体", self)
        bold_action.setShortcut("Ctrl+B")
        bold_action.triggered.connect(parent.toggle_bold)
        decoration_menu.addAction(bold_action)

        italic_action = Action("斜体", self)
        italic_action.setShortcut("Ctrl+I")
        italic_action.triggered.connect(parent.toggle_italic)
        decoration_menu.addAction(italic_action)

        underline_action = Action("下划线")
        underline_action.setShortcut("Ctrl+U")
        underline_action.triggered.connect(parent.toggle_underline)
        decoration_menu.addAction(underline_action)

        strikethrough_action = Action("删除线")
        strikethrough_action.setShortcut("Alt+S")
        strikethrough_action.triggered.connect(parent.toggle_strikethrough)
        decoration_menu.addAction(strikethrough_action)


        theme_menu = RoundMenu("主题", self)
        theme_menu.setIcon(FIF.CONSTRACT)

        dark_mode_action = Action(FIF.QUIET_HOURS, "暗黑模式")
        dark_mode_action.setShortcut("Alt+T")
        dark_mode_action.triggered.connect(lambda: self.change_theme(Theme.DARK))
        theme_menu.addAction(dark_mode_action)

        light_mode_action = Action(FIF.BRIGHTNESS, "明亮模式")
        light_mode_action.setShortcut("Alt+T")
        light_mode_action.triggered.connect(lambda: self.change_theme(Theme.LIGHT))
        theme_menu.addAction(light_mode_action)


        self.menu.addMenu(file_menu)
        self.menu.addMenu(text_menu)
        self.menu.addMenu(theme_menu)

        text_menu.addMenu(align_menu)
        text_menu.addMenu(decoration_menu)

        # 创建菜单按钮
        self.menuButton.clicked.connect(self.showMenu)

    def showMenu(self):
        # 在 menuButton 的左侧显示菜单
        self.menu.exec(self.menuButton.mapToGlobal(self.menuButton.rect().bottomLeft()))

    def canDrag(self, pos: QPoint):
        if not super().canDrag(pos):
            return False

        pos.setX(pos.x() - self.tabBar.x())
        return not self.tabBar.tabRegion().contains(pos)

    def test(self):
        print("hello")

    def change_theme(self, theme):
        self.parent().current_theme = theme
        setTheme(theme)
        self.parent().update_theme()


class Window(MSFluentWindow):

    def __init__(self):
        self.isMicaEnabled = True
        super().__init__()
        self.setTitleBar(CustomTitleBar(self))
        self.tabBar = self.titleBar.tabBar  # type: TabBar

        # 默认暗黑模式
        self.current_theme = Theme.DARK
        setTheme(self.current_theme)
        setThemeColor(QColor("red"))  # 设置红色强调色

        # 创建子界面
        self.homeInterface = QStackedWidget(self, objectName='homeInterface')

        self.tabBar.addTab(text="新建标签 1", routeKey="新建标签 1")
        self.tabBar.setCurrentTab('新建标签 1')
        self.initShortcuts()


        self.last_search = ""
        self.search_flags = QTextDocument.FindFlag(0)

        self.initNavigation()
        self.initWindow()

    # 快捷键
    def initShortcuts(self):
        # Ctrl
        bold_shortcut = QShortcut(QKeySequence("Ctrl+B"), self)
        bold_shortcut.activated.connect(self.toggle_bold)

        find_shortcut = QShortcut(QKeySequence("Ctrl+F"), self)
        find_shortcut.activated.connect(self.find_text)

        find_next_shortcut = QShortcut(QKeySequence("Ctrl+Down"), self)
        find_next_shortcut.activated.connect(self.find_next)

        find_previous_shortcut = QShortcut(QKeySequence("Ctrl+Up"), self)
        find_previous_shortcut.activated.connect(self.find_previous)

        italic_shortcut = QShortcut(QKeySequence("Ctrl+I"), self)
        italic_shortcut.activated.connect(self.toggle_italic)

        new_shortcut = QShortcut(QKeySequence("Ctrl+N"), self)
        new_shortcut.activated.connect(self.onTabAddRequested)

        open_shortcut = QShortcut(QKeySequence("Ctrl+O"), self)
        open_shortcut.activated.connect(self.open_document)

        save_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        save_shortcut.activated.connect(self.save_document)

        underline_shortcut = QShortcut(QKeySequence("Ctrl+U"), self)
        underline_shortcut.activated.connect(self.toggle_underline)

        strikethrough_shortcut = QShortcut(QKeySequence("Alt+S"), self)
        strikethrough_shortcut.activated.connect(self.toggle_strikethrough)

        # Alt
        font_shortcut = QShortcut(QKeySequence("Alt+A"), self)
        font_shortcut.activated.connect(self.change_font)

        color_shortcut = QShortcut(QKeySequence("Alt+C"), self)
        color_shortcut.activated.connect(self.change_text_color)

        theme_toggle_shortcut = QShortcut(QKeySequence("Alt+T"), self)
        theme_toggle_shortcut.activated.connect(self.toggle_theme)

        left_align_shortcut = QShortcut(QKeySequence("Alt+Left"), self)
        left_align_shortcut.activated.connect(self.align_left)

        center_align_shortcut = QShortcut(QKeySequence("Alt+Down"), self)
        center_align_shortcut.activated.connect(self.align_center)

        center_align_shortcut = QShortcut(QKeySequence("Alt+Up"), self)
        center_align_shortcut.activated.connect(self.align_center)

        right_align_shortcut = QShortcut(QKeySequence("Alt+Right"), self)
        right_align_shortcut.activated.connect(self.align_right)

        replace_shortcut = QShortcut(QKeySequence("Ctrl+Shift+R"), self)
        replace_shortcut.activated.connect(self.replace_text)

    def initNavigation(self):
        self.addSubInterface(self.homeInterface, QIcon("resource/write.svg"), 'Write', QIcon("resource/write.svg"))

        self.navigationInterface.addItem(
            routeKey='Help',
            icon=FIF.INFO,
            text='About',
            onClick=self.showMessageBox,
            selectable=False,
            position=NavigationItemPosition.BOTTOM,
        )

        self.navigationInterface.setCurrentItem(
            self.homeInterface.objectName())

        self.text_widgets = {}  # 创建一个字典来存储每个标签页的 TWidget 实例
        for i in range(self.tabBar.count()):  # 使用 count 遍历标签页
            routeKey = self.tabBar.tabText(i)  # 从 tabText 获取 routeKey

            # 为每个标签页创建一个新的 TWidget 实例
            t_widget = TWidget(self)
            self.text_widgets[routeKey] = t_widget  # 在字典中存储 TWidget 实例

            self.current_editor = t_widget

            # 将 TWidget 添加到相应的 TabInterface
            tab_interface = TabInterface(self.tabBar.tabText(i), 'icon', routeKey, self)
            tab_interface.vBoxLayout.addWidget(t_widget)
            self.homeInterface.addWidget(tab_interface)

        self.tabBar.currentChanged.connect(self.onTabChanged)
        self.tabBar.tabAddRequested.connect(self.onTabAddRequested)

    def initWindow(self):
        self.resize(1100, 750)
        self.setWindowIcon(QIcon('resource/icon.ico'))
        self.setWindowTitle('SimpleMDIExample')

        w, h = 1200, 800
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

    def showMessageBox(self):
        aboutWindow = MessageBox(
            'SimpleMDIExample 📝',
            (
                    "Version : 1.0"
                    + "\n" + "\n" + "\n"
                    + " CUMT 程序设计综合实践作业"
                    + "\n" + "\n"
                    + "相关库：PyQt6、QFluentWidgets (https://qfluentwidgets.com/)"
                    + "\n" + "\n" + "\n" +
                    "By KNWking"
            ),
            self
        )
        aboutWindow.yesButton.setText('GitHub')
        aboutWindow.cancelButton.setText('Return')

        if aboutWindow.exec():
            QDesktopServices.openUrl(QUrl("https://github.com/KNWking/"))

    def onTabChanged(self, index: int):
        objectName = self.tabBar.currentTab().routeKey()
        self.homeInterface.setCurrentWidget(self.findChild(TabInterface, objectName))
        self.stackedWidget.setCurrentWidget(self.homeInterface)

        # 获取当前活动的标签页
        current_tab = self.homeInterface.widget(index)

        if current_tab and isinstance(current_tab, TabInterface):
            # 更新当前的 TWidget
            self.current_editor = self.text_widgets[current_tab.objectName()]

    def copy_text(self):
        if self.current_editor:
            self.current_editor.copy()

    def paste_text(self):
        if self.current_editor:
            self.current_editor.paste()

    def cut_text(self):
        if self.current_editor:
            self.current_editor.cut()

    def undo_action(self):
        if self.current_editor:
            self.current_editor.undo()

    def redo_action(self):
        if self.current_editor:
            self.current_editor.redo()

    def onTabAddRequested(self):
        text = f'新建标签 {self.tabBar.count() + 1}'
        self.addTab(text, text, '')

        # 将 current_editor 设置为新添加的 TWidget
        self.current_editor = self.text_widgets[text]
        self.current_editor.update_theme()  # 确保新创建的编辑器使用正确的主题

        # 切换到新创建的标签页
        new_index = self.tabBar.count() - 1  # 新标签页的索引
        self.tabBar.setCurrentIndex(new_index)
        self.onTabChanged(new_index)  # 手动触发 onTabChanged 方法

    def open_document(self):
        file_path = filedialog.askopenfilename(
            title="打开文件",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
        )

        if not file_path:
            return

        try:
            # 检查是否存在对应的 HTML 文件
            html_path = os.path.splitext(file_path)[0] + '.html'
            if os.path.exists(html_path):
                # 如果存在 HTML 文件，读取 HTML 内容
                with open(html_path, "r", encoding='utf-8') as f:
                    filedata = f.read()
                new_tab_name = os.path.basename(file_path)
                self.addTab(new_tab_name, new_tab_name, '')
                self.current_editor.setHtml(filedata)
            else:
                # 如果不存在 HTML 文件，读取纯文本内容
                with open(file_path, "r", encoding='utf-8') as f:
                    filedata = f.read()
                new_tab_name = os.path.basename(file_path)
                self.addTab(new_tab_name, new_tab_name, '')
                self.current_editor.setPlainText(filedata)

            self.current_editor.file_path = file_path
            self.current_editor.setFocus()

            # 切换到新打开的文件标签页
            new_index = self.tabBar.count() - 1  # 新标签页的索引
            self.tabBar.setCurrentIndex(new_index)
            self.onTabChanged(new_index)  # 手动触发 onTabChanged 方法

        except Exception as e:
            print(f"打开文件时发生错误: {e}")

    def save_document(self):
        if not self.current_editor:
            return

        if not hasattr(self.current_editor, 'file_path') or not self.current_editor.file_path:
            file_path = filedialog.asksaveasfilename(
                title="保存文件",
                filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")],
                defaultextension=".txt"  # 设置默认扩展名
            )
            if not file_path:
                return
            # 如果用户没有指定 .txt 后缀，自动添加
            if not file_path.lower().endswith('.txt'):
                file_path += '.txt'
            self.current_editor.file_path = file_path
        else:
            file_path = self.current_editor.file_path

        try:
            # 保存纯文本内容
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(self.current_editor.toPlainText())

            # 检查是否包含富文本格式
            if self.current_editor.document().allFormats():
                # 如果包含格式，保存为 HTML
                html_path = os.path.splitext(file_path)[0] + '.html'
                with open(html_path, 'w', encoding='utf-8') as html_file:
                    html_file.write(self.current_editor.toHtml())

            print("文件保存成功。")
        except Exception as e:
            print(f"保存文档时发生错误: {e}")

    def change_font(self):
        if self.current_editor:
            cursor = self.current_editor.textCursor()
            has_selection = cursor.hasSelection()

            if has_selection:
                # 如果有选中的文本，获取选中文本的字体
                format = cursor.charFormat()
                current_font = format.font()
            else:
                # 如果没有选中的文本，获取光标位置的字体
                current_font = self.current_editor.currentFont()

            font, ok = QFontDialog.getFont(current_font, self, "选择字体")
            if ok:
                if has_selection:
                    # 如果有选中的文本，只改变选中文本的字体
                    format = QTextCharFormat()
                    format.setFont(font)
                    cursor.mergeCharFormat(format)
                else:
                    # 如果没有选中的文本，改变整个文档的字体
                    self.current_editor.selectAll()
                    self.current_editor.setCurrentFont(font)
                    cursor.clearSelection()
                    self.current_editor.setTextCursor(cursor)

                # 更新当前编辑器的默认字体，只影响新输入的文本

    def change_text_color(self):
        if self.current_editor:
            cursor = self.current_editor.textCursor()
            current_color = self.current_editor.textColor()

            color_dialog = ColorDialog(current_color, "选择文字颜色", self, enableAlpha=False)

            def apply_color(color):
                if cursor.hasSelection():
                    # 如果有选中的文本，只改变选中文本的颜色
                    format = QTextCharFormat()
                    format.setForeground(color)
                    cursor.mergeCharFormat(format)
                else:
                    # 如果没有选中的文本，改变光标位置的文字颜色
                    self.current_editor.setTextColor(color)

            color_dialog.colorChanged.connect(apply_color)

            if color_dialog.exec():
                # 用户点击了确定按钮
                final_color = color_dialog.color
                apply_color(final_color)

    def font_size(self):
        return None

    def align_left(self):
        if self.current_editor:
            self.current_editor.setAlignment(Qt.AlignmentFlag.AlignLeft)

    def align_center(self):
        if self.current_editor:
            self.current_editor.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def align_right(self):
        if self.current_editor:
            self.current_editor.setAlignment(Qt.AlignmentFlag.AlignRight)

    def toggle_bold(self):
        if self.current_editor:
            cursor = self.current_editor.textCursor()
            format = QTextCharFormat()
            if cursor.charFormat().fontWeight() == QFont.Weight.Bold:
                format.setFontWeight(QFont.Weight.Normal)
            else:
                format.setFontWeight(QFont.Weight.Bold)
            cursor.mergeCharFormat(format)
            self.current_editor.setTextCursor(cursor)

    def toggle_italic(self):
        if self.current_editor:
            cursor = self.current_editor.textCursor()
            format = QTextCharFormat()
            format.setFontItalic(not cursor.charFormat().fontItalic())
            cursor.mergeCharFormat(format)
            self.current_editor.setTextCursor(cursor)

    def toggle_underline(self):
        if self.current_editor:
            cursor = self.current_editor.textCursor()
            format = QTextCharFormat()
            format.setFontUnderline(not cursor.charFormat().fontUnderline())
            cursor.mergeCharFormat(format)
            self.current_editor.setTextCursor(cursor)

    def toggle_strikethrough(self):
        if self.current_editor:
            cursor = self.current_editor.textCursor()
            format = QTextCharFormat()
            format.setFontStrikeOut(not cursor.charFormat().fontStrikeOut())
            cursor.mergeCharFormat(format)
            self.current_editor.setTextCursor(cursor)

    def update_theme(self):
        # 更新所有编辑器的样式
        for editor in self.text_widgets.values():
            editor.update_theme()

        # 更新其他UI元素
        self.update()

        # 强制重绘所有编辑器
        for editor in self.text_widgets.values():
            editor.viewport().update()

        # 更新其他UI元素
        self.update()

    def toggle_theme(self):
        if not hasattr(self, 'current_theme'):
            self.current_theme = Theme.DARK if isDarkTheme() else Theme.LIGHT

        self.current_theme = Theme.LIGHT if self.current_theme == Theme.DARK else Theme.DARK
        setTheme(self.current_theme)
        self.update_theme()

        # 强制所有编辑器重新应用主题
        for editor in self.text_widgets.values():
            editor.update_theme()

    def update_theme(self):
        # 更新所有编辑器的样式
        for editor in self.text_widgets.values():
            if isDarkTheme():
                editor.setStyleSheet("QTextEdit{background-color: #000000; color: white; border: 0;}")
            else:
                editor.setStyleSheet("QTextEdit{background-color: white; color: black; border: 0;}")

        # 更新其他UI元素
        self.update()

    def find_text(self):
        if self.current_editor:
            text, ok = QInputDialog.getText(self, '查找', '输入要查找的文本:', text=self.last_search)
            if ok and text:
                self.last_search = text
                self.find_next()
                # 启用前进后退按钮
                self.titleBar.forwardButton.setEnabled(True)
                self.titleBar.backButton.setEnabled(True)

    def find_next(self):
        if self.current_editor and self.last_search:
            found = self.current_editor.find(self.last_search, self.search_flags)
            if not found:
                # 如果没找到，从头开始搜索
                cursor = self.current_editor.textCursor()
                cursor.movePosition(QTextCursor.MoveOperation.Start)
                self.current_editor.setTextCursor(cursor)
                found = self.current_editor.find(self.last_search, self.search_flags)
                if not found:
                    self.show_not_found_dialog()

    def find_previous(self):
        if self.current_editor and self.last_search:
            flags = self.search_flags | QTextDocument.FindFlag.FindBackward
            found = self.current_editor.find(self.last_search, flags)
            if not found:
                # 如果没找到，从尾部开始搜索
                cursor = self.current_editor.textCursor()
                cursor.movePosition(QTextCursor.MoveOperation.End)
                self.current_editor.setTextCursor(cursor)
                found = self.current_editor.find(self.last_search, flags)
                if not found:
                    self.show_not_found_dialog()

    def show_not_found_dialog(self):
        dialog = Dialog(
            "查找结果",
            f"未找到匹配文本: '{self.last_search}'",
            self
        )
        dialog.yesButton.setText("确定")
        dialog.cancelButton.hide()
        dialog.buttonLayout.insertStretch(1)
        dialog.exec()

    def replace_text(self):
        if self.current_editor:
            dialog = QDialog(self)
            dialog.setWindowTitle("替换")
            layout = QVBoxLayout()

            # 查找输入框
            find_layout = QHBoxLayout()
            find_layout.addWidget(QLabel("查找:"))
            find_input = QLineEdit()
            find_layout.addWidget(find_input)
            layout.addLayout(find_layout)

            # 替换输入框
            replace_layout = QHBoxLayout()
            replace_layout.addWidget(QLabel("替换为:"))
            replace_input = QLineEdit()
            replace_layout.addWidget(replace_input)
            layout.addLayout(replace_layout)

            # 按钮
            button_layout = QHBoxLayout()
            find_button = QPushButton("查找下一个")
            replace_button = QPushButton("替换")
            replace_all_button = QPushButton("全部替换")
            button_layout.addWidget(find_button)
            button_layout.addWidget(replace_button)
            button_layout.addWidget(replace_all_button)
            layout.addLayout(button_layout)

            dialog.setLayout(layout)

            def find_next():
                text = find_input.text()
                if text:
                    cursor = self.current_editor.document().find(text, self.current_editor.textCursor())
                    if not cursor.isNull():
                        self.current_editor.setTextCursor(cursor)
                    else:
                        InfoBar.success(
                            title='查找结果',
                            content="已到达文档末尾，从头开始查找",
                            orient=Qt.Orientation.Horizontal,
                            isClosable=True,
                            position=InfoBarPosition.TOP,
                            duration=2000,
                            parent=self
                        )
                        cursor = self.current_editor.document().find(text, QTextCursor(self.current_editor.document()))
                        if not cursor.isNull():
                            self.current_editor.setTextCursor(cursor)
                        else:
                            InfoBar.warning(
                                title='查找结果',
                                content=f"未找到匹配文本: '{text}'",
                                orient=Qt.Orientation.Horizontal,
                                isClosable=True,
                                position=InfoBarPosition.TOP,
                                duration=2000,
                                parent=self
                            )

            def replace():
                if self.current_editor.textCursor().hasSelection():
                    self.current_editor.textCursor().insertText(replace_input.text())
                find_next()

            def replace_all():
                text = find_input.text()
                replace_text = replace_input.text()
                cursor = QTextCursor(self.current_editor.document())
                count = 0
                while True:
                    cursor = self.current_editor.document().find(text, cursor)
                    if cursor.isNull():
                        break
                    cursor.insertText(replace_text)
                    count += 1
                InfoBar.success(
                    title='替换结果',
                    content=f"已替换 {count} 处文本",
                    orient=Qt.Orientation.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=2000,
                    parent=self
                )

            find_button.clicked.connect(find_next)
            replace_button.clicked.connect(replace)
            replace_all_button.clicked.connect(replace_all)

            dialog.exec()

    def addTab(self, routeKey, text, icon):
        self.tabBar.addTab(routeKey, text, icon)
        self.homeInterface.addWidget(TabInterface(text, icon, routeKey, self))
        # 为新标签页创建一个新的 TWidget 实例
        t_widget = TWidget(self)
        self.text_widgets[routeKey] = t_widget  # 在字典中存储 TWidget 实例
        tab_interface = self.findChild(TabInterface, routeKey)
        tab_interface.vBoxLayout.addWidget(t_widget)
        self.current_editor = t_widget  # 将 TWidget 添加到相应的 TabInterface


if __name__ == '__main__':
    font = QFont("Microsoft YaHei UI", 12)
    app = QApplication(sys.argv)
    app.setFont(font)
    w = Window()
    w.setStyleSheet(style_sheet)
    w.show()
    sys.exit(app.exec())
