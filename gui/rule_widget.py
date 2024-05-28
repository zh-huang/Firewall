from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QInputDialog, QMessageBox
from backend import IptablesManager
import subprocess

class RuleWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.iptablesManager = IptablesManager()
        self.load_rules()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        self.button_layout = QHBoxLayout()

        self.add_button = QPushButton('Add Rule')
        self.add_button.clicked.connect(self.add_rule)
        self.button_layout.addWidget(self.add_button)

        self.delete_button = QPushButton('Delete Rule')
        self.delete_button.clicked.connect(self.delete_rule)
        self.button_layout.addWidget(self.delete_button)

        self.save_button = QPushButton('Save Rules')
        self.save_button.clicked.connect(self.save_rules)
        self.button_layout.addWidget(self.save_button)

        self.layout.addLayout(self.button_layout)
        self.setLayout(self.layout)

    def load_rules(self):
        self.table.clear()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(['Chain', 'Target', 'Prot', 'Opt', 'Source', 'Destination', 'Ext', 'Ext2'])
        rules = self.iptablesManager.get_iptables_rules()
        self.table.setRowCount(len(rules))
        for i, rule in enumerate(rules):
            for j, col in enumerate(rule):
                self.table.setItem(i, j, QTableWidgetItem(col))

    def add_rule(self):
        rule, ok = QInputDialog.getText(self, 'Add Rule', 'Enter rule:')
        if ok and rule:
            try:
                self.iptablesManager.add_rule(rule)
                self.load_rules()
            except subprocess.CalledProcessError as e:
                QMessageBox.warning(self, 'Error', f'Failed to add rule: {e}')

    def delete_rule(self):
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.warning(self, 'Error', 'Please select a rule to delete')
            return

        chain = self.table.item(row, 0).text()
        target = self.table.item(row, 1).text()
        prot = self.table.item(row, 2).text()
        source = self.table.item(row, 4).text()
        destination = self.table.item(row, 5).text()
        ext = self.table.item(row, 7).text()
        try:
            self.iptablesManager.delete_rule(chain, target, prot, source, destination, ext)
            self.load_rules()
        except subprocess.CalledProcessError as e:
            QMessageBox.warning(self, 'Error', f'Failed to delete rule: {e}')

    def save_rules(self):
        self.iptablesManager.save_rules()
        QMessageBox.information(self, 'Success', 'Rules saved to iptables_rules.txt')
