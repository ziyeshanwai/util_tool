from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtOpenGL import QGLWidget
import sys
from OpenGL.GL import *
 
class MainWindow(QMainWindow):
	"""docstring for Mainwindow"""
	def __init__(self, parent = None):
		super(MainWindow,self).__init__(parent)
		self.basic()
		splitter_main = self.split_()
		self.setCentralWidget(splitter_main)
 
	#窗口基础属性
	def basic(self):
		#设置标题，大小，图标
		self.setWindowTitle("GT")
		self.resize(1100,650)
		self.setWindowIcon(QIcon("./image/Gt.png"))
		#居中显示
		screen = QDesktopWidget().geometry()
		self_size = self.geometry()
		self.move((screen.width() - self_size.width())/2,(screen.height() - self_size.height())/2)
 
	#分割窗口
	def split_(self):
		splitter = QSplitter(Qt.Vertical)
		s = OpenGLWidget()   #将opengl例子嵌入GUI
		splitter.addWidget(s)
		testedit = QTextEdit()
		splitter.addWidget(testedit)
		splitter.setStretchFactor(0,3)
		splitter.setStretchFactor(1,2)
		splitter_main = QSplitter(Qt.Horizontal)
		textedit_main = QTextEdit()
		splitter_main.addWidget(textedit_main)
		splitter_main.addWidget(splitter)
		splitter_main.setStretchFactor(0,1)
		splitter_main.setStretchFactor(1,4)
		return splitter_main
 
class OpenGLWidget(QGLWidget):
	def initializeGL(self):
		glClearColor(1,0,0,1)
		glEnable(GL_DEPTH_TEST)
		glEnable(GL_LIGHT0)
		glEnable(GL_LIGHTING)
		glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
		glEnable(GL_COLOR_MATERIAL)
 
	def paintGL(self):
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		glBegin(GL_TRIANGLES)
		glColor3f(1.0, 0.0, 0.0)
		glVertex3f(-0.5, -0.5, 0)
		glColor3f(0.0, 1.0, 0.0)
		glVertex3f( 0.5, -0.5, 0)
		glColor3f(0.0, 0.0, 1.0)
		glVertex3f( 0.0,  0.5, 0)
		glEnd()
 
 
if __name__ == "__main__":
	app = QApplication(sys.argv)
	win = MainWindow()
	win.show()
	sys.exit(app.exec_())
