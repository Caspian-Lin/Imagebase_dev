from PyQt5.QtCore import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
import sys, json, sqlite3
from PIL import ImageGrab
from PyQt5.QtWidgets import QWidget

class baseUI(QMainWindow):
    def __init__(self):
        super(baseUI, self).__init__()        
        self.window_stack = []
        self.SelfUI()
    
    def SelfUI(self):        
        global screensize
        screensize = ImageGrab.grab().size
        self.setGeometry (200,200, int(0.75*screensize[0]),int(0.6*screensize[1]))
        self.setWindowTitle("初始主视图")

        self.menuBar_01()
        self.base_list_widget()
        self.buttongroup()
        self.layout_01()

    ###功能模块###

    def menuBar_01(self):
        self.menuBar_ = self.menuBar()
        submenu1=self.menuBar_.addMenu(("File"))
        submenu2=self.menuBar_.addMenu(("preference"))
        self.label1 = QLabel(self)
        self.label1.setText("imagebase")
        self.label1.move(50,50)

    def base_list_widget(self):
        basecontent =self.load_base_content()
        listcol = list(basecontent[0].keys())
        self.base_list = QTableWidget(len(basecontent),len(listcol))
        self.choosed_base_dir =-1
        for row in range(len(basecontent)):
            for col in range(len(listcol)):
                item = QTableWidgetItem(str(basecontent[row][listcol[col]]))
                self.base_list.setItem(row, col, item)
        self.base_list.setHorizontalHeaderLabels(listcol)
        # 设置tableWidget所有列的默认行高为20。
        #self.base_list.verticalHeader().setDefaultSectionSize(20)
        # 设置tableWidget所有行的默认列宽为20
        self.base_list.horizontalHeader().setDefaultSectionSize(200)
        self.base_list.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.base_list.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.base_list.setSelectionMode(QAbstractItemView.SingleSelection)
        self.base_list.cellClicked.connect(self.print_row_col)

    def buttongroup(self):
        self.button_select_file = QPushButton(self)
        self.button_select_file.setText("选择文件")
        self.button_select_file.adjustSize()
        self.button_select_file.clicked.connect(self.open_file_dialog)

        self.button_select_directory = QPushButton(self)
        self.button_select_directory.setText("选择文件夹")
        self.button_select_directory.adjustSize()
        self.button_select_directory.clicked.connect(self.open_directory_dialoge)

        self.button_imgBm = QPushButton(self)
        self.button_imgBm.setText("进入主视图")
        self.button_imgBm.adjustSize()
        self.button_imgBm.clicked.connect(self.into_imgBasemain)

        self.button_Create_imgB = QPushButton(self)
        self.button_Create_imgB.setText("创建新库")
        self.button_Create_imgB.adjustSize()
        self.button_Create_imgB.clicked.connect(self.create_new_ImgB)

        self.groupbox =QButtonGroup(self)
        self.groupbox.addButton(self.button_select_file)
        self.groupbox.addButton(self.button_select_directory)
        self.groupbox.addButton(self.button_imgBm)
        self.groupbox.addButton(self.button_Create_imgB)

    def layout_01(self):
        self.sublayout1 = QVBoxLayout()
        self.sublayout1.addWidget(self.button_select_file)
        self.sublayout1.addWidget(self.button_select_directory)
        self.sublayout1.addWidget(self.button_imgBm)
        self.sublayout1.addWidget(self.button_Create_imgB)

        self.central_layout = QHBoxLayout()
        self.central_layout.addWidget(self.base_list)
        self.central_layout .addLayout(self.sublayout1)
        self.central_widget = QWidget(self)
        self.central_widget.setLayout(self.central_layout)
        self.setCentralWidget(self.central_widget)
        
    ###窗口逻辑

    def into_imgBasemain(self):
        if  self.choosed_base_dir == -1:
            print("请选中一个数据库")
        else:
            new_window = ImagebaseMain() #创建新窗口实例
            self.window_stack.append(new_window)  # 将新窗口压入栈
            new_window.show()  # 显示新窗口
    
    def into_imgPrev(self):
        new_window = ImagePreviewer()#创建新窗口实例
        self.window_stack.append(new_window)  # 将新窗口压入栈
        new_window.show()  # 显示新窗口

    def close_current_window(self):
        if self.window_stack:
            current_window = self.window_stack.pop()
            current_window.close()  # 关闭窗口
            if self.window_stack:
                self.window_stack[-1].raise_()

    ###功能函数

    def open_file_dialog(self):
        fname, _ = QFileDialog.getOpenFileName(self, "选择输入文件", "", "所有文件 (*)")
        return fname
    
    def open_directory_dialoge(self):
        dir = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        base_dir=[]
        if not base_dir:
            base_dir.append(dir)
        else:
            base_dir[0]=dir
        return dir
    
    def create_new_ImgB(self):
        #等待下一步施工
        print("pressed 创建新库")
        return 
    
    def print_row_col(self, row, col):
        self.choosed_base_dir = self.base_content_list[row]["dir"]
        self.basename =self.base_content_list[row]["baseName"]
        print(f"Clicked cell: Row {row}, Column {col}")
              
    def load_base_content(self):
        #读取配置
        configJson=open("config.json","r")
        configdata=json.load(configJson)
        #返回现有库信息，[{:,:...},{:,:...}...]
        self.base_content_list=[]
        for i in configdata["base_content"]:
            self.base_content_list.append(configdata[i])
        return self.base_content_list 
    
