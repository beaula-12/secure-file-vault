from ftplib import FTP
ftp = FTP('')
def start():
    
    ftp.connect('ftp.drivehq.com')
    ftp.login("SecureFileTeam12", "4NtH_B9TMhLPis_")
    ftp.cwd('/cloud/') #replace with your directory
    ftp.retrlines('LIST')
            
def uploadFile(filename, path):
    ftp.storbinary('STOR '+filename, open(path, 'rb'))
 
def downloadFile(filename):
 localfile = open("C:/Users/dell/Desktop/input/downdes.txt", 'wb')
 ftp.retrbinary('RETR ' + filename, localfile.write, 1024)
 ftp.quit()
 localfile.close()

def close():
    ftp.quit()
