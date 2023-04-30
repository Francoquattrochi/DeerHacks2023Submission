from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QLineEdit, QTextEdit, QInputDialog, \
    QHBoxLayout, QVBoxLayout, QFormLayout, QFrame, QFileDialog
from PyQt5.QtGui import QPixmap, QClipboard, QImage
import openai
import requests
from PIL.ImageQt import ImageQt
from PIL.ImageFilter import SHARPEN
from PIL import Image
import os
class ClickablePixmapLabel(QLabel):
    def __init__(self, path, w, h, parent=None, name="PlaceHolder.png"):
        super().__init__(parent=parent)
        pixmap = QPixmap(path)
        pixmap.scaled(size2, Qt.KeepAspectRatio)
        # Set the pixmap for the label
        self.setPixmap(QPixmap(path))
        self.name = name

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Perform your action here
            newPixmap = QPixmap(self.pixmap())
            newPixmap = newPixmap.scaled(size2, Qt.KeepAspectRatio)
            preview_image.setPixmap(newPixmap)
            mainToPreview()
            global filename
            filename = self.name+".jpg"

class ImageProcessor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = "Modified/"

    def loadImage(self, filename):
        '''When loading, remember the path and file name'''
        self.filename = filename
        fullname = os.path.join(workdir, filename)
        self.image = Image.open(fullname)

    def saveImage(self):
        '''saves a copy of the file in a sub-folder'''
        path = os.path.join(workdir, self.save_dir)
        if not (os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        fullname = os.path.join(path, self.filename)

        self.image.save(fullname)

    def do_bw(self):
        self.image = self.image.convert("L")
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_sharpen(self):
        self.image = self.image.filter(SHARPEN)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def showImage(self, path):
        lb_image.hide()
        pixmapimage = QPixmap(path)
        pixmapimage.scaled(256, 256)
        editing_image.setPixmap(pixmapimage)

    def do_save(self):
        preview_image.setPixmap(editing_image.pixmap())
        editToPreview()




openai.api_key = "ENTER API KEY HERE"
app = QApplication([])
window = QWidget()
window.resize(600, 700)
workdir = "TempImages/"
userPath = ""
filename = ""
size1 = QSize(150, 150)
size2 = QSize(500, 500)
size3 = QSize(259, 194)
with open('styles.qss', 'r') as f:
    style = f.read()
    app.setStyleSheet(style)

imageLabels = []
# Main Menu
title = QLabel("Image Creator")
generate_btn = QPushButton("Generate")
addPrompt_btn = QPushButton("Add Prompt")
deletePrompt_btn = QPushButton("Delete Prompt")
clear_btn = QPushButton("Clear")
promptLabel = QLabel("Prompt:")
promptField = QLineEdit()
promptField.setPlaceholderText("Enter Prompt Here")
promptList = QListWidget()
allPrompts = []
main_layout = QVBoxLayout()
v1 = QVBoxLayout()
v1.addWidget(title, alignment=Qt.AlignHCenter)
v2 = QVBoxLayout()

v2.addWidget(addPrompt_btn)
v2.addWidget(deletePrompt_btn)
v2.addWidget(clear_btn)

v2.addWidget(promptField)

v4 = QVBoxLayout()
v4.addWidget(generate_btn)
v4.addWidget(promptList)

h1 = QHBoxLayout()
h1.addLayout(v2)
h1.addLayout(v4)

v1.addLayout(h1)

for i in range(2):
    h2 = QHBoxLayout()
    for j in range(3):
        lb_image = ClickablePixmapLabel("Images/PlaceHolder.png", 150, 150)
        lb_image.show()
        h2.addWidget(lb_image)
        imageLabels.append(lb_image)
    v1.addLayout(h2)
main_frame = QFrame()
main_frame.setLayout(v1)

main_layout.addWidget(main_frame)

window.setLayout(main_layout)
# Button Cursors
generate_btn.setCursor(Qt.PointingHandCursor)
addPrompt_btn.setCursor(Qt.PointingHandCursor)
deletePrompt_btn.setCursor(Qt.PointingHandCursor)
clear_btn.setCursor(Qt.PointingHandCursor)
# END MAIN MENU

# START PREVIEW MENU
preview_title = QLabel("Image Preview")
preview_image = QLabel("Image")
preview_download_btn = QPushButton("Download")
preview_edit_btn = QPushButton("Edit")
preview_copy_btn = QPushButton("Copy")
preview_return_btn = QPushButton("Return")



preview_h1 = QHBoxLayout()
preview_h1.addWidget(preview_return_btn)
preview_h1.addWidget(preview_title, alignment=Qt.AlignHCenter, stretch=4)
preview_h2 = QHBoxLayout()
preview_h2.addWidget(preview_download_btn)
preview_h2.addWidget(preview_edit_btn)
preview_h2.addWidget(preview_copy_btn)
preview_layout = QVBoxLayout()
preview_layout.addLayout(preview_h1)
preview_layout.addWidget(preview_image, alignment=Qt.AlignHCenter)
preview_layout.addLayout(preview_h2)
preview_frame = QFrame()
preview_frame.setLayout(preview_layout)
preview_frame.hide()
main_layout.addWidget(preview_frame)
#END PREVIEW MENU

#START EDITING MENU
editing_title = QLabel("Image Editor")
editing_return = QPushButton("Return")
editing_action1 = QPushButton("Left")
editing_action2 = QPushButton("B/W")
editing_action3 = QPushButton("Flip")
editing_action4 = QPushButton("Right")
editing_action5 = QPushButton("Sharpen")
editing_action6 = QPushButton("Save")
editing_image = QLabel("Image")
editing_h1 = QHBoxLayout()
editing_h1.addWidget(editing_return)
editing_h1.addWidget(editing_title, alignment=Qt.AlignHCenter, stretch=4)
editing_v1 = QVBoxLayout()
editing_v1.addWidget(editing_action1)
editing_v1.addWidget(editing_action2)
editing_v1.addWidget(editing_action3)
editing_v2 = QVBoxLayout()
editing_v2.addWidget(editing_action4)
editing_v2.addWidget(editing_action5)
editing_v2.addWidget(editing_action6)
editing_h2 = QHBoxLayout()
editing_h2.addLayout(editing_v1)
editing_h2.addLayout(editing_v2)
editing_h2.addWidget(editing_image, alignment=Qt.AlignRight,stretch=4)

editing_v3 = QVBoxLayout()
editing_v3.addLayout(editing_h1)
editing_v3.addLayout(editing_h2, stretch=3)
editing_frame = QFrame()
editing_frame.setLayout(editing_v3)
editing_frame.hide()
main_layout.addWidget(editing_frame)
#END EDITING MENU
imageEditor = ImageProcessor()
def addPrompt():
    if promptField.text() != "":
        promptList.addItem(promptField.text())
        allPrompts.append(promptField.text())
        promptField.clear()


def deletePrompt():
    try:
        selected_item = promptList.selectedItems()[0].text()
        promptList.clear()
        allPrompts.remove(selected_item)
        promptList.addItems(allPrompts)
    except:
        promptField.clear()
        promptField.setPlaceholderText("Click on prompt to delete")


def clear():
    promptList.clear()
    allPrompts.clear()


def generateImages():
    response = openai.Image.create(
        prompt=" ".join(allPrompts),
        n=6,
        size="256x256"
    )

    for i in range(6):
        image_url = response['data'][i]['url']
        img_data = requests.get(image_url).content
        path = "TempImages/" + "".join(allPrompts) + "(" + str(i + 1) + ")" + ".jpg"
        with open(path, 'wb') as handler:
            handler.write(img_data)
        pixmapimage = QPixmap(path)

        pixmapimage = pixmapimage.scaled(size3)
        imageLabels[i].setPixmap(pixmapimage)
        imageLabels[i].name = "".join(allPrompts) + "(" + str(i + 1) + ")"


def setDownloadDirectory():
    global userPath
    userPath = QFileDialog.getExistingDirectory()


def downloadImage():
    setDownloadDirectory()
    path = userPath + "/" + filename
    print(path)
    preview_image.pixmap().save(path, "JPEG")
    print("Image Saved To: " + path)


def copyImage():
    clipboard = app.clipboard()
    clipboard.setPixmap(preview_image.pixmap(), mode=clipboard.Clipboard)


def mainToPreview():

    main_frame.hide()
    preview_frame.show()


def previewToMain():
    preview_frame.hide()
    main_frame.show()
    for lb in imageLabels:
        lb.show()
    v1.update()

def previewToEdit():
    preview_frame.hide()
    editing_frame.show()
    editing_image.setPixmap(preview_image.pixmap())
    path = "TempImages/"+filename
    preview_image.pixmap().save(path, "JPEG")
    imageEditor.loadImage(filename)
    imageEditor.showImage(os.path.join(workdir, imageEditor.filename))

def editToPreview():
    editing_frame.hide()
    preview_frame.show()



# Event Subscriptions
promptField.returnPressed.connect(addPrompt)
addPrompt_btn.clicked.connect(addPrompt)
deletePrompt_btn.clicked.connect(deletePrompt)
clear_btn.clicked.connect(clear)
generate_btn.clicked.connect(generateImages)

preview_return_btn.clicked.connect(previewToMain)
preview_download_btn.clicked.connect(downloadImage)
preview_copy_btn.clicked.connect(copyImage)
preview_edit_btn.clicked.connect(previewToEdit)

editing_return.clicked.connect(editToPreview)
editing_action1.clicked.connect(imageEditor.do_left)
editing_action4.clicked.connect(imageEditor.do_right)
editing_action2.clicked.connect(imageEditor.do_bw)
editing_action5.clicked.connect(imageEditor.do_sharpen)
editing_action3.clicked.connect(imageEditor.do_flip)
editing_action6.clicked.connect(imageEditor.do_save)

window.show()
app.exec_()
