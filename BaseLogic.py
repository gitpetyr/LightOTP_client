from urllib.parse import urljoin
import requests,os

def register(Server_URL,UserID,Password):
    Tokens={"userid" : UserID , "usertoken" : Password}
    res=requests.post(urljoin(Server_URL,"/register"),params=Tokens)
    
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
            baseurl="https://"+self.Server_URL
        else:
            baseurl="http://"+self.Server_URL
        # print(baseurl)
        return urljoin(baseurl,idx)
    def CheckConnect(self):
        Tokens={"userid" : self.UserID , "usertoken" : self.Password}
        res=requests.post(self.calcURL("test/checktoken"),params=Tokens)
        
        res_iter=(res.status_code,res.json())
        
        if res_iter[0]!=200:
            raise RuntimeError(res_iter)
        
        if "requests" in list(res_iter[1].keys()):
            del res_iter[1]["requests"]
            
        return res_iter
    
    def addTOTP(self,name : str,totpkey : str):
        Tokens={"userid" : self.UserID , "usertoken" : self.Passwd , "totpname" : name ,"totpkey" : totpkey}
        res=requests.post(self.calcURL("addtotp"),params=Tokens,verify=not(self.SkipSSLCERT))
        
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
        res=requests.post(self.calcURL("deltotp"),params=Tokens,verify=not(self.SkipSSLCERT))
        
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
        res=requests.post(self.calcURL("gettotp"),params=Tokens,verify=not(self.SkipSSLCERT))
        
        res_iter=(res.status_code,res.json())
        
        if res_iter[0]!=200:
            raise RuntimeError(res_iter)
        
        if "requests" in list(res_iter[1].keys()):
            del res_iter[1]["requests"]
            
        if not("res" in list(res_iter[1])):
            raise RuntimeError(res_iter)
        
        return str(res_iter[1]["res"]["totpkey"])
    
    def getTOTPList(self):
        Tokens={"userid" : self.UserID , "usertoken" : self.Passwd}
        res=requests.post(self.calcURL("gettotplist"),params=Tokens,verify=not(self.SkipSSLCERT))
        
        res_iter=(res.status_code,res.json())
        
        if res_iter[0]!=200:
            raise RuntimeError(res_iter)
        
        if "requests" in list(res_iter[1].keys()):
            del res_iter[1]["requests"]
            
        if not("res" in list(res_iter[1].keys())):
            raise RuntimeError(res_iter)
        
        if not("totpnames" in list(res_iter[1]["res"])):
            return []
        print(res_iter)
        return list(res_iter[1]["res"]["totpnames"])
    
    def getTOTPiter(self):
        ls=self.getTOTPList()
        iter={}
        for i in ls:
            try:
                iter[i]=self.getTOTP(i)
            except RuntimeError as e:
                iter[i]=str(e)
            finally:
                pass
        return iter
    
    
        
    
if __name__ == "__main__":
    while True:
        exec(input(">>>"))