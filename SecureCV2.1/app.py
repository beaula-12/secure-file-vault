from fileinput import filename
from logging import error
from flask import send_file
import os
# import datetime
# import hashlib
# import Crypto.Cipher
from Cryptodome.Cipher import AES 
from flask import Flask, session, url_for, redirect, render_template, request, abort, flash
# from pyparsing import empty
from database import user_reg,owner_reg,owner_login,upload_file,owner_viewfiles,upload_clouddata,user_request,owner_request,user_lastdownload
from database import onwer_viewdata,user_loginact,user_viewfile,user_viewfiledata,user_down,verify_user,verify_user2,user_finaldown,owner_update,user_down1,getUserEmailFromUsername
from werkzeug.utils import secure_filename
from AES import AESCipher
from des import des
# import random
import base64
# import cv2
from stegano import lsb 
from RSA import encrypt,decrypt,generate
from cloud import uploadFile,downloadFile,close,start
from sendmail import sendmail
from ftplib import FTP
from fileEncode import fileEncoding

app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route("/")
def FUN_root():
    return render_template("index_.html")


@app.route("/owner", methods = ['GET','POST'])
def FUN_admin():
    login_="/ownerlogact" 
    register_='/ownerreg'
    return render_template("login_.html",login=login_,register=register_,endUser="Owner",image ="loginOwner.svg")

@app.route("/ownerlogact",methods = ['GET','POST'])
def owner_logact():
   if request.method == 'POST':
       try:
           status=owner_login(request.form['username'],request.form['password'])
           if status == True:
               session['username'] = request.form['username']
               return render_template("ownerHome_.html",m1="Login sucess",endUser= "Owner")
           else:
               return render_template("login_.html",login="/ownerlogact",register='/ownerreg',endUser= "Owner",image ="loginOwner.svg",message = "Invalid Details")
       except Exception as e:
           return render_template("login_.html",login="/ownerlogact",register='/ownerreg',endUser= "Owner",image ="loginOwner.svg",message = "Invalid Details" )


@app.route("/ownerreg/")
def FUN_ownerreg():
      return render_template("register_.html",login="/owner",register='/ownerregact',endUser= "Owner")

@app.route("/ownerregact", methods = ['GET','POST'])
def FUN_ownerregact():
    if request.method == 'POST':
        try:
            status = owner_reg(request.form['username'],request.form['password'],request.form['dob'],request.form['email'],request.form['city'],request.form['contactno'])
            if status == True:
                return render_template("login_.html",login="/ownerlogact",register='/ownerreg',endUser= "Owner",image ="loginOwner.svg",m1="Registration Success")
            else:
                return render_template("register_.html",login="/owner",register='/ownerregact',endUser= "Owner")
        except Exception as err:
            err = registration_validation(err,"owner")
            return render_template("register_.html",login="/owner",register='/ownerregact',endUser= "Owner",message=err)

@app.route("/user/")
def FUN_student():
    
    return render_template("login_.html",login="/userlogact",register="/userreg",endUser= "User",image ="loginUser.svg")

@app.route("/userlogact",methods = ['GET','POST'])
def user_logact():
    if request.method == 'POST':
            status=user_loginact(request.form['username'],request.form['password'])
            if status == True:
                session['username'] = request.form['username']
                session['email'] = getUserEmailFromUsername(session['username'])
                return render_template("userHome_.html",m1="Login sucess",endUser= "User")
            else:
                return render_template("login_.html",login="/userlogact",register="/userreg",m2="fail",endUser= "User",image ="loginUser.svg",message = "Invalid Details")
        

@app.route("/userreg/")
def FUN_userreg():
    return render_template("register_.html",login="/user",register='/userregact',endUser= "User")


@app.route("/userregact", methods = ['GET','POST'])
def user_regact():
    try:
        if request.method == 'POST':
            status = user_reg(request.form['username'],request.form['password'],request.form['dob'],request.form['email'],request.form['city'],request.form['contactno'])
            if status == True:
                return render_template("login_.html",login="/userlogact",register="/userreg",endUser= "User",image ="loginUser.svg",m1="Registration Success")
            else:
                return render_template("register_.html",login="/user",register='/userregact',endUser= "User")
    except Exception as err:
        message = registration_validation(err,"user")
        return render_template("register_.html",login="/user",register='/userregact',endUser= "User",message=message)




@app.route("/userhome")
def user_home():
      return render_template("userHome_.html",endUser= "User")

