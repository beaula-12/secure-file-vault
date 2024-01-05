import base64
def fileEncoding(filename):
    with open(filename, "rb") as file:
        encoded_string = base64.b64encode(file.read())
        
        f = open("demofile.txt", "wb")
        f.write(encoded_string)
        f.close()
