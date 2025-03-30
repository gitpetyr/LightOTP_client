from ui.MainWindow import Ui_MainWindow
from ui.RegistrationDialog import Ui_RegistrationDialog
from ui.SettingDialog import Ui_SettingDialog
from ui.AddDialog import Ui_AddDialog
from PyQt6.QtWidgets import QApplication,QMainWindow,QDialog,QTableWidgetItem
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
    
    def Save(self):
        Connector.Server_URL=self.UrlEdit.text()
        Connector.UserID=self.UserIDEdit.text()
        Connector.Passwd=self.PasswordEdit.text()
        Connector.UseHTTPS=bool(self.ProtocolBox.currentIndex())
        Connector.SkipSSLCERT=self.SkipCertBox.isChecked()
    def ProtocolChanged(self):
        if self.ProtocolBox.currentIndex()==0:
            self.SkipCertBox.setEnabled(False)
        else:
            self.SkipCertBox.setEnabled(True)
    def SkipedChanged(self):
        pass
    
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
        self.accepted.connect(self.Save)
        self.ProtocolBox.currentIndexChanged.connect(self.ProtocolChanged)
        self.SkipCertBox.stateChanged.connect(self.SkipedChanged)
        
class AddDialog(Ui_AddDialog,QDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.LogicSetup()
        self.show()
        self.exec()
    
    def Accepted(self):
        try:
            Connector.addTOTP(self.OtpNameEdit.text(),self.KeyEdit.toPlainText())
            mainUI.fresh()
        except Exception as e:
            mainUI.LogsEdit.setPlainText(str(e))
        finally:
            pass
    
    def LogicSetup(self):
        self.setModal(True)
        self.buttonBox.accepted.connect(self.Accepted)
        pass

class MainUI(Ui_MainWindow,QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.LogicSetup()
        self.show()
    
    def fresh(self):
        try:
            self.FreshButton.setEnabled(False)
            iter=Connector.getTOTPiter()
            print(iter)
            row=0
            # self.OtpTable.clear()
            self.OtpTable.setRowCount(len(iter))
            for i in iter:
                self.OtpTable.setItem(row,0,QTableWidgetItem(i))
                self.OtpTable.setItem(row,1,QTableWidgetItem(iter[i]))
                row=row+1
            self.FreshButton.setEnabled(True)
        except Exception as e:
            self.LogsEdit.setPlainText(str(e))
        finally:
            pass
    def deleteOTP(self):
        try:
            row=self.OtpTable.currentRow()
            target=self.OtpTable.item(row,0).text()
            print(target)
        except Exception as e:
            self.LogsEdit.setPlainText(str(e))
        finally:
            pass
    
    def LogicSetup(self):
        self.actionExit.triggered.connect(self.close)
        self.actionRegistration_Tools.triggered.connect(RegistrationDialog)
        self.actionSettings.triggered.connect(SettingDialog)
        self.FreshButton.clicked.connect(self.fresh)
        self.AddButton.clicked.connect(AddDialog)
        self.DelButton.clicked.connect(self.deleteOTP)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainUI = MainUI()
    sys.exit(app.exec())