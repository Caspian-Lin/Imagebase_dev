from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
import sys, json, sqlite3, os, hashlib
from PIL import ImageGrab
from keras.applications.vgg16 import VGG16, preprocess_input
from keras.preprocessing import image
import numpy as np

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
        self.choosed_basefile_dir =-1
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
        self.base_list.cellClicked.connect(self.click_row_col)

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
        if  self.choosed_basefile_dir == -1:
            print("请选中一个数据库")
        else:
            self.baseMainwin = ImagebaseMain() #创建新窗口实例
            self.window_stack.append(self.baseMainwin)  # 将新窗口压入栈
            self.hide()
            self.baseMainwin.show()  # 显示新窗口
            
    
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
                self.window_stack[-1].show()

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
    
    def click_row_col(self, row, col):
        self.choosed_basefile_dir = self.base_content_list[row]["basefile_dir"]
        self.choosedbase_info =self.base_content_list[row]
        print(f"Clicked cell: Row {row}, Column {col}")

    def load_configJson(self):
        self.configJson=open("config.json","r")
        self.configdata=json.load(self.configJson)

    def load_base_content(self):
        #读取配置 还要重新加内容
        self.load_configJson()
        #返回现有库信息，[{:,:...},{:,:...}...]
        self.base_content_list=[]
        for i in self.configdata["base_content"]:
            self.base_content_list.append(self.configdata[i])
        return self.base_content_list 


