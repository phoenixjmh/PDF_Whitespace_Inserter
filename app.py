import cv2
import numpy as np
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QGraphicsScene,
    QGraphicsView,
    QVBoxLayout,
    QWidget,
)
from PyQt5.QtGui import QCloseEvent, QImage, QKeyEvent, QPixmap, QResizeEvent
from PyQt5.QtCore import Qt, QEvent


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("PyQt Image Viewer")
        self.setGeometry(100, 100, 800, 600)

        self.image = cv2.imread("res/input.png")
        self.original_image = self.image.copy()

        self.graphics_view = QGraphicsView()
        self.scene = QGraphicsScene()
        self.graphics_view.setScene(self.scene)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.graphics_view)

        self.container = QWidget()
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)

        self.update_image(self.image)

        self.graphics_view.setMouseTracking(True)
        self.graphics_view.viewport().installEventFilter(self)

        self.start_y = 0
        self.clicked = False
    def saveOutputImage(self,event):
        cv2.imwrite('output.png',self.image)

    def keyPressEvent(self,event):
        
        if(event.text().lower()=='s'):
            self.saveOutputImage(self)

    def resizeEvent(self,event): 
        self.update_image(self.image)

    def closeEvent(self,event):
        self.saveOutputImage(self)
        
    def update_image(self, image):
        global scale_factor
        height, width, channel = image.shape
        bytes_per_line = 3 * width
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        scale_factor = self.graphics_view.width() / width
        image = cv2.resize(
            image, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_AREA
        )
        height, width, channel = image.shape
        bytes_per_line = 3 * width

        q_img = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_img)
        self.scene.clear()
        self.scene.addPixmap(pixmap)
        self.graphics_view.setScene(self.scene)
        print(scale_factor, "Scale factor")
        # self.graphics_view.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)

    def insert_whitespace(self, image, click_y, space_height):
        content_below_height = image.shape[0] - click_y
        height, width = image.shape[:2]
        new_height = height + space_height
        resized_image = np.zeros((new_height, width, 3), dtype=np.uint8)
        resized_image[:click_y] = image[:click_y]
        resized_image[click_y + space_height :] = image[click_y:]
        resized_image[click_y : click_y + space_height, :] = 255  # White color
        return resized_image

    def eventFilter(self, source, event):
        global scale_factor,amount_inserted
        if (
            event.type() == QEvent.Type.MouseButtonPress
            and event.buttons() == Qt.LeftButton
            and source is self.graphics_view.viewport()
        ):
            self.clicked = True
            print(event.pos(), "raw event pos")
            refpos = event.pos()
            scene_pos = self.graphics_view.mapToScene(event.pos())
            self.start_y = int(
                scene_pos.y() * self.image.shape[0] / self.scene.height()
            )
            screen_to_viewport = refpos.y() / self.start_y
            # print(self.start_y,"Scene position")
            print(screen_to_viewport, "Screen to viewport")
            return True
        elif( event.type()==QEvent.Type.MouseButtonRelease):
            amount_inserted=0
            return True

        elif (
            event.type() == QEvent.Type.MouseMove
            and event.buttons() == Qt.LeftButton
            and source is self.graphics_view.viewport()
        ):
           
            scene_pos = self.graphics_view.mapToScene(event.pos())
            end_y = int(scene_pos.y()* self.image.shape[0]/self.scene.height())
            print("Local Start",self.start_y,"Local End",end_y,"Event Y",event.pos().y())


            space_height = int((end_y-self.start_y) )
            delta=space_height-amount_inserted
            if delta<0:
                delta=0
            print(delta,"Delta",amount_inserted,"Amount Inserted")
            self.image = self.insert_whitespace(
                self.original_image.copy(), self.start_y, delta
            )
            self.original_image = self.image.copy()
            self.update_image(self.image)
            # restart loop?
            amount_inserted+=delta
            
            return True

        
        return super(MainWindow, self).eventFilter(source, event)


if __name__ == "__main__":
    scale_factor = 1
    amount_inserted=0
    import sys
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
