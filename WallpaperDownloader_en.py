import sys
import os
import re
import subprocess
import threading
import base64
import json

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QPushButton, QTextEdit, QFileDialog, QComboBox,
    QListWidget, QProgressBar
)
from PyQt6.QtCore import Qt, pyqtSignal


accounts = {
    'ruiiixx': 'UzY3R0JUQjgzRDNZ',
    'premexilmenledgconis': 'M3BYYkhaSmxEYg==',
    'vAbuDy': 'Qm9vbHE4dmlw',
    'adgjl1182': 'UUVUVU85OTk5OQ==',
    'gobjj16182': 'enVvYmlhbzgyMjI=',
    '787109690': 'SHVjVXhZTVFpZzE1'
}

passwords = {
    acc: base64.b64decode(accounts[acc]).decode('utf-8')
    for acc in accounts
}


CONFIG_FILE = "config.json"


def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}


def save_config(data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=4)


class App(QWidget):
    update_queue_signal = pyqtSignal(int, str)
    update_progress_signal = pyqtSignal(int)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Wallpaper Downloader")
        self.setFixedSize(600, 600)

        layout = QVBoxLayout()

        title = QLabel("Wallpaper Downloader")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: bold;")
        layout.addWidget(title)

        acc_label = QLabel("Select Steam Account")
        layout.addWidget(acc_label)

        self.account = QComboBox()
        self.account.addItems(accounts.keys())
        layout.addWidget(self.account)

        self.path_btn = QPushButton("Select Wallpaper Engine Folder")
        self.path_btn.clicked.connect(self.select_path)
        layout.addWidget(self.path_btn)

        self.path_label = QLabel("No path selected")
        layout.addWidget(self.path_label)

        self.links = QTextEdit()
        self.links.setPlaceholderText("Paste workshop links or IDs...")
        layout.addWidget(self.links)

        self.queue = QListWidget()
        layout.addWidget(self.queue)

        self.progress = QProgressBar()
        self.progress.setValue(0)
        layout.addWidget(self.progress)

        self.download_btn = QPushButton("Start Download")
        self.download_btn.clicked.connect(self.start_thread)
        layout.addWidget(self.download_btn)

        self.setLayout(layout)

        self.save_path = ""

        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: white;
                font-family: Segoe UI;
            }

            QPushButton {
                background-color: #2d2d2d;
                border: none;
                padding: 8px;
            }

            QPushButton:hover {
                background-color: #3a3a3a;
            }

            QTextEdit, QListWidget {
                background-color: #121212;
                border: 1px solid #2d2d2d;
            }

            QComboBox {
                background-color: #2d2d2d;
                padding: 5px;
            }
        """)

        self.config = load_config()

        if "save_path" in self.config:
            self.save_path = self.config["save_path"]
            self.path_label.setText(self.save_path)

        # connect signals
        self.update_queue_signal.connect(self.update_queue)
        self.update_progress_signal.connect(self.progress.setValue)

    def update_queue(self, index, text):
        self.queue.item(index).setText(text)

    def select_path(self):
        folder = QFileDialog.getExistingDirectory()
        if folder:
            self.save_path = folder
            self.path_label.setText(folder)

            self.config["save_path"] = folder
            save_config(self.config)

    def run_download(self, pubfileid, index):
        exe = os.path.join("DepotdownloaderMod", "DepotDownloadermod.exe")

        target_folder = os.path.join(self.save_path, "projects", "myprojects")
        os.makedirs(target_folder, exist_ok=True)

        out = os.path.join(target_folder, pubfileid)

        command = [
            exe,
            "-app", "431960",
            "-pubfile", pubfileid,
            "-username", self.account.currentText(),
            "-password", passwords[self.account.currentText()],
            "-dir", out
        ]

        self.update_queue_signal.emit(index, f"Downloading: {pubfileid}")

        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )

            for line in process.stdout:
                match = re.search(r'(\d+)%', line)
                if match:
                    self.update_progress_signal.emit(int(match.group(1)))

            process.wait()

            self.update_queue_signal.emit(index, f"Done: {pubfileid}")
            self.update_progress_signal.emit(100)

        except:
            self.update_queue_signal.emit(index, f"Failed: {pubfileid}")
            self.update_progress_signal.emit(0)

    def start_thread(self):
        threading.Thread(target=self.process, daemon=True).start()

    def process(self):
        self.queue.clear()
        self.update_progress_signal.emit(0)

        lines = self.links.toPlainText().splitlines()
        ids = []

        for line in lines:
            match = re.search(r'\d{8,10}', line)
            if match:
                ids.append(match.group(0))
                self.queue.addItem(f"Queued: {match.group(0)}")

        for i, id in enumerate(ids):
            self.run_download(id, i)


app = QApplication(sys.argv)
window = App()
window.show()
sys.exit(app.exec())
