from customtkinter import *
from PIL import ImageTk, Image
from customtkinter import filedialog
from modules.libs import Encode, Decode
from modules.AES import AESCipher
import tkinter as tk
import base64
from image.exp import explode
from io import BytesIO

root = CTk()
root.title('Image Steganography')
# root.geometry("885x572")
root.minsize(885, 585)
set_default_color_theme("dark-blue")
set_appearance_mode("system")

app = CTkScrollableFrame(root)
app.pack(fill=BOTH, expand=1)

left_frame = CTkFrame(app, border_width=3)
right_frame = CTkFrame(app,border_width=3)

def clear_frame(frame):
   for widgets in frame.winfo_children():
      widgets.destroy()

def getImage(image):
    if image == ".\\image\\imageico.jpg" or "":
        byte_data = base64.b64decode(explode)
        image_data = BytesIO(byte_data)
        img_old = Image.open(image_data)
    else:
        img_old=Image.open(image)
    width, height = img_old.size  
    scale=float(400/width)
    img_resized=img_old.resize((int(width*scale),int(height*scale)))
    my_img=ImageTk.PhotoImage(img_resized)
    return my_img

def encode_widgets():
    global left_frame, right_frame
    clear_frame(left_frame)
    clear_frame(right_frame)
    # top_frame(app, "Encode")
    def form_widgets(frame):
        def open_image():
            global file_path
            file_path = filedialog.askopenfilename(initialdir="/", title="Open Image", filetypes=(("IMG","*.png"), ("IMG","*.jpeg"), ("IMG","*.jpg")))
            if file_path != "":
                password_text.configure(state=NORMAL)
                password_text.delete(0, END) 
                message_box.configure(state=NORMAL)
                message_box.delete(1.0, "end-1c") 
                img_label.configure(image=getImage(file_path))
                img_path.configure(text=file_path)
                gen_button.configure(state=NORMAL)
                lbl_enc_stat.configure(text="")

        def generateStegoImage(frame):
            if file_path != "":
                password = password_text.get()
                message = message_box.get(1.0, "end-1c")
                aes = AESCipher()
                encryped_message = aes.encrypt(message, password)
                encoded = Encode(file_path, encryped_message)
                save_path = filedialog.asksaveasfile(defaultextension=".png",filetypes=[("Image","*.png")])
                if save_path:
                    # print(save_path)
                    encoded.download(save_path.name)
                    lbl_enc_stat.configure(text="Stego Image Generated and Saved!")
                encoded.debugInfo()

        select_img_button = CTkButton(frame, text="Open Image", command=open_image)
        password_label = CTkLabel(frame, text="Enter Password : ")
        password_text = CTkEntry(frame, width=200, show="*", state=DISABLED)
        message_label = CTkLabel(frame, text="Enter the Message : ")
        message_box = CTkTextbox(frame, width=350,height=200, state=DISABLED, font=("Segoe-UI", 18))
        gen_button = CTkButton(frame, text="Generate Stego Image", state=DISABLED, command=lambda:generateStegoImage(frame))
        lbl_enc_stat = CTkLabel(frame, text="")

        select_img_button.grid(row=0, column=0, padx=10, columnspan=2, pady=20)
        password_label.grid(row=1, column=0, padx=10, pady=10, sticky="E")
        password_text.grid(row=1, column=1, padx=10, pady=10)
        message_label.grid(row=2, column=0, padx=10, sticky="SE", pady=10)
        message_box.grid(row=3, column=0, columnspan=2, padx=25, sticky="WE" )
        gen_button.grid(row=4, column=0, padx=10, columnspan=2, pady=10)
        lbl_enc_stat.grid(row=5, column=0, padx=10,pady=10, columnspan=2)

    app.enc_file = '.\\image\\imageico.jpg'
    def img_widgets(frame):
        global img_label, img_path, img_btn
        img_label = CTkLabel(frame, image=getImage(app.enc_file), text="", width= 400, height=400)
        img_path = CTkLabel(frame, text="")

        img_label.grid(row=0,column=0, padx=10, pady=10)
        img_path.grid(row=1, column=0, pady=10, padx=10)
        

    left_frame.grid(row=1, column=0, padx=10, pady=10, sticky=(N,S,E,W))
    form_widgets(left_frame)

    right_frame.grid(row=0, column=1, padx=10, pady=10, rowspan=10, sticky=(N,S,E,W))
    img_widgets(right_frame)


