from PyQt5 import QtCore, uic, QtWidgets
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem, QCheckBox
import sys
from random import random

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)

        self.init_UI()
        self.init_Data()
        
    def init_UI(self):
        self.risk_analysys_table.setColumnWidth(0, 370)
        for i in range(1, 11):
            self.risk_analysys_table.setColumnWidth(i, 20)

        self.calculateRiskProbability.clicked.connect(self.risk_probability)
        self.calculateEventProbability.clicked.connect(self.event_probability)
        self.actionMain_menu.triggered.connect(self.back)
        self.generate_marks_button.clicked.connect(self.generate)
        self.event_analysys_button.clicked.connect(self.event_analysys)
        self.group_result_button.clicked.connect(self.group_result)
        self.generate_loss_button.clicked.connect(self.generate_loss)
        self.calculate_vrer_button.clicked.connect(self.calculate_vrer)
        self.risk_priority_button.clicked.connect(self.risk_priority)

    def generate(self):
        for i in range(1, 47):
            for j in range(1, 11):
                self.risk_analysys_table.setItem(i-1, j, QTableWidgetItem(str(round(random(), 2))))
    
    def generate_loss(self):
        for i in range(1, 47):
            value = round(random(), 2)
            self.loss.append(value)
            self.vrer_table.setItem(i-1, 2, QTableWidgetItem(str(value)))

    def risk_priority(self):
        min_vrer = min(self.vrer)
        max_vrer = max(self.vrer)
        self.min_vrer_box.setText(str(min_vrer))
        self.max_vrer_box.setText(str(max_vrer))
        step = round((max_vrer - min_vrer) / 3, 2)
        low_priority_limit = round(min_vrer + step, 2)
        middle_priority_limit = round(max_vrer - step, 2)
        self.low_interval_box.setText(f"[{min_vrer}; {low_priority_limit})")
        self.middle_interval_box.setText(f"[{low_priority_limit}; {middle_priority_limit})")
        self.high_interval_box.setText(f"[{low_priority_limit}; {max_vrer}]")

        for i in range(1, 47):
            if self.vrer[i-1] < low_priority_limit:
                priority = "НИЗЬКИЙ"
            elif self.vrer[i-1] < middle_priority_limit:
                priority = "СЕРЕДНІЙ"
            else:
                priority = "ВИСОКИЙ"
            self.vrer_table.setItem(i-1, 4, QTableWidgetItem(priority))


    def calculate_vrer(self):
        for i in range(1, 47):
            vrer = round(self.event_risks[i-1] * self.loss[i-1], 2)
            self.vrer.append(vrer)
            self.vrer_table.setItem(i-1, 3, QTableWidgetItem(str(vrer)))

    def event_analysys(self):
        for i in range(1, 47):
            row_sum = 0
            for j in range(1, 11):
                row_sum += float(self.risk_analysys_table.item(i-1, j).text())
            self.event_risks.append(round(row_sum / 10, 2))
            self.risk_analysys_table.setItem(i-1, 11, QTableWidgetItem(str(round(row_sum / 10, 2))))
            self.vrer_table.setItem(i-1, 1, QTableWidgetItem(str(round(row_sum / 10, 2))))

    def group_result(self):
        total_sum = 0
        group_sum = 0
        for i in range(1, 11):
            row_sum = float(self.risk_analysys_table.item(i-1, 11).text())
            group_sum += row_sum
        self.group_result_table.setItem(0, 0, QTableWidgetItem(str(round(group_sum / 46, 2))))
        total_sum += group_sum / 46
        
        group_sum = 0
        for i in range(12, 19):
            row_sum = float(self.risk_analysys_table.item(i-1, 11).text())
            group_sum += row_sum
        self.group_result_table.setItem(1, 0, QTableWidgetItem(str(round(group_sum / 46, 2))))
        total_sum += group_sum / 46
        
        group_sum = 0
        for i in range(20, 30):
            row_sum = float(self.risk_analysys_table.item(i-1, 11).text())
            group_sum += row_sum
        self.group_result_table.setItem(2, 0, QTableWidgetItem(str(round(group_sum / 46, 2))))
        total_sum += group_sum / 46

        group_sum = 0
        for i in range(30, 46):
            row_sum = float(self.risk_analysys_table.item(i-1, 11).text())
            group_sum += row_sum
        self.group_result_table.setItem(3, 0, QTableWidgetItem(str(round(group_sum / 46, 2))))
        self.analysysWidget.setCurrentIndex(1)
        total_sum += group_sum / 46

        self.total_result.setText(str(round(total_sum, 2)))

        result = "Ймовірність виникнення ризикової події є "
        if total_sum < 0.1:
            result += "дуже низькою"
        elif total_sum < 0.25:
            result += "низькою"
        elif total_sum < 0.5:
            result += "середньою"
        elif total_sum < 0.75:
            result += "високою"
        else:
            result += "дуже високою"
        
        self.label_result.setText(result)

    def back(self):
        self.riskEventsWidget.setCurrentIndex(1)
        self.riskSourcesWidget.setCurrentIndex(1)
        self.analysysWidget.setCurrentIndex(0)
        
    def init_Data(self):
        self.risk_types = ('tech', 'money', 'plan', 'manage')
        self.risks = dict.fromkeys(self.risk_types, 0)
        self.risks_probability = dict.fromkeys(self.risk_types, 0)
        self.event_risks = []
        self.loss = []
        self.vrer = []
        
    def calculate(self, type_):
        for risk_type in self.risk_types:
            number = 1
            checkbox = self.findChild(QCheckBox, f"{risk_type}_{type_}{number}")
            while checkbox:
                if checkbox.isChecked():
                    self.risks[risk_type] += 1
                number += 1
                checkbox = self.findChild(QCheckBox, f"{risk_type}_{type_}{number}")

    def calculate_probability(self, amount):
        for risk_type in self.risk_types:
            self.risks_probability[risk_type] = (self.risks[risk_type] / amount) * 100
    
    def write_risks_table(self, table):
        for index, risk_type in enumerate(self.risk_types):
            table.setItem(0, index, QTableWidgetItem(str(round(self.risks_probability[risk_type], 2))))

    def risk_probability(self):
        self.calculate('risk')
        self.calculate_probability(18)
        table = self.risk_prob_table
        self.write_risks_table(table)
        table.setItem(0, 4, QTableWidgetItem(str(round(sum(self.risks_probability.values()), 2))))
        self.init_Data()
        self.riskSourcesWidget.setCurrentIndex(0)

    def event_probability(self):
        self.calculate('event')
        self.calculate_probability(46)
        table = self.event_prob_table
        self.write_risks_table(table)
        table.setItem(0, 4, QTableWidgetItem(str(round(sum(self.risks_probability.values()), 2))))
        self.init_Data()
        self.riskEventsWidget.setCurrentIndex(0)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())