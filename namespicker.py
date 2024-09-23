import sys, os
import random
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QMessageBox
from PySide6.QtCore import Qt, QTimer
import qdarktheme

class RandomPicker(QWidget):
    def __init__(self):
        super().__init__()
        # 初始化界面
        self.initUI()

        # 姓名列表
        self.names = []

        # 计时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showName)

    def initUI(self):
        # 选择姓名文件按钮
        self.selectFilesBtn = QPushButton('选择姓名文件（回车）', self)
        self.selectFilesBtn.clicked.connect(self.selectMultipleFiles)

        # 开始/结束按钮
        self.startStopBtn = QPushButton('开始点名（Alt）', self)
        self.startStopBtn.clicked.connect(self.startStop)

        # 切换浅色/深色模式
        self.toggleDarkModeBtn = QPushButton('深/浅', self)
        self.toggleDarkModeBtn.clicked.connect(self.toggleDarkMode)
        self.darkmode = False

        # 姓名标签
        self.nameLabel = QLabel(self)
        self.nameLabel.setAlignment(Qt.AlignCenter)
        self.nameLabel.setStyleSheet('font-size: 100px')

        # 布局
        buttonlayout = QHBoxLayout()
        nameLayout = QHBoxLayout()
        layout = QVBoxLayout()
        buttonlayout.addWidget(self.selectFilesBtn)
        buttonlayout.addWidget(self.startStopBtn)
        buttonlayout.addWidget(self.toggleDarkModeBtn)
        layout.addLayout(buttonlayout)
        nameLayout.addWidget(self.nameLabel)
        layout.addLayout(nameLayout)
        self.setLayout(layout)

        # 窗口属性
        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle('随机点名器')
        self.show()

    def selectMultipleFiles(self):
        self.names = []
        # 弹出文件选择对话框
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileNames, _ = QFileDialog.getOpenFileNames(self, '选择姓名文件', '', 'Text Files (*.txt)', options=options)

        # 如果选择了文件，则读取文件中的姓名
        for fileName in fileNames:
            try:
                with open(fileName, 'r',encoding='utf-8') as f:
                    self.names += [line.strip() for line in f.readlines()]
            except UnicodeDecodeError:
                QMessageBox.warning(self, '警告', f'文件 {fileName} 不是有效的UTF-8编码文件，请选择其他文件！')
        self.setWindowTitle('随机点名器 ' + ', '.join([os.path.splitext(os.path.basename(fileName))[0] for fileName in fileNames]))

    def startStop(self):
        if self.timer.isActive():
            # 如果计时器已经启动，则停止计时器
            self.timer.stop()
            self.startStopBtn.setText('开始点名（Alt）')
        else:
            # 如果计时器未启动，则启动计时器
            if self.names:
                self.timer.start(50)
                self.startStopBtn.setText('停止点名（Alt）')
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.selectMultipleFiles()
        elif event.key() == Qt.Key_Alt:
            self.startStop()

    def toggleDarkMode(self):
        if self.darkmode:
            qdarktheme.setup_theme("light")
        else:
            qdarktheme.setup_theme("dark")
        self.darkmode = not self.darkmode

    def showName(self):
        # 显示随机姓名
        if self.names:
            self.nameLabel.setText(random.choice(self.names))
        else:
            QMessageBox.warning(self, '警告', '姓名文件列表为空，请选择姓名文件！')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    qdarktheme.setup_theme("light")
    picker = RandomPicker()
    sys.exit(app.exec())