def decode_widgets():
    global left_frame, right_frame
    clear_frame(left_frame)
    clear_frame(right_frame)
    top_frame(app, "Decode")
    def form_widgets(frame):
        def open_image():
            global file_path
            file_path = filedialog.askopenfilename(initialdir="/", title="Open Image", filetypes=(("IMG","*.png"), ("IMG","*.jpeg"), ("IMG","*.jpg")))
            if file_path != "":
                password_text.configure(state=NORMAL)
                password_text.delete(0, END) 
                # message_box.configure(state=NORMAL)
                # message_box.delete(1.0, "end-1c") 
                img_label.configure(image=getImage(file_path))
                img_path.configure(text=file_path)
                gen_button.configure(state=NORMAL)
                lbl_dec_stat.configure(text="")

        def decode_and_decrypt(frame):
            dec_message.delete(1.0, "end-1c")
            if file_path != "":
                password = password_text.get()
                decoded = Decode(file_path)
                if decoded.secret_encryped_message:
                    aes = AESCipher()
                    decrpted_message = aes.decrypt(decoded.secret_encryped_message, password)
                    if decrpted_message:
                        # print(f"Hidden Message: {decrpted_message}")
                        lbl_dec_stat.configure(text="Decryption Successful")
                        dec_message.configure(state=NORMAL)
                        dec_message.insert("0.0", decrpted_message)
                    else:
                        lbl_dec_stat.configure(text="Decryption Failed! Invalid Password or Image")
                else:
                    lbl_dec_stat.configure(text="Decryption Failed! Invalid Password or Image")
                decoded.debugInfo()
            else:
                lbl_dec_stat.configure(text="Decryption Failed! Invalid Password or Image")

            lbl_dec_stat.grid(row=5, column=0, columnspan=3)

        select_img_button = CTkButton(frame, text="Open Stego Image", command=open_image)
        password_label = CTkLabel(frame, text="Enter Password : ")
        password_text = CTkEntry(frame, width=200, show="*", state=DISABLED)
        gen_button = CTkButton(frame, text="Decrypt and Display Message", state=DISABLED, command=lambda:decode_and_decrypt(frame))
        lbl_dec_stat = CTkLabel(frame, text="")
        dec_message = CTkTextbox(frame, width=350, height=200, state=DISABLED, font=("Segoe-UI", 18))


        select_img_button.grid(row=0, column=0, columnspan=2, pady=20)
        password_label.grid(row=1, column=0, padx=10, pady=10, sticky="E")
        password_text.grid(row=1, column=1,padx=10, pady=10)
        gen_button.grid(row=3, column=0,padx=10, columnspan=2, pady=10)
        lbl_dec_stat.grid(row=4, column=0,padx=10, columnspan=2)
        dec_message.grid(row=6, column=0, columnspan=4, pady=20, padx=25, sticky="WE")


    app.enc_file = '.\\image\\imageico.jpg'
    def img_widgets(frame):
        global img_label, img_path
        img_label = CTkLabel(frame, image=getImage(app.enc_file), text="", width= 400, height=400)
        img_path = CTkLabel(frame, text="")

        img_label.grid(row=0,column=0, padx=10, pady=10)
        img_path.grid(row=1, column=0, padx=10, pady=10)
        
    left_frame.grid(row=1, column=0, padx=10, pady=10)
    form_widgets(left_frame)

    right_frame.grid(row=0, column=1, padx=10, pady=10, rowspan=2, sticky=(N,S,E,W))
    img_widgets(right_frame)

def load_gui(mode : str):
    if(mode == "Encode"):
        encode_widgets()
    else:
        decode_widgets()


def top_frame(frame, mode):
    def change_scaling_event(new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        set_widget_scaling(new_scaling_float)

    upper_frame = CTkFrame(frame, border_width=3)
    upper_frame.grid(row=0,column=0, pady=10, padx=10,sticky=(N,E,W))

    optionmenu_1 = CTkOptionMenu(upper_frame, values=["Encode", "Decode"], command=load_gui)
    optionmenu_1.grid(row=0, column=0, pady=20, padx=25)
    optionmenu_1.set(mode)

    scaling_optionemenu =CTkOptionMenu(upper_frame, values=["80%", "90%", "100%", "110%", "120%"], command=change_scaling_event)
    scaling_optionemenu.grid(row=0, column=1, padx=25, pady=20)
    scaling_optionemenu.set("100%")

top_frame(app, "Encode")
encode_widgets()

root.mainloop()