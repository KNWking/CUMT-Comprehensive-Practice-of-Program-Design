import sys
import json
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from tkinter import messagebox, filedialog
import os
from PyQt6.QtGui import *
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import *
from qframelesswindow import *

# write_icon = QIcon("./resource/write.svg")
# about_icon = QIcon("./resource/write.svg")
# BOLD_ICON = QIcon("./resource/bold-24.svg")
# ITALIC_ICON = QIcon("./resource/italic-24.svg")

style_sheet = f"""
        QMenuBar {{
            background-color: #323232;
        }}
        QMenuBar::item {{
            background-color: #323232;
            color: red;
        }}
        QMenuBar::item::selected {{
            background-color: #1b1b1b;
        }}
        QMenu {{
            background-color: rgb(49, 49, 49);
            color: red;
            border: 0px solid #000;
        }}
        QMenu::item::selected {{
            background-color: rgb(30, 30, 30);
        }}
        QTextEdit {{
        background-color: #000000;
        color: white;
        border: 0;
    }}
    """


class TWidget(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFont(QFont("Microsoft YaHei UI", 16))
        self.setStyleSheet("QTextEdit{background-color : #000000; color : white; border: 0;}")
        self.setTextColor(QColor("white"))


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
        self.forwardButton = TransparentToolButton(FIF.RIGHT_ARROW.icon(color=color), self)
        self.backButton = TransparentToolButton(FIF.LEFT_ARROW.icon(color=color), self)

        # self.openButton = TransparentToolButton(QIcon("resource/open.png"), self)
        # self.openButton.clicked.connect(parent.open_document)
        # self.newButton = TransparentToolButton(QIcon("resource/new.png"), self)
        # self.newButton.clicked.connect(parent.onTabAddRequested)
        # self.saveButton = TransparentToolButton(QIcon("resource/save.png"), self)
        # self.saveButton.clicked.connect(parent.save_document)

        self.forwardButton.setDisabled(True)
        self.toolButtonLayout.setContentsMargins(20, 0, 20, 0)
        self.toolButtonLayout.setSpacing(15)
        self.toolButtonLayout.addWidget(self.menuButton)
        self.toolButtonLayout.addWidget(self.backButton)
        self.toolButtonLayout.addWidget(self.forwardButton)

        # self.toolButtonLayout.addWidget(self.openButton)
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
        # self.tabBar.currentChanged.connect(lambda i: print(self.tabBar.tabText(i)))

        self.hBoxLayout.insertWidget(5, self.tabBar, 1)
        self.hBoxLayout.setStretch(6, 0)

        # self.hBoxLayout.insertWidget(7, self.saveButton, 0, Qt.AlignmentFlag.AlignLeft)
        # self.hBoxLayout.insertWidget(7, self.openButton, 0, Qt.AlignmentFlag.AlignLeft)
        # self.hBoxLayout.insertWidget(7, self.newButton, 0, Qt.AlignmentFlag.AlignLeft)
        # self.hBoxLayout.insertSpacing(8, 20)

        self.menu = RoundMenu("目录")
        self.menu.setStyleSheet("QMenu{color : red;}")

        file_menu = RoundMenu("文件", self)

        file_menu.setIcon(FIF.FOLDER)

        copy_action = Action(FIF.COPY, "复制")
        copy_action.triggered.connect(parent.copy_text)
        file_menu.addAction(copy_action)

        paste_action = Action(FIF.PASTE, "粘贴")
        paste_action.triggered.connect(parent.paste_text)
        file_menu.addAction(paste_action)

        cut_action = Action(FIF.CUT, "剪切")
        cut_action.triggered.connect(parent.cut_text)
        file_menu.addAction(cut_action)

        undo_action = Action(FIF.CANCEL, "撤销")
        undo_action.triggered.connect(parent.undo_action)
        file_menu.addAction(undo_action)

        redo_action = Action(FIF.HISTORY, "重做")
        redo_action.triggered.connect(parent.redo_action)
        file_menu.addAction(redo_action)

        file_menu.addSeparator()

        new_action = Action(FIF.ADD, "新建")
        new_action.triggered.connect(parent.onTabAddRequested)
        file_menu.addAction(new_action)

        open_action = Action(FIF.SEND_FILL, "打开")
        open_action.triggered.connect(parent.open_document)
        file_menu.addAction(open_action)

        save_action = Action(FIF.SAVE, "保存")
        save_action.triggered.connect(parent.save_document)
        file_menu.addAction(save_action)

        text_menu = RoundMenu("文字", self)

        text_menu.setIcon(FIF.EDIT)

        font_action = Action(FIF.FONT, "字体")
        font_action.triggered.connect(parent.change_font)
        text_menu.addAction(font_action)

        size_action = Action(FIF.FONT_SIZE, "文字大小")
        size_action.triggered.connect(parent.font_size)
        text_menu.addAction(size_action)

        # 欢迎去玩 palette 社的《纯白交响曲》！
        color_action = Action(FIF.PALETTE, "颜色")
        color_action.triggered.connect(parent.change_color)
        text_menu.addAction(color_action)

        text_menu.addSeparator()

        align_menu = RoundMenu("对齐", self)

        align_menu.setIcon(FIF.ALIGNMENT)

        left_align_action = Action(FIF.CARE_LEFT_SOLID, "左对齐")
        left_align_action.triggered.connect(parent.align_left)
        align_menu.addAction(left_align_action)

        center_align_action = Action(FIF.CARE_DOWN_SOLID, "居中对齐")
        center_align_action.triggered.connect(parent.align_center)
        align_menu.addAction(center_align_action)

        right_align_action = Action(FIF.CARE_RIGHT_SOLID, "右对齐")
        right_align_action.triggered.connect(parent.align_right)
        align_menu.addAction(right_align_action)

        decoration_menu = RoundMenu("文本修饰", self)

        align_menu.setIcon(FIF.FONT_INCREASE)

        # bold_action = Action(BOLD_ICON, "粗体")
        bold_action = Action("粗体", self)
        bold_action.triggered.connect(parent.toggle_bold)
        decoration_menu.addAction(bold_action)

        # italic_action = Action(ITALIC_ICON, "斜体")
        italic_action = Action("斜体", self)
        italic_action.triggered.connect(parent.toggle_italic)
        decoration_menu.addAction(italic_action)

        underline_action = Action("下划线")
        underline_action.triggered.connect(parent.toggle_underline)
        decoration_menu.addAction(underline_action)

        self.menu.addMenu(file_menu)
        self.menu.addMenu(text_menu)

        text_menu.addMenu(align_menu)
        text_menu.addMenu(decoration_menu)

        # 创建菜单按钮
        # self.menuButton = TransparentToolButton(FIF.MENU, self)
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


class Window(MSFluentWindow):

    def __init__(self):
        self.isMicaEnabled = True
        super().__init__()
        self.setTitleBar(CustomTitleBar(self))
        self.tabBar = self.titleBar.tabBar  # type: TabBar

        setTheme(Theme.DARK)
        setThemeColor(QColor("red"))  # 设置红色强调色

        # 创建子界面
        self.homeInterface = QStackedWidget(self, objectName='homeInterface')
        # self.settingsInterface = Widget('Application Interface', self)
        # self.videoInterface = Widget('Video Interface', self)
        # self.libraryInterface = Widget('library Interface', self)

        self.tabBar.addTab(text="新建标签 1", routeKey="新建标签 1")
        self.tabBar.setCurrentTab('新建标签 1')
        self.initShortcuts()

        # self.current_editor = self.text_widgets["Scratch 1"]

        self.initNavigation()
        self.initWindow()

    def initShortcuts(self):
        bold_shortcut = QShortcut(QKeySequence("Ctrl+B"), self)
        bold_shortcut.activated.connect(self.toggle_bold)

        italic_shortcut = QShortcut(QKeySequence("Ctrl+I"), self)
        italic_shortcut.activated.connect(self.toggle_italic)

        underline_shortcut = QShortcut(QKeySequence("Ctrl+U"), self)
        underline_shortcut.activated.connect(self.toggle_underline)

        save_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        save_shortcut.activated.connect(self.save_document)

        open_shortcut = QShortcut(QKeySequence("Ctrl+O"), self)
        open_shortcut.activated.connect(self.open_document)

        new_shortcut = QShortcut(QKeySequence("Ctrl+N"), self)
        new_shortcut.activated.connect(self.onTabAddRequested)

    def initNavigation(self):
        self.addSubInterface(self.homeInterface, QIcon("resource/write.svg"), 'Write', QIcon("resource/write.svg"))
        # self.addSubInterface(self.appInterface, FIF.ALBUM, '应用')
        # self.addSubInterface(self.videoInterface, FIF.EMBED, '视频')

        # self.addSubInterface(self.libraryInterface, FIF.BOOK_SHELF,
        #                      '库', FIF.LIBRARY_FILL, NavigationItemPosition.BOTTOM)
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

        #        desktop = QApplication.desktop().availableGeometry()
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
                filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
            )
            if not file_path:
                return
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
        return None

    def change_color(self):
        return None

    def font_size(self):
        return None

    def align_left(self):
        return None

    def align_center(self):
        return None

    def align_right(self):
        return None

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
