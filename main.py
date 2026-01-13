from grover_simulator import GroverSimulator

#g = GroverSimulator(3, 2, 1)

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer, Qt, QElapsedTimer

from qt import MyWindow

class GameController:
    def __init__(self, window):
        self.window = window
        self.keys = set()
        self.speed = 5

        self.timer = QElapsedTimer()
        self.timer.start()

        self.last_time = self.timer.elapsed()  # ms

        #grover simulator
        self.qubit_count = 3
        self.solutions = 2
        self.iterations = 1
        self.grover = GroverSimulator(self.qubit_count, self.solutions, self.iterations)
        self.window.set_simulator(self.grover)

        #results
        self.results = [0, 0]
        self.window.set_results(self.results)

        #controlling simulation
        self.should_run = False
        self.shots = 0

    def key_press(self, key):
        self.keys.add(key)

    def key_release(self, key):
        self.keys.discard(key)

    def update(self):
        current_time = self.timer.elapsed()
        delta_ms = current_time - self.last_time
        self.last_time = current_time

        delta_time = delta_ms / 1000.0  # seconds

        updated = False
        if Qt.Key.Key_W in self.keys:
            updated = True
            self.qubit_count += 1
        if Qt.Key.Key_S in self.keys:
            if (self.qubit_count > 2):
                updated = True
                self.qubit_count -= 1

        if Qt.Key.Key_A in self.keys:
            updated = True
            self.solutions += 1
        if Qt.Key.Key_D in self.keys:
            if (self.solutions > 1):
                updated = True
                self.solutions -= 1
        
        if Qt.Key.Key_Z in self.keys:
            updated = True
            self.iterations += 1
        if Qt.Key.Key_X in self.keys:
            if (self.iterations > 1):
                updated = True
                self.iterations -= 1
        
        self.should_run = False
        if Qt.Key.Key_T in self.keys:
            self.should_run = True
        
        if (updated):
            self.grover = GroverSimulator(self.qubit_count, self.solutions, self.iterations)
            self.window.set_simulator(self.grover)
            self.results = [0, 0]
        '''if Qt.Key.Key_S in self.keys:
            self.window.y += self.speed
        if Qt.Key.Key_A in self.keys:
            self.window.x -= self.speed
        if Qt.Key.Key_D in self.keys:
            self.window.x += self.speed'''

        if self.should_run:
            val = self.grover.run()
            for x in val.keys():
                print(f"{str(x)[::-1]}, {self.grover.solution_list}")
                print(val)
                if str(x)[::-1] in self.grover.solution_list:
                    self.results[1] += 1
                else:
                    self.results[0] += 1
            
            print(self.results)

        
        self.window.set_simulator(self.grover)
        self.window.set_results(self.results)

        self.window.update()

def main():
    app = QApplication(sys.argv)

    window = MyWindow()
    window.setWindowTitle("GroverSimulator")
    window.setGeometry(100, 100, 960, 540)
    window.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
    window.show()

    controller = GameController(window)

    # Inject input handlers
    window.keyPressEvent = lambda e: controller.key_press(e.key())
    window.keyReleaseEvent = lambda e: controller.key_release(e.key())

    # Main loop
    timer = QTimer()
    timer.timeout.connect(controller.update)
    timer.start(16)  # ~60 FPS

    sys.exit(app.exec())

if __name__ == "__main__":
    main()