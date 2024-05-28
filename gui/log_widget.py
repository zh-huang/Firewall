import sys
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTextEdit, QWidget, QPushButton, QHBoxLayout
from scapy.all import sniff
import threading


class PacketLogger(QObject):
    packet_received = pyqtSignal(str)


class LogWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        self.sniffing = False
        self.sniff_thread = None
        self.packet_logger = PacketLogger()
        self.packet_logger.packet_received.connect(self.log_packet)
        
        self.initUI()
        self.start_sniffing()
    
    def initUI(self):
        layout = QVBoxLayout()
        self.textEdit = QTextEdit()
        layout.addWidget(self.textEdit)
        
        button_layout = QHBoxLayout()
        self.start_button = QPushButton('Start')
        self.start_button.clicked.connect(self.start_sniffing)
        button_layout.addWidget(self.start_button)
        
        self.stop_button = QPushButton('Stop')
        self.stop_button.clicked.connect(self.stop_sniffing)
        self.start_button.setEnabled(False)
        button_layout.addWidget(self.stop_button)
        
        self.clear_button = QPushButton('Clear')
        self.clear_button.clicked.connect(self.clear_log)
        button_layout.addWidget(self.clear_button)

        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
    def log_packet(self, log_entry):
        self.textEdit.append(log_entry)
    
    def clear_log(self):
        self.textEdit.clear()

    def start_sniffing(self):
        if not self.sniffing:
            self.sniffing = True
            self.sniff_thread = threading.Thread(target=self.sniff_packets)
            self.sniff_thread.start()
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)

    def stop_sniffing(self):
        if self.sniffing:
            self.sniffing = False
            self.sniff_thread.join()
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)

    def sniff_packets(self):
        sniff(prn=lambda x: self.packet_logger.packet_received.emit(x.summary()), store=0, stop_filter=lambda x: not self.sniffing)
