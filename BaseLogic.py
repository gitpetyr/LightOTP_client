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
        Server_URL=""
        UseHTTPS=False
        SkipSSLCERT=False
        UserID=""
        Passwd=""
    def CheckConnect(self):
        pass
    
if __name__ == "__main__":
    while True:
        exec(input(">>>"))