@app.route("/vf/")
def user_vf():
       viewfile = user_viewfile()
       return render_template("userViewFiles_.html", viewfiledata = viewfile)

@app.route("/vf1/", methods = ['GET', 'POST'])
def user_vf1():
        fname = request.args.get('filename')
        owner = request.args.get('owner')
        check = user_viewfiledata(fname,owner,session['email'])
        if check == True:
         return render_template("userViewFiles_.html",m1="Request_success") 
        else:
         return render_template("userViewFiles_.html",m1="Request_failed") 
            

@app.route("/download/")
def user_download():
    downloaddata = user_down(session['email'])
    return render_template("userVerify_.html", downloads = downloaddata)

@app.route("/downloadact/" , methods = ['GET', 'POST'])
def user_downloadact():
    fname = request.args.get('fname')
    return render_template("userDownload_.html", filename = fname)




@app.route("/ownerhome")
def FUN_ownerhome():
    return render_template("ownerHome_.html",endUser= "Owner")

@app.route("/Upload", methods = ['GET','POST'])
def owner_upload():
    try:
        if request.method == 'POST':
            file = request.files['inputfile']
            # print(file.read())
            file_name = file.filename
            create_newFile_path = file_name
            #   print(type(create_newFile_path))
            #   print(type(file_name))
            with open(create_newFile_path,"wb") as file_write:
                file_write.write(file.read())

            fileEncoding(create_newFile_path)
            file = open("demofile.txt","rb")
            #   file_name = request.files.id
            fname = file_name
            owner = session['username']
            data = file.read()
            #   data.decode()
            check = upload_file(file_name,file,owner)
            owner_split(fname,owner,data.decode('utf-8'))
            if check == True:
                return render_template("fileUpload_.html",m1="success")
            else:
                return render_template("fileUpload_.html",m1="Failed")
    except:
        return render_template("fileUpload_.html",m1="Failed")
    finally:
        # if os.path.exists("demofile.txt"):
        #     os.remove("demofile.txt")
        # else:
        #     print("demo file does not exist")
        if os.path.exists(file_name):
            os.remove(file_name)
        else:
            print(" file does not exist")

@app.route("/fileupload")
def FUN_fileupload():
         return render_template("fileUpload_.html")

@app.route("/ownerviewfiles")
def FUN_ownerviewfiles():
    viewdata = owner_viewfiles(session['username'])
    return render_template("ownerViewFiles_.html",showdata = viewdata)


def owner_split(fname,owner,data):

    size = len(data)
    l=len(data)
    leng=len(data)//3
    length=len(data)//2
    s1 = leng+leng  
    k = s1+leng    
    le = 1
    halfString=data[0:leng]
    second = data[leng:s1]
    third = data[s1:l]
    
   #   DES PART
    DESkey_16 = os.urandom(8)     
    d = des()
    encodedkey1 = base64.b64encode(DESkey_16)
    strkey = str(encodedkey1, 'utf-8')
    desencrypted = d.encrypt(DESkey_16,halfString,padding=True)

    fileDES= open("C:/Users/user/OneDrive/Desktop/input/DES.txt", "w")
    fileDES.write(str(desencrypted.encode("utf-8")))
    fileDES.close()
    start()
    uploadFile('DES.txt',"C:/Users/user/OneDrive/Desktop/input/DES.txt")
    # AES PART
    AESkey_16 = os.urandom(16) 
    aescipher = AESCipher(AESkey_16)   
    encodedkey = base64.b64encode(AESkey_16)
    strkey1 = str(encodedkey, 'utf-8')
    aesencrypted = aescipher.encrypt(second)
   
    fileAES= open("C:/Users/user/OneDrive/Desktop/input/AES.txt", "w")
    fileAES.write(str(aesencrypted))
    fileAES.close()
    
    uploadFile('AES.txt',"C:/Users/user/OneDrive/Desktop/input/AES.txt")

    #RSA ORIGHINAL
    key_pair = generate(8)

    public_key = key_pair["public"]
    private_key = key_pair["private"]

     #Now encrypt
    ciphertext = encrypt(public_key, third)
    txt = ', '.join(map(lambda x: str(x), ciphertext))

    fileRSA= open("C:/Users/user/OneDrive/Desktop/input/RSA.txt", "w")
    fileRSA.write(txt)
    fileRSA.close()
    uploadFile('RSA.txt',"C:/Users/user/OneDrive/Desktop/input/RSA.txt")
    val = ', '.join(map(lambda x: str(x), private_key))
    
    close()
    status = upload_clouddata(data,fname.rstrip(),owner,desencrypted,strkey,aesencrypted,strkey1,str(txt),str(val))
    return render_template("ownerViewFiles_.html",m1="sucess")

