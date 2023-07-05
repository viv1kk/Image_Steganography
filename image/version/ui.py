from customtkinter import *
from PIL import ImageTk, Image
from customtkinter import filedialog
from modules.libs import Encode, Decode
from modules.AES import AESCipher
import tkinter as tk

root = CTk()
root.title('Image Steganography')
root.geometry("500x500")

frame = CTkScrollableFrame(root)
frame.pack(fill=BOTH, expand=1)

app = CTkFrame(frame)
app.grid(row=1, column=0)

def change_scaling_event(new_scaling: str):
    new_scaling_float = int(new_scaling.replace("%", "")) / 100
    set_widget_scaling(new_scaling_float)

def clear_frame():
   for widgets in app.winfo_children():
      widgets.destroy()

def encodeWidgets(app):
    clear_frame()
    global  lab1, btn_open, lab2, passw, lab3, msg, enc
    def addDefaultImage(image):
        global l1
        img_old=Image.open(image)
        width, height = img_old.size  
        scale=float(400/width)
        img_resized=img_old.resize((int(width*scale),int(height*scale)))
        my_img=ImageTk.PhotoImage(img_resized)
        l1= CTkLabel(app,image=my_img, text="", width= 400, height=400)
        l1.grid(row=0,column=0, columnspan=3)

    app.enc_file = './image/imageico.jpg'
    def openImg():
        msg = filedialog.askopenfilename(initialdir="/", title="Choose a File", filetypes=(("png files","*.png"), ("all files","*")))
        print("\n\nFile -> "+app.enc_file)
        if msg == "":
            # addDefaultImage('./image/imageico.jpg')
            pass
        else:
            l1.grid_forget()
            app.enc_file = msg
            addDefaultImage(app.enc_file)
            lbl = CTkLabel(app, text= app.enc_file)
            lbl.grid_forget()
            lbl.grid(row=1, column=0, columnspan=3)


    def encode():
        if app.enc_file == "" or app.enc_file == "./image/imageico.jpg":
            print("Error: Load Image")
        else:
            password = passw.get()
            message = msg.get(1.0, "end-1c")
            aes = AESCipher()
            encryped_message = aes.encrypt(message, password)
            encoded = Encode(app.enc_file, encryped_message)
            app.dl = f = filedialog.asksaveasfile(defaultextension=".png",filetypes=[("Image","*.png")])
            if app.dl:
                print(app.dl)
                encoded.download(app.dl.name)
                lbl_enc_stat = CTkLabel(app, text="Stego Image Generated and Saved!")
                lbl_enc_stat.grid(row=6, column=0, columnspan=3)
            encoded.debugInfo()

    addDefaultImage(app.enc_file)
    lab1 = CTkLabel(app, text="Select Image : ")
    btn_open = CTkButton(app, text="Open Image", command=openImg)
    lab2 = CTkLabel(app, text="Input Password : ")
    passw = CTkEntry(app, width=400, show="*")
    lab3 = CTkLabel(app, text="Message : ")
    msg = CTkTextbox(app, width=400)
    enc = CTkButton(app, text="Generate Stego Image", command=encode)

    lab1.grid(row=2, column=0)
    btn_open.grid(row=2, column=1)
    lab2.grid(row=3, column=0)
    passw.grid(row=3, column=1, columnspan=2)
    lab3.grid(row=4, column=0)
    msg.grid(row=4, column=1, columnspan=2)
    enc.grid(row=5, column=0, columnspan=3)


