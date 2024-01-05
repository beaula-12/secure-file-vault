import smtplib
import imghdr
from stegano import lsb  
from email.message import EmailMessage
def sendmail(stringkeys,Reciever_Email):
    # print(stringkeys)
    Sender_Email = "twinklebeaula@gmail.com"
    Password = "tcuhlkcyviqxsprm"

    #message hide in png file using lsb
    msg = lsb.hide("images/mailStegno.png",str(stringkeys)) #hide key in image
    msg.save("images/mailStegno.png") #save the embedded image
            

    newMessage = EmailMessage()                         
    newMessage['Subject'] = "Stegnographic key" 
    newMessage['From'] = Sender_Email                   
    newMessage['To'] = Reciever_Email                   
    newMessage.set_content('Keys are hidden in the image!') 

    with open('images/mailStegno.png', 'rb') as f:
        image_data = f.read()
        image_type = imghdr.what(f.name)
        image_name = f.name

    newMessage.add_attachment(image_data, maintype='image', subtype=image_type, filename=image_name)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(Sender_Email,Password)              
        smtp.send_message(newMessage)