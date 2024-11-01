import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from tkinter import messagebox, filedialog
import os
from PyQt6.QtGui import *
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import *
from qframelesswindow import *

write_icon = QIcon("./resource/write.svg")
about_icon = QIcon("./resource/write.svg")

# Stylesheet 保持不变
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
    """


class TWidget(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFont(QFont("DotNess", 16))
        self.setAcceptRichText(False)
        self.setStyleSheet("QTextEdit{background-color : #000000; color : white; border: 0;}")


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
        new_action = Action(FIF.ADD, "新建")
        new_action.triggered.connect(parent.onTabAddRequested)
        file_menu.addAction(new_action)

        open_action = Action(FIF.SEND_FILL, "打开")
        open_action.triggered.connect(parent.open_document)
        file_menu.addAction(open_action)

        file_menu.addSeparator()

        save_action = Action(FIF.SAVE, "保存")
        save_action.triggered.connect(parent.save_document)
        file_menu.addAction(save_action)

        self.menu.addMenu(file_menu)

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

        self.tabBar.addTab(text="Glyph 1", routeKey="Glyph 1")
        self.tabBar.setCurrentTab('Glyph 1')

        # self.current_editor = self.text_widgets["Scratch 1"]

        self.initNavigation()
        self.initWindow()

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
        w = MessageBox(
            'Notes(1) 📝',
            (
                    "Version : 1.0"
                    + "\n" + "\n" + "\n" + "💝  I hope you'll enjoy using notes(1) as much as I did while coding it  💝" + "\n" + "\n" + "\n" +
                    "Made with 💖 By Rohan Kishore"
            ),
            self
        )
        w.yesButton.setText('GitHub')
        w.cancelButton.setText('Return')

        if w.exec():
            QDesktopServices.openUrl(QUrl("https://github.com/rohankishore/"))

    def onTabChanged(self, index: int):
        objectName = self.tabBar.currentTab().routeKey()
        self.homeInterface.setCurrentWidget(self.findChild(TabInterface, objectName))
        self.stackedWidget.setCurrentWidget(self.homeInterface)

        # 获取当前活动的标签页
        current_tab = self.homeInterface.widget(index)

        if current_tab and isinstance(current_tab, TabInterface):
            # 更新当前的 TWidget
            self.current_editor = self.text_widgets[current_tab.objectName()]

    def onTabAddRequested(self):
        text = f'Glyph {self.tabBar.count() + 1}'
        self.addTab(text, text, '')

        # 将 current_editor 设置为新添加的 TWidget
        self.current_editor = self.text_widgets[text]

    def open_document(self):
        file_dir = filedialog.askopenfilename(
            title="选择文件",
        )
        filename = os.path.basename(file_dir).split('/')[-1]

        if file_dir:
            try:
                f = open(file_dir, "r")
                filedata = f.read()
                self.addTab(filename, filename, '')
                self.current_editor.setPlainText(filedata)
                f.close()
            except UnicodeDecodeError:
                messagebox.showerror("错误的文件类型！", "不支持此文件类型！")

    def save_document(self):
        try:
            if not self.current_editor:
                print("未找到活动的 TWidget.")
                return  # 检查是否有活动的 TWidget

            text_to_save = self.current_editor.toPlainText()
            print("要保存的文本：", text_to_save)  # Debug print

            name = filedialog.asksaveasfilename(
                title="选择文件",
                filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
            )

            print("要保存的文件路径：", name)  # Debug print

            if name:
                with open(name, 'w') as file:
                    file.write(text_to_save)
                    title = os.path.basename(name) + " ~ ZenNotes"
                    active_tab_index = self.tabBar.currentIndex()
                    self.tabBar.setTabText(active_tab_index, os.path.basename(name))
                    self.setWindowTitle(title)
                    print("文件保存成功。")  # Debug print
        except Exception as e:
            print(f"保存文档时发生错误: {e}")

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
    font = QFont("DotNess", 12)
    app = QApplication(sys.argv)
    app.setFont(font)
    w = Window()
    w.setStyleSheet("background-color : black;")
    w.show()
    sys.exit(app.exec())
