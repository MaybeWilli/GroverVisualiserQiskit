from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtGui import QPainter, QColor, QPen, QFont
import sys
from PyQt6.QtCore import Qt
import math
import time
from grover_simulator import GroverSimulator


class MyWindow(QWidget):
    def __init__(self):
        print("Huh")
        self.label = "Hello world"
        super().__init__()

    def paintEvent(self, event):
        painter = QPainter(self)

        self.draw_probability(painter)
        self.draw_instructions(painter)
        self.display_stats(painter)

    def draw_probability(self, painter):
        # Make it hollow by removing the brush (no fill)
        painter.setBrush(Qt.BrushStyle.NoBrush)

        # Set the pen for the outline (color and thickness)
        pen = QPen(Qt.GlobalColor.black)
        pen.setWidth(4)  # Thickness of the circle outline
        painter.setPen(pen)

        # Draw a circle at (x=100, y=100) with radius 50
        x = 100
        y = 100
        radius = 150
        painter.drawEllipse(x, y, radius*2, radius*2)

        #Label circle
        font = QFont("Arial", 20)  # Font family and size
        painter.setFont(font)
        painter.setPen(QColor(50, 100, 200))  # RGB color
        painter.drawText(200, 90, "Solutions")
        painter.setPen(QColor(200, 100, 50))
        painter.drawText(410, 250, "Non-Solutions")
        self.draw_dot(painter, QColor(50, 100, 200), 0)
        self.draw_dot(painter, QColor(200, 100, 50), -3.14/2)
        
        #draw dotted line and expected probability
        self.draw_angle(painter, QColor(50, 100, 200), 
            -math.atan2(abs(math.sin(self.grover.get_angle())), abs(math.cos(self.grover.get_angle()))), True)
        self.draw_angle(painter, QColor(50, 100, 200), -self.grover.get_angle())



        self.display_results(painter)
    
    def draw_angle(self, painter, color, radians, isDotted=False):
        pen = QPen(color)
        pen.setWidth(3)
        if (isDotted):
            pen.setWidth(2)
            pen.setStyle(Qt.PenStyle.DotLine)
        
        painter.setPen(pen)

        center_x = 250
        center_y = 250

        x = center_x + 150 * math.cos(radians)
        y = center_y + 150 * math.sin(radians)

        painter.drawLine(int(center_x) , int(center_y), int(x), int(y))
    
    def draw_instructions(self, painter):
        font = QFont("Arial", 20)  # Font family and size
        painter.setFont(font)
        painter.setPen(QColor(100, 100, 100))  # RGB color
        painter.drawText(550, 300, "Controls:")
        painter.drawText(550, 325, "W: Increase qubit count")
        painter.drawText(550, 350, "S: Decrease qubit count")
        painter.drawText(550, 375, "A: Increase solution count")
        painter.drawText(550, 400, "D: Decrease solution count")
        painter.drawText(550, 425, "Z: Increase iterations")
        painter.drawText(550, 450, "X: Decrease iterations")
        painter.drawText(550, 475, "T: Start/stop")
    
    def display_stats(self, painter):
        font = QFont("Arial", 20)  # Font family and size
        painter.setFont(font)
        painter.setPen(QColor(50, 200, 50))  # RGB color
        painter.drawText(550, 100, "Current simulation stats:")
        painter.drawText(550, 125, f"Number of qubits: {self.grover.qubit_count}")
        painter.drawText(550, 150, f"Number of items: {math.pow(2, self.grover.qubit_count)}")
        painter.drawText(550, 175, f"Number of solutions: {self.grover.solution_count}")
        painter.drawText(550, 200, f"Number of iterations: {self.grover.iterations}")
    
    def display_results(self, painter):
        if (self.results[0]+self.results[1] != 0):
            y = math.sqrt(self.results[1]/(self.results[0]+self.results[1]))
            x = math.sqrt(self.results[0]/(self.results[0]+self.results[1]))

            radian = math.atan2(y, x)
            self.draw_angle(painter, QColor(50, 200, 50), -radian)

            font = QFont("Arial", 20)  # Font family and size
            painter.setFont(font)
            painter.setPen(QColor(50, 200, 50))  # RGB color
            painter.drawText(100, 450, f"Solutions: {self.results[1]}")
            painter.drawText(100, 475, f"Non-solutions: {self.results[0]}")
    
    def main_loop(self):
        print("Hello loop")
    
    def draw_dot(self, painter, color, radians):
        center_x = 250
        center_y = 250

        x = center_x + 150 * math.cos(radians)
        y = center_y + 150 * math.sin(radians)

        dot_radius = 5
        painter.setBrush(color)
        painter.drawEllipse(int(x - dot_radius),
                            int(y - dot_radius),
                            dot_radius*2,
                            dot_radius*2)
    
    def set_simulator(self, grover):
        self.grover = grover
    
    def set_results(self, results):
        self.results = results



'''app = QApplication(sys.argv)
window = MyWindow()
window.setWindowTitle("Drawing in PyQt6")
window.setGeometry(100, 100, 960, 540)
window.show()
sys.exit(app.exec())

time.sleep(3)

window.label = "What the"
window.update()'''