class ImagebaseMain(QMainWindow):
    def __init__(self):
        super(ImagebaseMain, self).__init__()
        self.SelfUI()

    def SelfUI(self):  
        basename=win.choosedbase_info["baseName"]
        self.base_dir = win.choosedbase_info["basedir"]
        self.setWindowTitle(f'imagebase-{basename}')
        self.setGeometry (200,200, int(0.75*screensize[0]),int(0.6*screensize[1]))
        
        self.menubar_01()
        self.imagePrev_view()
        self.button_group()
        self.filetree_view()
        self.imglist_widget()
        self.img_propertyview()
        self.exsitingEventList_inbase()
        self.layout01()

    ###视图模块###

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

        self.button_baseRefresh = QPushButton(self)
        self.button_baseRefresh.setText("刷新库")
        self.button_baseRefresh.adjustSize()
        self.button_baseRefresh.clicked.connect(self.basedirRefresh)

    def filetree_view(self):
        model = QFileSystemModel()
        model.setRootPath(QDir.currentPath())
        self.filetree =  QTreeView()
        self.filetree.setModel(model)
        self.filetree.setRootIndex(model.index(QDir.currentPath()))

    def img_propertyview(self):
        self.img_propertyList = QTableWidget(1,1)
        for row in range(1):
            for col in range(1):
                item = QTableWidgetItem(str(self.imgquery[row][col]))
                self.img_list.setItem(row, col, item)
                
    def exsitingEventList_inbase(self):
        self.EventList = QTableWidget(1,1)
        for row in range(1):
            for col in range(1):
                item = QTableWidgetItem(str(self.imgquery[row][col]))
                self.img_list.setItem(row, col, item)

    def imglist_widget(self):
        # 执行查询
        self.conn = sqlite3.connect(win.choosed_basefile_dir)
        cursor = self.conn.cursor()
        cursor.execute('''SELECT * FROM main ''')
        self.imgquery=cursor.fetchall()
        # 创建列表模型并填充数据

        cursor.execute('''PRAGMA table_info(main)''')
        base_describe = cursor.fetchall()
        listcol  = [row[1] for row in base_describe]
        self.img_list = QTableWidget(len(self.imgquery),len(listcol))
        for row in range(len(self.imgquery)):
            for col in range(len(listcol)):
                item = QTableWidgetItem(str(self.imgquery[row][col]))
                self.img_list.setItem(row, col, item)
        self.img_list.setHorizontalHeaderLabels(listcol)
        # 设置tableWidget所有列的默认行高为20。
        self.img_list.verticalHeader().setDefaultSectionSize(20)
        # 设置tableWidget所有行的默认列宽为20
        self.img_list.horizontalHeader().setDefaultSectionSize(200)
        self.img_list.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        '''self.img_list.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.img_list.setSelectionMode(QAbstractItemView.SingleSelection)'''
        self.img_list.cellClicked.connect(self.imagePrev_show)

        self.img_list.setAcceptDrops(True)
    
    def layout01(self):
        # 布局
        widgetr = QWidget()
        layout2 =QVBoxLayout()
        layout2.addWidget(self.image_prev)
        layout2.addWidget(self.EventList)
        layout2.addWidget(self.img_propertyList)
        widgetr.setLayout(layout2)
        layout = QHBoxLayout()      
        layout.addWidget(self.filetree)
        layout.addWidget(self.img_list)
        layout.addWidget(widgetr)
        layout.addWidget(self.button_imgprev)
        layout.addWidget(self.button_baseRefresh)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    ###功能函数

    def imagePrev_show(self):
        #待施工
        pass
    
    def basedirRefresh(self):
        
        current_files_dir_list =[]
        for root,dirs,files in os.walk(self.base_dir):
            for file in files:
                current_files_dir_list.append(os.path.join(root, file))       
        
        old_files_dir_list = [f[2] for f in self.imgquery]
        # 比较list
        removed_files = set(old_files_dir_list).difference(set(current_files_dir_list))
        added_files = set(current_files_dir_list).difference(set(old_files_dir_list))
      
        if removed_files:
            print("检测到有以下图片不在目录下 是否从数据库中删除：", removed_files)
        if added_files:
            print("检测到以下图片新增在目录下 是否添加到目录中：", added_files)
            self.baseupdate(added_files)
        if False: # 两列表均为空
            print("无改变")

    def baseupdate(self,added_files):
        cursor = self.conn.cursor()
        for i in added_files:
            uselessvalue, file_extension = os.path.splitext(i)
            if file_extension not in [".jpg",".png"]:
                print("文件类型不受支持，跳过")
                continue
            filename = i.split('\\')[-1]

            md5_hash = hashlib.md5()
            with open(i, 'rb') as f:
                while chunk := f.read(8192):
                    md5_hash.update(chunk)
            md5_value = md5_hash.hexdigest()

            # 加载VGG16模型
            vgg16 = VGG16(weights='imagenet', include_top=True)
            # 提取特征
            img = image.load_img(i, target_size=(224, 224))
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = preprocess_input(img_array)
            features = vgg16.predict(img_array)

            # 存进SQL
            cursor.execute(f'''
                INSERT INTO main (hash,filename,filepath,feature) 
                        VALUES (?,?,?,?);''', (md5_value,filename,i,features))


        # 打印每一行
        cursor.execute("SELECT * FROM main")
        rows = cursor.fetchall()
        for row in rows:
            print(row)

        cursor.close()
        self.conn.commit()


    ###关闭当前窗口事件

    def closeEvent(self, event):
        # 在窗口关闭时触发的自定义函数
        win.close_current_window()
        print("ImagebaseMain_Window is closing.")

class ImagePreviewer(QMainWindow):
    def __init__(self):
        super(ImagePreviewer, self).__init__()
        self.ImagePreviewerUI()
    
    def ImagePreviewerUI(self):
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
        self.Eventname ="默认事件"
        
    def SelfUI(self):
        self.setWindowTitle(f'Eventsolver-{win.basename}-{self.Eventname}')
        self.setGeometry (200,200, int(0.75*screensize[0]),int(0.6*screensize[1]))

def mainwindow():
    app = QApplication(sys.argv)
    global win
    win = baseUI()
    win.window_stack.append(win)
    win.show()
    sys.exit(app.exec_())

#读取settings.json, 恢复上一次的使用数据
mainwindow()
