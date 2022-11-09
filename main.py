import sys
import os
from sqlite3 import IntegrityError

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QLabel, QLineEdit

import sqlite3
import typing as tp


def sqlite_lower(string):  # Переопределение функции преобразования к нижнему регистру
    return string.lower()


def sqlite_upper(string):  # Переопределение функции преобразования к верхнему регистру
    return string.upper()


class Data:
    def __init__(self) -> None:
        if not os.path.exists('./data'):
            os.mkdir('./data')
        with sqlite3.connect('./data/base.db') as db:
            cursor = db.cursor()
            query = """CREATE TABLE IF NOT EXISTS "maths" (
                    'name' TEXT PRIMARY KEY,
                    'formula' TEXT,
                    'section' TEXT
                    )"""
            cursor.execute(query)
            db.commit()

        self.error: tp.Optional[ExistingElementErrorWindow] = None
        self.cursor = db.cursor()

    def add(self, name: str, formula: str, section: str) -> None:
        with sqlite3.connect('./data/base.db') as db:
            self.cursor = db.cursor()
            query = f"""INSERT INTO maths(name, formula, section) VALUES(?, ?, ?)"""
            self.cursor.execute(query, (name, formula, section))
            db.commit()

    def update_formula(self, name: str, formula: str) -> None:
        with sqlite3.connect('./data/base.db') as db:
            db.create_function("LOWER", 1, sqlite_lower)
            db.create_function("UPPER", 1, sqlite_upper)
            self.cursor = db.cursor()
            query = f"""UPDATE maths 
            SET formula = ? 
            WHERE LOWER(name) = ?"""
            self.cursor.execute(query, (formula, name.lower()))
            db.commit()

    def update_section(self, name: str, section: str) -> None:
        with sqlite3.connect('./data/base.db') as db:
            db.create_function("LOWER", 1, sqlite_lower)
            db.create_function("UPPER", 1, sqlite_upper)
            self.cursor = db.cursor()
            query = f"""UPDATE maths 
            SET section = ? 
            WHERE LOWER(name) = ?"""
            self.cursor.execute(query, (section, name.lower()))
            db.commit()

    def delete_values(self, name: str) -> None:
        with sqlite3.connect('./data/base.db') as db:
            db.create_function("LOWER", 1, sqlite_lower)
            db.create_function("UPPER", 1, sqlite_upper)
            self.cursor = db.cursor()
            query = f"""DELETE FROM maths 
            WHERE LOWER(name) = ?"""
            self.cursor.execute(query, (name.lower(),))
            db.commit()

    def select_values(self, name: str) -> list:
        with sqlite3.connect('./data/base.db') as db:
            db.create_function("LOWER", 1, sqlite_lower)
            db.create_function("UPPER", 1, sqlite_upper)
            self.cursor = db.cursor()
            query = f"""SELECT * FROM maths 
            WHERE LOWER(name) = ?"""
            result = self.cursor.execute(query, (name.lower(),)).fetchall()
            return result


data = Data()


class MissingElementErrorWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.label = QLabel(self)

        self.initUI()

    def initUI(self) -> None:
        self.setGeometry(700, 450, 550, 200)
        self.setWindowTitle('Ошибка')
        self.label.setFont(QFont('Arial', 12))
        self.label.setText("Введено отсутствующее название закона.")
        self.label.move(30, 65)


class ExistingElementErrorWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.label = QLabel(self)
        self.initUI()

    def initUI(self) -> None:
        self.setGeometry(700, 500, 500, 200)
        self.setWindowTitle('Ошибка')
        self.label.setFont(QFont('Arial', 12))
        self.label.setText("Этот закон уже есть в базе.")
        self.label.move(90, 65)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.ex1 = AddWindow()
        self.ex2 = DelWindow()
        self.ex3 = FormulaWindow()
        self.ex4 = SectionWindow()
        self.ex5 = CheckWindow()

        self.add_button = QPushButton('Добавить новый математический закон', self)
        self.del_button = QPushButton('Удалить уже существующий закон', self)
        self.formula_button = QPushButton('Изменить формулу закона', self)
        self.section_button = QPushButton('Изменить раздел математики закона', self)
        self.check_button = QPushButton('Посмотреть закон', self)

        self.initUI()

    def initUI(self) -> None:
        self.setGeometry(600, 360, 700, 440)
        self.setWindowTitle('Math.exe')
        text_font = QFont('Arial', 14)

        self.add_button.resize(660, 75)
        self.add_button.move(20, 20)
        self.add_button.setFont(text_font)
        self.add_button.clicked.connect(self.add)

        self.del_button.resize(660, 75)
        self.del_button.move(20, 100)
        self.del_button.setFont(text_font)
        self.del_button.clicked.connect(self.delete)

        self.formula_button.resize(660, 75)
        self.formula_button.move(20, 180)
        self.formula_button.setFont(text_font)
        self.formula_button.clicked.connect(self.formula)

        self.section_button.resize(660, 75)
        self.section_button.move(20, 260)
        self.section_button.setFont(text_font)
        self.section_button.clicked.connect(self.section)

        self.check_button.resize(660, 75)
        self.check_button.move(20, 340)
        self.check_button.setFont(text_font)
        self.check_button.clicked.connect(self.check)

    def add(self) -> None:
        self.ex1.show()

    def delete(self) -> None:
        self.ex2.show()

    def formula(self) -> None:
        self.ex3.show()

    def section(self) -> None:
        self.ex4.show()

    def check(self) -> None:
        self.ex5.show()


class AddWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.name_input = QLineEdit(self)
        self.formula_input = QLineEdit(self)
        self.section_input = QLineEdit(self)

        self.result_button = QPushButton('Подтвердить', self)

        self.error = ExistingElementErrorWindow()

        self.initUI()

    def initUI(self) -> None:
        self.setGeometry(700, 400, 500, 350)
        self.setWindowTitle('Добавление закона')
        text_font = QFont('Arial', 10)

        label1 = QLabel(self)
        label1.setFont(text_font)
        label1.setText("Введите название закона")
        label1.move(20, 20)

        self.name_input.move(20, 52)
        self.name_input.resize(450, 30)

        label2 = QLabel(self)
        label2.setFont(text_font)
        label2.setText("Введите формулу")
        label2.move(20, 110)

        self.formula_input.move(20, 142)
        self.formula_input.resize(450, 30)

        label3 = QLabel(self)
        label3.setFont(text_font)
        label3.setText("Введите раздел математики закона")
        label3.move(20, 200)

        self.section_input.move(20, 232)
        self.section_input.resize(450, 30)

        self.result_button.resize(150, 30)
        self.result_button.move(320, 300)
        self.result_button.setFont(QFont('Arial', 8))
        self.result_button.clicked.connect(self.input_result)

    def input_result(self) -> None:
        name = self.name_input.text()
        formula = self.formula_input.text()
        section = self.section_input.text()
        try:
            data.add(name, formula, section)
            self.close()
        except IntegrityError:
            self.error.show()


class DelWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.name_input = QLineEdit(self)

        self.result_button = QPushButton('Подтвердить', self)

        self.error = MissingElementErrorWindow()

        self.initUI()

    def initUI(self) -> None:
        self.setGeometry(700, 400, 500, 200)
        self.setWindowTitle('Удаление закона')
        text_font = QFont('Arial', 10)

        label1 = QLabel(self)
        label1.setFont(text_font)
        label1.setText("Введите название закона")
        label1.move(20, 20)

        self.name_input.move(20, 52)
        self.name_input.resize(450, 30)

        self.result_button.resize(150, 30)
        self.result_button.move(320, 150)
        self.result_button.setFont(QFont('Arial', 8))
        self.result_button.clicked.connect(self.input_result)

    def input_result(self) -> None:
        name = self.name_input.text()
        try:
            data.delete_values(name)
        except:
            self.error.show()
        self.close()


class FormulaWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.name_input = QLineEdit(self)
        self.formula_input = QLineEdit(self)

        self.result_button = QPushButton('Подтвердить', self)

        self.error = MissingElementErrorWindow()

        self.initUI()

    def initUI(self) -> None:
        self.setGeometry(700, 400, 500, 275)
        self.setWindowTitle('Изменение формулы закона')
        text_font = QFont('Arial', 10)

        label1 = QLabel(self)
        label1.setFont(text_font)
        label1.setText("Введите название закона")
        label1.move(20, 20)

        self.name_input.move(20, 52)
        self.name_input.resize(450, 30)

        label2 = QLabel(self)
        label2.setFont(text_font)
        label2.setText("Введите формулу")
        label2.move(20, 110)

        self.formula_input.move(20, 142)
        self.formula_input.resize(450, 30)

        self.result_button.resize(150, 30)
        self.result_button.move(320, 230)
        self.result_button.setFont(QFont('Arial', 8))
        self.result_button.clicked.connect(self.input_result)

    def input_result(self) -> None:
        name = self.name_input.text()
        formula = self.formula_input.text()
        try:
            data.update_formula(name, formula)
        except:
            self.error.show()
        self.close()


class SectionWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.name_input = QLineEdit(self)
        self.section_input = QLineEdit(self)

        self.result_button = QPushButton('Подтвердить', self)

        self.error = MissingElementErrorWindow()

        self.initUI()

    def initUI(self) -> None:
        self.setGeometry(700, 400, 500, 275)
        self.setWindowTitle('Изменение раздела математики закона')
        text_font = QFont('Arial', 10)

        label1 = QLabel(self)
        label1.setFont(text_font)
        label1.setText("Введите название закона")
        label1.move(20, 20)

        self.name_input.move(20, 52)
        self.name_input.resize(450, 30)

        label2 = QLabel(self)
        label2.setFont(text_font)
        label2.setText("Введите раздел математики")
        label2.move(20, 110)

        self.section_input.move(20, 142)
        self.section_input.resize(450, 30)

        self.result_button.resize(150, 30)
        self.result_button.move(320, 230)
        self.result_button.setFont(QFont('Arial', 8))
        self.result_button.clicked.connect(self.input_result)

    def input_result(self) -> None:
        name = self.name_input.text()
        section = self.section_input.text()
        try:
            data.update_section(name, section)
        except:
            self.error.show()
        self.close()


class CheckWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.name_input = QLineEdit(self)

        self.result_button = QPushButton('Подтвердить', self)

        self.error = MissingElementErrorWindow()
        self.result_window: tp.Optional[ResultWindow] = None

        self.initUI()

    def initUI(self) -> None:
        self.setGeometry(700, 400, 500, 200)
        self.setWindowTitle('Просмотр закона')
        text_font = QFont('Arial', 10)

        label1 = QLabel(self)
        label1.setFont(text_font)
        label1.setText("Введите название закона")
        label1.move(20, 20)

        self.name_input.move(20, 52)
        self.name_input.resize(450, 30)

        self.result_button.resize(150, 30)
        self.result_button.move(320, 150)
        self.result_button.setFont(QFont('Arial', 8))
        self.result_button.clicked.connect(self.input_result)

    def input_result(self) -> None:
        name = self.name_input.text()
        result = data.select_values(name)
        if not result:
            self.error.show()
            return
        name = result[0][0]
        formula = result[0][1]
        section = result[0][2]
        self.result_window = ResultWindow(name, formula, section)
        self.result_window.show()


class ResultWindow(QWidget):
    def __init__(self, name: str, formula: str, section: str) -> None:
        super().__init__()

        self.name = name
        self.formula = formula
        self.section = section

        self.error = MissingElementErrorWindow()

        self.initUI()

    def initUI(self) -> None:
        result_string = self.name + ': ' + self.formula + ', раздел математики - '
        result_string += self.section.lower() + '.'
        self.setGeometry(600, 500, 750, 120)
        self.setWindowTitle('Просмотр закона')
        text_font = QFont('Arial', 10)

        label1 = QLabel(self)
        label1.setFont(text_font)
        label1.setText(result_string)
        label1.move(20, 40)


def main() -> None:
    math = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(math.exec())


if __name__ == '__main__':
    main()
