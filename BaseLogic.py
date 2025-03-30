from urllib.parse import urljoin
import requests

def register(Server_URL,UserID,Password):
    Tokens={"userid" : UserID , "usertoken" : Password}
    res=requests.post(urljoin(Server_URL,"register"),params=Tokens)
    
    res_iter=(res.status_code,res.json())
    
    if res_iter[0]!=200:
        raise RuntimeError(res_iter)
    
    if "requests" in list(res_iter[1].keys()):
        del res_iter[1]["requests"]
        
    if res_iter[1]["res"]!="Ok":
        raise RuntimeError(res_iter)
    
    return res_iter

class OTPConnector():
    def __init__(self):
        self.Server_URL=""
        self.UseHTTPS=True
        self.SkipSSLCERT=False
        self.UserID=""
        self.Passwd=""
    def calcURL(self,idx : str):
        if self.UseHTTPS:
            baseurl=urljoin("https://",self.Server_URL)
        else:
            baseurl=urljoin("http://",self.Server_URL)
        return urljoin(baseurl,idx)
    def CheckConnect(self):
        Tokens={"userid" : self.UserID , "usertoken" : self.Password}
        res=requests.post(self.calcURL("/test/checktoken"),params=Tokens)
        
        res_iter=(res.status_code,res.json())
        
        if res_iter[0]!=200:
            raise RuntimeError(res_iter)
        
        if "requests" in list(res_iter[1].keys()):
            del res_iter[1]["requests"]
            
        return res_iter
    
    def addTOTP(self,name : str,totpkey : str):
        Tokens={"userid" : self.UserID , "usertoken" : self.Passwd , "totpname" : name ,"totpkey" : totpkey}
        res=requests.post(self.calcURL("/addtotp"),params=Tokens)
        
        res_iter=(res.status_code,res.json())
        
        if res_iter[0]!=200:
            raise RuntimeError(res_iter)
        
        if "requests" in list(res_iter[1].keys()):
            del res_iter[1]["requests"]
            
        if res_iter[1]["res"]!="Ok":
            raise RuntimeError(res_iter)
        
        return "Ok"
    
    def delTOTP(self,name : str):
        Tokens={"userid" : self.UserID , "usertoken" : self.Passwd , "totpname" : name}
        res=requests.post(self.calcURL("/deltotp"),params=Tokens)
        
        res_iter=(res.status_code,res.json())
        
        if res_iter[0]!=200:
            raise RuntimeError(res_iter)
        
        if "requests" in list(res_iter[1].keys()):
            del res_iter[1]["requests"]
            
        if res_iter[1]["res"]!="Ok":
            raise RuntimeError(res_iter)
        
        return "Ok"
    
    def getTOTP(self,name : str):
        Tokens={"userid" : self.UserID , "usertoken" : self.Passwd , "totpname" : name}
        res=requests.post(self.calcURL("/gettotp"),params=Tokens)
        
        res_iter=(res.status_code,res.json())
        
        if res_iter[0]!=200:
            raise RuntimeError(res_iter)
        
        if "requests" in list(res_iter[1].keys()):
            del res_iter[1]["requests"]
            
        if not("res" in list(res_iter[1])):
            raise RuntimeError(res_iter)
        
        return str(res_iter["res"]["totpkey"])
    
    def getTOTPList(self):
        Tokens={"userid" : self.UserID , "usertoken" : self.Passwd}
        res=requests.post(self.calcURL("/gettotplist"),params=Tokens)
        
        res_iter=(res.status_code,res.json())
        
        if res_iter[0]!=200:
            raise RuntimeError(res_iter)
        
        if "requests" in list(res_iter[1].keys()):
            del res_iter[1]["requests"]
            
        if not("res" in list(res_iter[1])):
            raise RuntimeError(res_iter)
        
        return list(res_iter["res"]["totpnames"])
    
    
        
    
if __name__ == "__main__":
    while True:
        exec(input(">>>"))