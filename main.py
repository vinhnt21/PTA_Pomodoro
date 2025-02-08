import sys
from PyQt6 import QtWidgets, uic, QtCore
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import QUrl
import os


class PomodoroTimer(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Load UI
        uic.loadUi("pomodoro.ui", self)

        # Initialize variables
        self.time_left = 25 * 60  # 25 minutes in seconds
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.is_work_time = True
        self.is_running = False

        # Setup media player
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)

        # Load background music
        self.player.setSource(QUrl.fromLocalFile(os.path.abspath("music.mp3")))
        self.audio_output.setVolume(0.5)

        # Connect buttons
        self.startButton.clicked.connect(self.start_stop_timer)
        self.resetButton.clicked.connect(self.reset_timer)
        self.musicCheckBox.stateChanged.connect(self.toggle_music)

        # Update initial display
        self.update_display()

    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.update_display()
        else:
            self.timer.stop()
            self.is_work_time = not self.is_work_time

            if self.is_work_time:
                self.time_left = self.workTimeSpinBox.value() * 60
                QtWidgets.QMessageBox.information(self, "Break Over!", "Time to work!")
            else:
                self.time_left = self.breakTimeSpinBox.value() * 60
                QtWidgets.QMessageBox.information(
                    self, "Work Over!", "Time for a break!"
                )

            self.timer.start(1000)
            self.update_display()

    def update_display(self):
        minutes = self.time_left // 60
        seconds = self.time_left % 60
        self.timerLabel.setText(f"{minutes:02d}:{seconds:02d}")

    def start_stop_timer(self):
        if not self.is_running:
            self.timer.start(1000)
            self.startButton.setText("Stop")
            self.is_running = True
        else:
            self.timer.stop()
            self.startButton.setText("Start")
            self.is_running = False

    def reset_timer(self):
        self.timer.stop()
        self.is_running = False
        self.is_work_time = True
        self.time_left = self.workTimeSpinBox.value() * 60
        self.startButton.setText("Start")
        self.update_display()

    def toggle_music(self, state):
        if state == QtCore.Qt.CheckState.Checked.value:
            self.player.play()
        else:
            self.player.stop()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = PomodoroTimer()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

# Created/Modified files during execution:
# - pomodoro.ui
# - main.py