@app.route("/viewencfiles")
def owner_viewencfiles():
    splitdata = onwer_viewdata(session['username'])
    return render_template("viewencfiles.html",spliinfo = splitdata)

@app.route("/vuserreq")
def owner_vuserreq():
    userrequest = user_request(session['username'])
    return render_template("ownerViewRequests_.html",userreqdata = userrequest)

@app.route("/logout")
def FUN_logout():
    return render_template("index_.html")

@app.route("/response", methods = ['GET','POST'])
def owner_response():
    fname1 = request.args.get('filename')
    owner1 = request.args.get('owner')
    email1 = request.args.get('email')
    result = owner_request(fname1,owner1,email1)   
    rdata = result    
    status = owner_update(rdata,fname1,owner1,email1)
    if status == True:
        for skey,skey1,skey2 in rdata:
            # print(skey,skey1,skey2)
            stringkeys = 'fi'+skey+'se'+skey1+'co'+skey2+'th'
            sendmail(stringkeys,email1)
            
            print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
                            
        return redirect(url_for('owner_vuserreq'))
    else:
        return render_template("ownerViewRequests_.html",m1="false")  


@app.route("/download_file/", methods = ['GET','POST'])
def user_download_file():
    fname = request.args.get('filename')
    
    return send_file(fname, as_attachment=True) #render_template("userHome_.html")

@app.route("/verify", methods = ['GET','POST'])
def user_verfiy3():
    fileImage = request.files['inputImage']
    #print(fileImage)
    filename  = request.form['filename']
    fileImage = lsb.reveal(fileImage)
    #print(fileImage) # show the keys
    left = 'fi'
    right = 'se'
    left1= 'se'
    right1 = 'co'
    left2 = 'co'
    right2 = 'th'
                          
    key1 = fileImage[fileImage.index(left)+len(left):fileImage.index(right)]
    key2 = fileImage[fileImage.index(left1)+len(left1):fileImage.index(right1)]
    key3 = fileImage[fileImage.index(left2)+len(left2):fileImage.index(right2)]

    dats=user_finaldown(filename,key1,key2,key3)
    try:
        dats=user_finaldown(filename,key1,key2,key3)
        if dats:
            for filename,owner in dats:
                fdata = user_lastdownload(filename,owner)
                if fdata:
                    for skey,skey1,skey2,f1,f2,f3 in fdata:
                        #   DES PART
                        decodedkey = base64.b64decode(key1) 
                        descipherdec = des()   
                        desdecrypted = descipherdec.decrypt(decodedkey,f1,padding=True)
                        #   AES PART
                        decodedkey1 = base64.b64decode(key2)            
                        aescipherdec = AESCipher(decodedkey1)   
                        aesdecrypted = aescipherdec.decrypt(f2)
                         #   RSA PART
                        rsaencrypteddata = list(f3.split(", "))
                        rsapublickey = tuple(key3.split(", ")) 
                        rsadeciphertext = decrypt(rsapublickey, rsaencrypteddata)
           
                totaldata = desdecrypted+aesdecrypted+rsadeciphertext
                with open(filename,"wb") as final_file:
                    k = base64.b64decode(totaldata)
                    final_file.write(k)
            #    print('totaldata: %s' % totaldata) 
                
                file1 = open("C:/Users/user/OneDrive/Desktop/input/myfile.txt","w") 
                file1.write(totaldata) 
            #    fileDecoding(filename)

            return send_file(filename, as_attachment=True) 
        else:
            return render_template("userVerify_.html",m2="downlaod failed")
    except:
        return render_template("userVerify_.html",m2="downlaod failed")
    finally:
        if os.path.exists(filename):
            print("file deleted with file name: "+filename)
            # os.remove(filename)
        else:
            print(" file does not exist")
def registration_validation(e,endUser):
    err = str(e)
    # print(err)

    if(err == "UNIQUE constraint failed: "+endUser+".username"):
        err = "Username already exists"
    elif(err == "UNIQUE constraint failed: "+endUser+".email"):
        err = "Email already exists"
    return err
@app.route("/logout")
def admin_logout():
    return render_template("index_.html")
if __name__ == "__main__":
   app.run(debug=True,host='127.0.0.1', port=5002)

