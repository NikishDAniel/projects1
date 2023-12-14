'''
Outline --
    -- 'What is our application' 
    -- necessary packages and libraries
    '''
from customtkinter import *
from CTkMessagebox import *
from mysql.connector import *
myDataBase = connect(
    host = 'localhost',
    user = 'root',
    password = '3122003',
    database = 'myAppLogins'
)

myCursor = myDataBase.cursor()

def show():
    Name = name.get()
    pass1 = passwordMain.get()
    if Name == '':
        CTkMessagebox(main,title="ERROR MESSAGE",icon='cancel',message="Please enter your UserName")
    elif pass1 == '':
        CTkMessagebox(main,title="ERROR MESSAGE",icon='cancel',message="Please enter your Password")
    else:        
        CTkMessagebox(main,message=f"WELCOME {Name} !! ")
        name.delete(0,END)
        passwordMain.delete(0,END)
                       
def screen2():
        def saveUser():
            details = (useNAme.get(),password.get(),email.get())
            print(details)
            if details[0] == '' or details[1]=='' or details[2] == '':
                CTkMessagebox(main,title='INVALID ENTRY !!',icon = 'warning',message='INVALID ENTRY !!.. Please check your Name , Password & E-Mail')
            elif len(details[1])>=8:
                sql = 'insert into logins (name,password,email) values(%s,%s,%s)'
                myCursor.execute(sql,(details[0],details[1],details[2]))
                myDataBase.commit()
                CTkMessagebox(main,title='REGISTERED SUCCESSFULLY',icon='check',message='You are successfully registred your Account',option_1="Thanks")
            elif len(details[1])<8:
                CTkMessagebox(main,title='ERROR MESSAGE',icon='cancel',message='Your password must contains atleast 8 characters')
                
        for widget in main.winfo_children():
            widget.destroy()
        CTkLabel(main,text='Enter Your Name : ',text_color= 'white').grid(row = 0,column = 0)
        useNAme = CTkEntry(main,placeholder_text='Your name')
        useNAme.grid(row = 0 , column = 1)
        CTkLabel(main,text='Password : ',text_color= 'white').grid(row = 1,column = 0)
        password = CTkEntry(main,placeholder_text= 'Enter Your Password')
        password.grid(row = 1,column=1)
        CTkLabel(main,text= 'E-Mail',text_color='white').grid(row = 2,column = 0)
        email = CTkEntry(main,placeholder_text='Your E-Mail')
        email.grid(row = 2,column = 1)
        CTkButton(main,text='Submit',command=saveUser).grid(row = 4 , column = 1) 
       
main = CTk()
main.geometry('255x255')
set_appearance_mode('dark')
set_default_color_theme('dark-blue')
main.title('My First App')
name = CTkEntry(main,placeholder_text="Your UserName ")
name.pack()
passwordMain = CTkEntry(main,placeholder_text='Your Password')
passwordMain.pack()
CTkButton(main,text="Login",command=show).pack()
CTkButton(main,text="Register",command=screen2).pack()
CTkButton(main,text = "close",command=main.destroy).pack()
main.mainloop()