def decodeWidgets(app):
    clear_frame()
    global  lab1, btn_open, lab2, passw, lab3, msg, enc, lbl, lbl_dec_stat, text_1
    def addDefaultImage(image):
        global l1
        img_old=Image.open(image)
        width, height = img_old.size  
        scale=float(400/width)
        img_resized=img_old.resize((int(width*scale),int(height*scale)))
        my_img=ImageTk.PhotoImage(img_resized)
        l1=CTkLabel(app,image=my_img, text="", width= 400, height=400)
        l1.grid(row=2,column=0, columnspan=3)

    app.dec_file = './image/imageico.jpg'
    def openImg():
        msg = filedialog.askopenfilename(initialdir="/", title="Choose a File", filetypes=(("png files","*.png"), ("all files","*")))
        print("\n\nFile -> "+app.dec_file)
        if msg == "":
            # addDefaultImage('./image/imageico.jpg')
            pass
        else:
            l1.grid_forget()
            app.dec_file = msg
            addDefaultImage(app.dec_file)
            lbl = CTkLabel(app, text= app.dec_file)
            lbl.grid(row=1, column=0, columnspan=3)

    lbl_dec_stat = CTkLabel(app, text="")
    lbl_dec_stat.grid(row=5, column=0, columnspan=3)

    text_1 = CTkTextbox(app)

    def decode():
        global lbl_dec_stat, text_1
        lbl_dec_stat.grid_forget()
        text_1.grid_forget()
        text_1 = CTkTextbox(app, width=600, height=100)
        lbl_dec_stat = CTkLabel(app, text="Decryption Failed, Please Input correct Password and Image")

        if app.dec_file == "" or app.dec_file == "./image/imageico.jpg":
            print("Error: Load Image")
        else:
            password = passw.get()
            decoded = Decode(app.dec_file)
            try:
                if decoded.secret_encryped_message:
                    decoded.debugInfo()
                    aes = AESCipher()
                    decrpted_message = aes.decrypt(decoded.secret_encryped_message, password)
                    if decrpted_message:
                        # print(f"Hidden Message: {decrpted_message}")

                        
                        lbl_dec_stat = CTkLabel(app, text="Decryption Successful")

                        text_1.grid(row=6, column=0, columnspan=4, pady=10, padx=10)
                        text_1.insert("0.0", decrpted_message)
                    else:
                        # lbl_dec_stat.grid_forget()
                        pass
                else:
                    
                    # lbl_dec_stat.grid_forget()
                    pass
            except: 
                
                # lbl_dec_stat.grid_forget()
                pass
                
            lbl_dec_stat.grid(row=5, column=0, columnspan=3)

    
    addDefaultImage(app.dec_file)
    lab1 = CTkLabel(app, text="Select Image : ")
    btn_open = CTkButton(app, text="Open Image", command=openImg)
    lab2 = CTkLabel(app, text="Input Password : ")
    passw = CTkEntry(app, width=400, show="*")
    enc = CTkButton(app, text="Decrypt & Extract Message", command=decode)
    # lab3 = CTkLabel(app, text="Message : ")
    # msg = CTkTextbox(app, width=400, state=DISABLED)

    lab1.grid(row=0, column=0)
    btn_open.grid(row=0, column=1)
    lab2.grid(row=3, column=0)
    passw.grid(row=3, column=1, columnspan=2)
    enc.grid(row=4, column=0, columnspan=3)
    # lab3.grid(row=6, column=0)
    # msg.grid(row=6, column=1, columnspan=2)

def loadgui(option: str):
    if(option == "Encode"):
        encodeWidgets(app)
    else:
        decodeWidgets(app)

frame_1 = CTkFrame(frame)
frame_1.grid(row=0,column=0, pady=5, padx=0)

optionmenu_1 = CTkOptionMenu(frame_1, values=["Encode", "Decode"], command=loadgui)
optionmenu_1.grid(row=0, column=0, pady=10, padx=10)
optionmenu_1.set("Encode")


scaling_optionemenu =CTkOptionMenu(frame_1, values=["80%", "90%", "100%", "110%", "120%"], command=change_scaling_event)
scaling_optionemenu.grid(row=0, column=3, padx=0, pady=10)
scaling_optionemenu.set("100%")

encodeWidgets(app)
root.mainloop()