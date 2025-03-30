from ui.MainWindow import Ui_MainWindow
from ui.RegistrationDialog import Ui_RegistrationDialog
from ui.SettingDialog import Ui_SettingDialog
from PyQt6.QtWidgets import QApplication,QMainWindow,QDialog
import BaseLogic
import sys,PyQt6

Connector=BaseLogic.OTPConnector()

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
        self.setModal(True)
        self.RegisterButton.clicked.connect(self.register_on_click)
        
class SettingDialog(Ui_SettingDialog,QDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.LogicSetup()
        self.show()
        self.exec()
    
    def ProtocolChanged(self):
        Connector.UseHTTPS=bool(self.ProtocolBox.currentIndex())
        if not Connector.UseHTTPS:
            self.SkipCertBox.setEnabled(False)
        else:
            self.SkipCertBox.setEnabled(True)
    
    def SkipedChanged(self):
        Connector.SkipSSLCERT=self.SkipCertBox.isChecked()
    
    def LogicSetup(self):
        self.setModal(True)
        self.UrlEdit.setText(Connector.Server_URL)
        self.UserIDEdit.setText(Connector.UserID)
        self.PasswordEdit.setText(Connector.Passwd)
        if Connector.UseHTTPS:
            self.ProtocolBox.setCurrentIndex(1)
            self.SkipCertBox.setEnabled(True)
        else:
            self.ProtocolBox.setCurrentIndex(0)
            self.SkipCertBox.setEnabled(False)
        if Connector.SkipSSLCERT:
            self.SkipCertBox.setChecked(True)
        else:
            self.SkipCertBox.setChecked(False)
        self.ProtocolBox.currentIndexChanged.connect(self.ProtocolChanged)
        self.SkipCertBox.stateChanged.connect(self.SkipedChanged)

class MainUI(Ui_MainWindow,QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.LogicSetup()
        self.show()
        
    def LogicSetup(self):
        self.actionExit.triggered.connect(self.close)
        self.actionRegistration_Tools.triggered.connect(RegistrationDialog)
        self.actionSettings.triggered.connect(SettingDialog)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainUI = MainUI()
    sys.exit(app.exec())