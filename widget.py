from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
    QFileDialog,
    QLabel,
    QFrame,
    QComboBox,
    QGridLayout,
    QMessageBox,
    QLineEdit,
    QGroupBox,
    QListWidget,
    QAbstractItemView,
    QRadioButton,
    QVBoxLayout,
    QHBoxLayout,
    QButtonGroup,
    QProgressDialog,
)
from pathlib import Path
from PySide6.QtCore import Qt, QTimer, QThread, Signal, QObject
from PySide6.QtGui import QPixmap
from helper_functions import get_sql_dataframe, validate_file_name_and_path, apply_replacements
from create_excel import create_xlsx_orderform
import os
import sys

class Worker(QObject):
    finished = Signal()
    progress = Signal(int)
    error_occurred = Signal(str)

    def __init__(
        self,
        brand,
        season,
        selected_categories,
        currency,
        size,
        colour_scheme,
        password,
        file_path,
        error_path,
    ):
        super().__init__()
        self.brand = brand
        self.season = season
        self.selected_categories = selected_categories
        self.currency = currency
        self.size = size
        self.colour_scheme = colour_scheme
        self.password = password
        self.file_path = file_path
        self.error_path = error_path

    def run(self):
        try:
            create_xlsx_orderform(
                brand=self.brand,
                season=self.season,
                category=self.selected_categories,
                currency=self.currency,
                use_size=self.size,
                colour_scheme=self.colour_scheme,
                password=self.password,
                file_path=self.file_path,
                file_path_error=self.error_path,
            )
            self.finished.emit()
        except Exception as e:
            self.error_occurred.emit(str(e))

