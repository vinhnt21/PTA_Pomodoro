import sys
from PyQt6 import QtWidgets, uic, QtCore
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import QUrl
import os


class PomodoroTimer(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Tải giao diện từ file UI
        uic.loadUi("pomodoro.ui", self)

        # Khởi tạo các biến ban đầu
        self.time_left = 25 * 60  # 25 phút được chuyển thành giây
        self.timer = QtCore.QTimer()  # Tạo đối tượng Timer để đếm thời gian
        self.timer.timeout.connect(
            self.update_timer
        )  # Kết nối timer với hàm update_timer
        self.is_work_time = True  # Biến đánh dấu đang trong thời gian làm việc
        self.is_running = False  # Biến đánh dấu timer đang chạy hay dừng

        # Thiết lập trình phát nhạc
        self.player = QMediaPlayer()  # Tạo đối tượng phát media
        self.audio_output = QAudioOutput()  # Tạo đối tượng xuất âm thanh
        self.player.setAudioOutput(self.audio_output)  # Kết nối player với audio output

        # Tải file nhạc nền
        self.player.setSource(QUrl.fromLocalFile(os.path.abspath("music.mp3")))
        self.audio_output.setVolume(0.5)  # Đặt âm lượng 50%

        # Kết nối các nút với các hàm xử lý tương ứng
        self.startButton.clicked.connect(self.start_stop_timer)
        self.resetButton.clicked.connect(self.reset_timer)
        self.musicCheckBox.stateChanged.connect(self.toggle_music)

        # Cập nhật hiển thị ban đầu
        self.update_display()

    def update_timer(self):
        """
        Hàm cập nhật thời gian mỗi giây
        Được gọi mỗi khi timer timeout (1 giây)
        """
        if self.time_left > 0:
            self.time_left -= 1  # Giảm thời gian còn lại
            self.update_display()  # Cập nhật hiển thị
        else:
            # Khi hết thời gian
            self.timer.stop()
            self.is_work_time = not self.is_work_time  # Đổi trạng thái làm việc/nghỉ

            if self.is_work_time:
                # Chuyển sang thời gian làm việc
                self.time_left = self.workTimeSpinBox.value() * 60
                QtWidgets.QMessageBox.information(
                    self, "Hết giờ nghỉ!", "Đến lúc làm việc!"
                )
            else:
                # Chuyển sang thời gian nghỉ
                self.time_left = self.breakTimeSpinBox.value() * 60
                QtWidgets.QMessageBox.information(
                    self, "Hết giờ làm việc!", "Đến lúc nghỉ ngơi!"
                )

            self.timer.start(1000)  # Khởi động lại timer
            self.update_display()

    def update_display(self):
        """
        Hàm cập nhật hiển thị thời gian lên giao diện
        Chuyển đổi giây thành định dạng phút:giây
        """
        minutes = self.time_left // 60
        seconds = self.time_left % 60
        self.timerLabel.setText(f"{minutes:02d}:{seconds:02d}")

    def start_stop_timer(self):
        """
        Hàm xử lý sự kiện khi nhấn nút Start/Stop
        Chuyển đổi giữa trạng thái chạy và dừng
        """
        if not self.is_running:
            # Nếu timer đang dừng thì start
            self.timer.start(1000)  # 1000ms = 1 giây
            self.startButton.setText("Stop")
            self.is_running = True
        else:
            # Nếu timer đang chạy thì stop
            self.timer.stop()
            self.startButton.setText("Start")
            self.is_running = False

    def reset_timer(self):
        """
        Hàm xử lý sự kiện khi nhấn nút Reset
        Đặt lại toàn bộ về trạng thái ban đầu
        """
        self.timer.stop()
        self.is_running = False
        self.is_work_time = True
        self.time_left = self.workTimeSpinBox.value() * 60
        self.startButton.setText("Start")
        self.update_display()

    def toggle_music(self, state):
        """
        Hàm xử lý sự kiện khi checkbox nhạc nền thay đổi trạng thái
        state: trạng thái của checkbox (đánh dấu/bỏ đánh dấu)
        """
        if state == QtCore.Qt.CheckState.Checked.value:
            self.player.play()  # Phát nhạc
        else:
            self.player.stop()  # Dừng nhạc


def main():
    """
    Hàm main khởi tạo ứng dụng
    """
    app = QtWidgets.QApplication(sys.argv)
    window = PomodoroTimer()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
