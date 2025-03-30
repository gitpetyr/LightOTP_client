from ui.MainWindow import Ui_MainWindow
from ui.RegistrationDialog import Ui_RegistrationDialog
from PyQt6.QtWidgets import QApplication,QMainWindow,QDialog
import BaseLogic
import sys,PyQt6

class RegistrationDialog(Ui_RegistrationDialog,QDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.LogicSetup()
        self.show()
        self.exec()
    
    def register_on_click(self):
        try:
            self.RegisterButton.setEnabled(False)
            mainUI.LogsEdit.setPlainText(str(BaseLogic.register(self.UrlEdit.text(),self.UserIDEdit.text(),self.PasswordEdit.text())))
        except Exception as e:
            mainUI.LogsEdit.setPlainText(str(e))
        finally:
            self.RegisterButton.setEnabled(True)
    
    def LogicSetup(self):
        self.RegisterButton.clicked.connect(self.register_on_click)

class MainUI(Ui_MainWindow,QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.LogicSetup()
        self.show()
        
    def LogicSetup(self):
        self.actionExit.triggered.connect(self.close)
        self.actionRegistration_Tools.triggered.connect(RegistrationDialog)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainUI = MainUI()
    sys.exit(app.exec())