"""
        if base_dir:
            self.label2 = QtWidgets.QLabel(self)
            self.label2.setText(f"已选择{base_dir[0]}，是否进入此目录作为数据库")
            self.button_dir_as_base.adjustSize()
            self.label2.move(50,400)

            self.button_dir_as_base = QPushButton(self)
            self.button_dir_as_base.setText("进入目录")
            self.button_dir_as_base.adjustSize()
            self.button_dir_as_base.clicked.connect(filebrowser02)
            self.button_dir_as_base.move(50,450)

"""

class ImagebaseMain(QMainWindow):
    def __init__(self):
        super(ImagebaseMain, self).__init__()
        self.SelfUI()

    def SelfUI(self):  
        self.setWindowTitle(f'imagebase-{win.basename}')
        self.setGeometry (200,200, int(0.75*screensize[0]),int(0.6*screensize[1]))

        self.menubar_01()
        self.imagePrev_view()
        self.button_group()
        self.filetree_view()
        self.imglist_widget()
        self.layout01()

    ###功能模块###

    def menubar_01(self):
        menubar = self.menuBar()
        # 创建一个 File 菜单
        submenu1 = menubar.addMenu("File")
        # 添加一个打开文件的动作
        open_action = QAction("Open", self)
        submenu1.addAction(open_action)
        # 添加一个退出应用的动作
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        submenu1.addAction(exit_action)
    def imagePrev_view(self):
        self.image_prev = QLabel()

    def button_group(self):
        self.button_imgprev = QPushButton(self)
        self.button_imgprev.setText("进入预览")
        self.button_imgprev.adjustSize()
        self.button_imgprev.clicked.connect(win.into_imgPrev)

    def filetree_view(self):
        model = QFileSystemModel()
        model.setRootPath(QDir.currentPath())
        self.filetree =  QTreeView()
        self.filetree.setModel(model)
        self.filetree.setRootIndex(model.index(QDir.currentPath()))

    def imglist_widget(self):
        # 执行查询
        conn = sqlite3.connect(win.choosed_base_dir)
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM main ''')
        query=cursor.fetchall()
        # 创建列表模型并填充数据

        cursor.execute('''PRAGMA table_info(main)''')
        base_describe = cursor.fetchall()
        listcol  = [row[1] for row in base_describe]
        self.img_list = QTableWidget(len(query),len(listcol))
        self.choosed_base_dir =-1
        for row in range(len(query)):
            for col in range(len(listcol)):
                item = QTableWidgetItem(str(query[row][col]))
                self.img_list.setItem(row, col, item)
        self.img_list.setHorizontalHeaderLabels(listcol)
        # 设置tableWidget所有列的默认行高为20。
        self.img_list.verticalHeader().setDefaultSectionSize(20)
        # 设置tableWidget所有行的默认列宽为20
        self.img_list.horizontalHeader().setDefaultSectionSize(200)
        self.img_list.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        '''lf.img_list.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.img_list.setSelectionMode(QAbstractItemView.SingleSelection)'''
        self.img_list.cellClicked.connect(self.imagePrev_show)

    def layout01(self):
        # 布局
        layout = QHBoxLayout()      
        layout.addWidget(self.filetree)
        layout.addWidget(self.img_list)
        layout.addWidget(self.button_imgprev)
        layout.addWidget(self.image_prev)
                    
        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    ###功能函数

    def imagePrev_show(self):
        #待施工
        pass

class ImagePreviewer(QMainWindow):
    def __init__(self):
        super(ImagePreviewer, self).__init__()
        self.SelfUI()
    
    def SelfUI(self):
        self.setWindowTitle('imagebase-preview')
        self.setGeometry (200,200, int(0.75*screensize[0]),int(0.6*screensize[1]))
        
        # 创建一个QWidget作为中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建一个垂直布局
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # 创建一个QLabel用于显示图像
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_label)
        
        # 创建一个按钮用于打开文件选择对话框
        self.load_button = QPushButton('打开图像')
        self.load_button.clicked.connect(self.load_image)
        layout.addWidget(self.load_button)
        
    def load_image(self):
        # 打开文件选择对话框
        file_name, _ = QFileDialog.getOpenFileName(self, "选择图像文件", "", "图像文件(*.png *.jpeg *.jpg *.gif *.bmp)")
        if file_name:
            self.setWindowTitle(f'imagebase-preview:{file_name}')
            # 使用QPixmap加载图像
            pixmap = QPixmap(file_name)
            # 更新QLabel显示图像
            self.image_label.setPixmap(pixmap)
            # 调整QLabel大小以适应screen大小
            '''self.image_label.resize(screensize)'''
            # 更新主窗口大小
            self.resize(self.image_label.size())

class NewDialog(QDialog):
    def __init__(self, parent=None):
        super(NewDialog, self).__init__(parent)
        self.Selfui()

    def Selfui(self):
        self.setWindowTitle('新界面')
        button = QPushButton('关闭')
        button.clicked.connect(self.accept)
        layout = QVBoxLayout()
        layout.addWidget(button)
        self.setLayout(layout)

class Eventsolver(QMainWindow):
    def __init__(self):
        super().__init__(self)
        self.SelfUI()
        
    def SelfUI(self):
        self.setWindowTitle(f'imagebase-{win.basename}')
        self.setGeometry (200,200, int(0.75*screensize[0]),int(0.6*screensize[1]))

def mainwindow01():
    app = QApplication(sys.argv)
    global win
    win = baseUI()
    win.show()
    sys.exit(app.exec_())

#读取settings.json, 恢复上一次的使用数据
mainwindow01()