class Widget(QWidget):
    def __init__(self):
        super().__init__()

        if getattr(sys, "frozen", False):
            self.base_path = sys._MEIPASS
        else:
            self.base_path = os.path.abspath(".")

        self.setWindowTitle("Shiner Orderform Builder")

        group_box = QGroupBox("Orderform Selections")

        self.folder_label = QLabel("Output Path:", self)
        self.folder_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        self.folder_text = QLabel("Browse for an output folder", self)
        self.folder_text.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.folder_text.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        browse_button = QPushButton("Browse")

        self.brand_label = QLabel("Brand:", self)
        self.brand_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        with open(
            os.path.join(self.base_path, "t-sql", "brand query.sql"),
            "r",
        ) as file:
            brand_sql = file.read()

        df_brands, error_message = get_sql_dataframe(brand_sql)

        self.brand_combo_box = QComboBox(self)

        if error_message:
            self.show_error_message(error_message)
        else:
            self.brand_combo_box.addItems(df_brands["Brand Name"].tolist())

        self.season_label = QLabel("Season:", self)
        self.season_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.season_combo_box = QComboBox(self)
        self.category_label = QLabel("Category:", self)
        self.category_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        self.category_list = QListWidget(self)
        self.category_list.setSelectionMode(QAbstractItemView.MultiSelection)

        self.currency_label = QLabel("Currency:", self)
        self.currency_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        self.currency_layout = QVBoxLayout()
        self.currency_button_group = QButtonGroup(self)

        currencies = ["GBP", "EUR", "USD"]
        for currency in currencies:
            radio_button = QRadioButton(currency, self)
            self.currency_button_group.addButton(radio_button)
            self.currency_layout.addWidget(radio_button)

        self.currency_button_group.buttons()[0].setChecked(True)

        self.size_label = QLabel("Use Size:", self)
        self.size_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        self.size_layout = QHBoxLayout()
        self.size_button_group = QButtonGroup(self)

        sizes = ["Size 1", "EU", "US"]
        for size in sizes:
            radio_button_size = QRadioButton(size, self)
            self.size_button_group.addButton(radio_button_size)
            self.size_layout.addWidget(radio_button_size)

        self.size_button_group.buttons()[0].setChecked(True)

        self.scheme_label = QLabel("Colour Scheme:", self)
        self.scheme_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        self.scheme_combo_box = QComboBox(self)

        self.scheme_combo_box.addItems(["Shiner Ltd", "Shiner B.V", "Shiner LLC"])

        self.password_label = QLabel("Excel Password:", self)
        self.password_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.password_text = QLineEdit()
        self.password_text.setAlignment(Qt.AlignLeft)

        self.file_name_label = QLabel("Output File Name:", self)
        self.file_name_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.file_name_text = QLineEdit()
        self.file_name_text.setAlignment(Qt.AlignLeft)

        group_box = QGroupBox("Orderform Selections")

        group_layout = QGridLayout()

        group_layout.addWidget(self.folder_label, 0, 0)
        group_layout.addWidget(self.folder_text, 0, 1, 1, 2)
        group_layout.addWidget(browse_button, 0, 3)

        group_layout.addWidget(self.brand_label, 1, 0)
        group_layout.addWidget(self.brand_combo_box, 1, 1)
        group_layout.addWidget(self.season_label, 1, 2)
        group_layout.addWidget(self.season_combo_box, 1, 3)

        group_layout.addWidget(self.category_label, 2, 0)
        group_layout.addWidget(self.category_list, 2, 1)
        group_layout.addWidget(self.currency_label, 2, 2)
        group_layout.addLayout(self.currency_layout, 2, 3)

        group_layout.addWidget(self.size_label, 3, 0)
        group_layout.addLayout(self.size_layout, 3, 1)
        group_layout.addWidget(self.scheme_label, 4, 2)
        group_layout.addWidget(self.scheme_combo_box, 4, 3)

        group_layout.addWidget(self.password_label, 4, 0)
        group_layout.addWidget(self.password_text, 4, 1)

        group_layout.addWidget(self.file_name_label, 5, 0)
        group_layout.addWidget(self.file_name_text, 5, 1, 1, 3)

        group_layout.setContentsMargins(25, 25, 25, 25)

        group_layout.setColumnStretch(0, 1)
        group_layout.setColumnStretch(1, 2)
        group_layout.setColumnStretch(2, 2)
        group_layout.setColumnStretch(3, 1)

        group_layout.setHorizontalSpacing(10)
        group_layout.setVerticalSpacing(20)

        group_layout.setColumnMinimumWidth(1, 200)
        group_layout.setColumnMinimumWidth(3, 130)

        group_box.setLayout(group_layout)

        self.create_button = QPushButton("Create xlsx")
        self.create_button.clicked.connect(self.create_excel_orderform)

        # The below block of code initializes the GUI

        self.update_season_combo_box()
        self.update_category_list()
        self.create_file_name()
        self.validate_form()

        image_label = QLabel(self)
        pixmap = QPixmap(os.path.join(self.base_path, "logos", "SHINER_LOGO_BLK_GEN.png"))
        resized_pixmap = pixmap.scaled(
            80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        image_label.setPixmap(resized_pixmap)
        image_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        main_layout = QGridLayout()

        main_layout.addWidget(image_label, 0, 0, 1, 1, Qt.AlignLeft)
        main_layout.addWidget(group_box, 1, 0, 1, 4)
        main_layout.addWidget(self.create_button, 2, 3, 1, 1)

        main_layout.setContentsMargins(25, 25, 25, 25)

        main_layout.setColumnStretch(0, 1)
        main_layout.setColumnStretch(1, 2)
        main_layout.setColumnStretch(2, 2)
        main_layout.setColumnStretch(3, 1)

        main_layout.setHorizontalSpacing(10)
        main_layout.setVerticalSpacing(20)

        main_layout.setColumnMinimumWidth(1, 200)
        main_layout.setColumnMinimumWidth(3, 130)

        self.setLayout(main_layout)

        # The below code sorts out all the signals in the app

        browse_button.clicked.connect(self.browse_button_clicked)
        self.brand_combo_box.currentTextChanged.connect(self.form_selection_change)
        self.season_combo_box.currentTextChanged.connect(self.form_selection_change)
        self.category_list.itemSelectionChanged.connect(self.input_selection_change)
        self.currency_button_group.buttonClicked.connect(self.form_selection_change)
        self.password_text.textChanged.connect(self.validate_form)

    def show_error_message(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText("An error occurred")
        msg_box.setInformativeText(message)
        msg_box.setWindowTitle("Error")
        msg_box.exec()

    def show_info_message(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText("Information")
        msg_box.setInformativeText(message)
        msg_box.setWindowTitle("Information")
        msg_box.exec()

    def show_warning_message(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setText("Warning")
        msg_box.setInformativeText(message)
        msg_box.setWindowTitle("Warning")
        msg_box.exec()

    def browse_button_clicked(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.folder_text.setText(directory)

        self.validate_form()

    def create_file_name(self):
        brand_text = self.brand_combo_box.currentText()
        season_text = self.season_combo_box.currentText()

        selected_currency_button = self.currency_button_group.checkedButton()

        currency_text = selected_currency_button.text()

        selected_categories = [
            item.text() for item in self.category_list.selectedItems()
        ]

        if len(selected_categories) > 1:
            category_text = "Multiple Categories"
        elif len(selected_categories) == 1:
            category_text = selected_categories[0]
        else:
            category_text = ""

        file_name = (
            f"{brand_text} {category_text} {season_text} Orderform {currency_text}"
        )

        self.file_name_text.setText(file_name)

    def update_category_list(self):

        self.category_list.blockSignals(True)

        self.category_list.clear()

        brand_text = self.brand_combo_box.currentText()
        season_text = self.season_combo_box.currentText()

        selected_currency_button = self.currency_button_group.checkedButton()

        currency_text = selected_currency_button.text()

        with open(
            os.path.join(self.base_path, "t-sql", "category query.sql"),
            "r",
        ) as file:
            category_sql = file.read()

        category_sql = apply_replacements(category_sql, brand=brand_text, currency=currency_text, season=season_text)
        
        df_category, error_message = get_sql_dataframe(category_sql)

        if error_message:
            self.show_error_message(error_message)
        else:
            self.category_list.addItems(df_category["Category"].tolist())

        self.category_list.blockSignals(False)

    def update_season_combo_box(self):
        self.season_combo_box.blockSignals(True)

        current_season = self.season_combo_box.currentText()

        self.season_combo_box.clear()

        brand_text = self.brand_combo_box.currentText()
        
        with open(
            os.path.join(self.base_path, "t-sql", "season query.sql"),
            "r",
        ) as file:
            season_sql = file.read()

        season_sql = apply_replacements(season_sql, brand=brand_text)

        df_season, error_message = get_sql_dataframe(season_sql)
        
        if error_message:
            self.show_error_message(error_message)
        else:
            if not df_season.empty:
                self.season_combo_box.addItems(df_season["Season Code"].tolist())

                if current_season in df_season["Season Code"].tolist():
                    index = self.season_combo_box.findText(current_season)
                    self.season_combo_box.setCurrentIndex(index)
                else:
                    self.season_combo_box.setCurrentIndex(0)
            else:
                self.show_error_message(
                    "No seasons available for the selected brand and currency."
                )

        self.season_combo_box.blockSignals(False)
        
    def form_selection_change(self):
        self.update_season_combo_box()
        self.update_category_list()
        self.create_file_name()
        self.validate_form()

    def input_selection_change(self):
        self.validate_form()
        self.create_file_name()

    def validate_form(self):
        folder_filled = (
            self.folder_text.text() != "Browse for an output folder"
            and self.folder_text.text() != ""
        )
        brand_selected = self.brand_combo_box.currentText() != ""
        season_selected = self.season_combo_box.currentText() != ""
        categories_selected = len(self.category_list.selectedItems()) > 0
        password_filled = self.password_text.text() != ""

        if folder_filled:
            self.folder_label.setText("Output Path:")
        else:
            self.folder_label.setText("Output Path: <span style='color:red;'>*</span>")

        if brand_selected:
            self.brand_label.setText("Brand:")
        else:
            self.brand_label.setText("Brand: <span style='color:red;'>*</span>")

        if season_selected:
            self.season_label.setText("Season:")
        else:
            self.season_label.setText("Season: <span style='color:red;'>*</span>")

        if categories_selected:
            self.category_label.setText("Category:")
        else:
            self.category_label.setText("Category: <span style='color:red;'>*</span>")

        if password_filled:
            self.password_label.setText("Excel Password:")
        else:
            self.password_label.setText(
                "Excel Password: <span style='color:red;'>*</span>"
            )

        if (
            folder_filled
            and brand_selected
            and season_selected
            and categories_selected
            and password_filled
        ):
            self.create_button.setEnabled(True)
        else:
            self.create_button.setEnabled(False)

    def show_progress_dialog(self):
        self.progress_dialog = QProgressDialog(
            "Creating Orderform...", "Cancel", 0, 100, self
        )
        self.progress_dialog.setWindowTitle("Creating Orderform")
        self.progress_dialog.setWindowModality(Qt.WindowModal)
        self.progress_dialog.setMinimumDuration(0)
        self.progress_dialog.setAutoClose(False)
        self.progress_dialog.setAutoReset(True)
        self.progress_dialog.setValue(0)

    def update_progress(self):
        value = self.progress_dialog.value()
        if value < 100:
            value += 1.5
            self.progress_dialog.setValue(value)
        else:
            self.timer.stop()

    def finish_up_task(self):
        self.timer.stop()
        self.progress_dialog.setValue(100)
        self.progress_dialog.close()

        if os.path.isfile(self.worker.error_path):
            self.show_warning_message(
                f"You have successfully created the orderform: {self.worker.file_path.name}.\n\n"
                f"This ordeform is saved at the following location: {self.worker.file_path.parent}.\n\n"
                 "Errors in the item card data have been identified during the creation of this orderform. The affected items were removed."
                 " An error xlsx file has been created in the same location for you to review the items."
            )
        else:
            self.show_info_message(
                f"You have successfully created the orderform: {self.worker.file_path.name}\n\n"
                f"It is saved at the following location: {self.worker.file_path.parent}"
            )

        self.create_button.setEnabled(True)

    def create_excel_orderform(self):
        self.create_button.setEnabled(False)

        brand_text = self.brand_combo_box.currentText()
        season_text = self.season_combo_box.currentText()
        selected_categories = ", ".join(
            f"'{item}'"
            for item in [item.text() for item in self.category_list.selectedItems()]
        )
        selected_currency_button = self.currency_button_group.checkedButton()
        currency_text = selected_currency_button.text()
        selected_size_button = self.size_button_group.checkedButton()
        size_text = selected_size_button.text()
        colour_scheme_text = self.scheme_combo_box.currentText()
        password_text = self.password_text.text()
        folder_path = self.folder_text.text()
        file_name = self.file_name_text.text() + ".xlsx"
        file_name_error = self.file_name_text.text() + " Error.xlsx"
        file_path = Path(folder_path + "/" + file_name)
        error_path = Path(folder_path + "/" + file_name_error)

        is_valid, error_message = validate_file_name_and_path(
            file_name, file_name_error, folder_path
        )
        if not is_valid:
            self.show_error_message(error_message)
            return

        self.show_progress_dialog()

        self.thread = QThread()
        self.worker = Worker(
            brand_text,
            season_text,
            selected_categories,
            currency_text,
            size_text,
            colour_scheme_text,
            password_text,
            file_path,
            error_path,
        )
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.error_occurred.connect(
            self.handle_worker_error
        )
        self.thread.finished.connect(self.thread.deleteLater)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(700)

        self.worker.finished.connect(self.finish_up_task)

        self.thread.start()

    def handle_worker_error(self, error_message):
        self.timer.stop()
        self.progress_dialog.close()

        self.show_error_message(error_message)

        self.thread.quit()
        self.thread.wait()
        self.thread.deleteLater()

        self.create_button.setEnabled(True)