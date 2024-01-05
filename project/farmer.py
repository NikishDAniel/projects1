# importing necessary libraries for our application
from customtkinter import *
from tkintermapview import *
from CTkMessagebox import *
from PIL import Image
#import getpass
from mysql.connector import *

# my Data table connection
mydataBase = connect(
    host = 'localhost',
    user = 'root',
    password = '3122003',
    database = 'project'
)
myCursor = mydataBase.cursor()
menuOption = 0

#a function to create or show screen  
def showScreen(num,colour,userName = None):
    global menuOption
    
    def fetch():
        myCursor = mydataBase.cursor()
        myCursor.execute(f'select role from logins where name = "{userName}"')
        userRole = myCursor.fetchone()[0]
        myCursor.close() 
        return userRole
        
    # taking details
    def takeFarmerDetails(column,pos):
        myCursor = mydataBase.cursor()
        myCursor.execute(f'Select {column},farmer from items where location = "{str(pos[0])+","+str(pos[1])}"')
        item , name = myCursor.fetchone()
        myCursor.close()
        return (item,name)
        
    # take initial message box position
    def takeStart(event):
        global start,start1
        start = event.x
        start1 = event.y
    
    # shows details of the farmer and allows to ask/set kg of items 
    def showDetails(pos):
        
        # make message box movable  
        def moveable(event):
            if start is not None:
                x = consumerFrame.winfo_x()+(event.x-start)
                y = consumerFrame.winfo_y()+(event.y - start1)
                consumerFrame.place(x=x,y=y)
        
        # setting quantity add
        def addQuantity(value,price):
            priceLabel.set(eval(f'{price}*({value}+1)'))
            quantity.set(eval(f'{value}+1'))
        
        # setting quantity reduce
        def reduceQuantity(value,price):
            if value > 1:
                priceLabel.set((value-1)*price)
                quantity.set(value-1) 
            else:
                priceLabel.set(price)
                quantity.set(value)
            
        quantity = StringVar(value=1)
        consumerFrame = CTkFrame(main,width = 350,height=210,fg_color='grey23' if colour == 'white' else 'gainsboro')
        consumerFrame.place(x=10,y=10)
        topFrame = CTkFrame(consumerFrame,width=350,height=30,fg_color='grey7' if colour == 'white' else 'white',bg_color='grey7' if colour == 'white' else 'gainsboro')
        topFrame.place(x=0,y=0)
        price,framerName = takeFarmerDetails('price',pos)
        priceLabel = StringVar(value=price)
        CTkLabel(consumerFrame,text=f'Name : {framerName}\nPrice : {price}\nLocation : {pos}',text_color=colour).place(x=0,y=50)
        CTkButton(topFrame,width=10,height=30,text='',fg_color='grey7',bg_color='grey7',image=CTkImage(Image.open(r'C:\Users\Nikish daniel\Downloads\close-red-icon.webp'),size=(25,25)),command=consumerFrame.destroy).place(x=310,y=0)
        CTkLabel(consumerFrame,text='Please note that this price is not stable. Make a request and wait for the response.\nThe prices may change/got updated by the farmer.',text_color=colour,font=('Times New Roman', 10, 'bold')).place(x=0,y=120)
        CTkEntry(consumerFrame,text_color=colour,state=DISABLED,textvariable=quantity,width=40).place(x=10,y=70)
        CTkEntry(consumerFrame,text_color=colour,state=DISABLED,textvariable=priceLabel,width=60).place(x=100,y=70)
        CTkButton(consumerFrame,text='Confirm',width=50).place(x=160,y=160)
        CTkButton(consumerFrame,text='+',width=15,height=10,fg_color='black',command=lambda :addQuantity(quantity.get(),price)).place(x=160,y=125)
        CTkButton(consumerFrame,text='-',width=18,height=10,fg_color='black',command=lambda :reduceQuantity(int(quantity.get()),price)).place(x=100,y=125)
        consumerFrame.bind('<ButtonPress-1>',takeStart)
        consumerFrame.bind("<B1-Motion>",moveable)
             
    # price update by the farmers
    def pricePopUp(pos):
        
        # make message box movable  
        def moveable1(event):
            x = popUpFrame.winfo_x()+(event.x-start)
            y = popUpFrame.winfo_y()+(event.y - start1)
            popUpFrame.place(x=x,y=y)
            
        def priceUpdate():
            myCursor = mydataBase.cursor()
            myCursor.execute(f'update items set price = "{updatedPrice.get()}" where location = "{str(pos[0])+","+str(pos[1])}"')
            mydataBase.commit()
            myCursor.close()
            popUpFrame.destroy()
            CTkMessagebox(main,icon='check',title='Successfully Updated',message="Your item's price is successfully updated")
                    
        item, name = takeFarmerDetails('item',pos)
        myCursor = mydataBase.cursor()
        myCursor.execute(f"select price from items where location = '{str(pos[0])+','+str(pos[1])}'")
        priceVal = myCursor.fetchone()[0]
        myCursor.close()
        price = StringVar(value=priceVal)
        popUpFrame = CTkFrame(main,width = 350,height=190,fg_color='grey23' if colour == 'white' else 'gainsboro')
        popUpFrame.place(x=10,y=10)
        topFrame = CTkFrame(popUpFrame,width=350,height=30,fg_color='grey7' if colour == 'white' else 'white',bg_color='grey7' if colour == 'white' else 'gainsboro')
        topFrame.place(x=0,y=0)
        CTkLabel(popUpFrame,text=f'Welcome back {name}\nAdd/Update the price of your {item} you sell').place(x=0,y=50)
        updatedPrice = CTkEntry(popUpFrame,text_color=colour,textvariable=price)
        updatedPrice.place(x=80,y=85)
        CTkButton(popUpFrame,text='ok',text_color=colour,command=priceUpdate).place(x=70,y=125)
        CTkButton(popUpFrame,text='cancel',text_color=colour,command=popUpFrame.destroy).place(x=175,y=125)
        popUpFrame.bind('<ButtonPress-1>',takeStart)
        popUpFrame.bind("<B1-Motion>",moveable1)
        
    # right click menu
    def addPlace(coor):
        myCursor = mydataBase.cursor()
        item = CTkInputDialog(title='Item',text='Add the item you sell')
        myCursor.execute('insert into items(item,location,price,farmer) values(%s,%s,%s,%s)',(item.get_input(),','.join([str(coor[0]),str(coor[1])]),'0',userName))
        mydataBase.commit()
        myCursor.close()
        
    # set theme
    def theme(option):
        global menuOption
        menuOption = 0
        set_appearance_mode(option)
        showScreen(1,'black') if option=='Light' else showScreen(1,'white')       
    
    #close confirmation
    def screenClose():
        option = CTkMessagebox(main,icon='question',title='CONFORMATION',message='Would you like to close this screen ? You need to login once again to view this screen',option_1='Yes',option_2='No')
        if option.get() == 'Yes':
            showScreen(1,colour,None)
    
    # function to check or fetch datas from the logins table
    def getDatas(data,operation,name):
        myCursor = mydataBase.cursor()
        sql = f"select {data} from logins where {operation} = '{name}'"
        myCursor.execute(sql)
        data = myCursor.fetchall()
        myCursor.close()
        return data     
    
    # clear entry function 1
    def clear1():
        userName1.delete(0,END)
        password1.delete(0,END)
        email.delete(0,END)
    
    # clear entry function 0
    def clear():
        userName.delete(0,END)
        password.delete(0,END) 
    
    # login check function    
    def check():
        details = (userName.get(),password.get())
        
        # checking for null entry
        if details[0] == '' or details[1] == '':
            CTkMessagebox(main,title="ERROR MESSAGE",icon='cancel',message="Please check your UserName and Password")
        
        # check for the correctness of the data
        else: 
            datas = getDatas('Name,Password','Name',details[0]) 
            if len(datas)==1 and datas[0]==details:     
                option1 = CTkMessagebox(main,message=f"WELCOME {details[0]} !! ",option_1='Next',option_2='Cancel')
                showScreen(3,colour,userName.get()) if option1.get()=='Next' else clear()            
            else:
                option = CTkMessagebox(main,title='LOGIN ERROR',icon='cancel',message='Please Register before login . Already Registered ? Please verify your Password and wait few minutes and try again',option_1='Retry',option_2='Cancel')
                if option.get()=='Cancel':
                    clear()
                    
    # function for new registration
    def register():
        myCursor = mydataBase.cursor()
        details = [userName1.get()]+[password1.get()]+[email.get()]+[role.get()]
        datas = getDatas('Name','Name',details[0])
        emails = getDatas('Email','Email',details[2]) 
        
        # checking for the nullity entry       
        if len(details[0])==0 or len(details[1])==0 or len(details[2])==0:
            opinion = CTkMessagebox(main,title='LOGIN ERROR',icon='warning',message='Please check your UserName , Password , Email Id and set the Role!!',option_1='Retry',option_2='Close')
            if opinion.get() == 'Close':
                clear1()
        elif len(datas)==1:
            CTkMessagebox(main,icon='warning',title='LOGIN ERROR!!',message='This UserName already exist. Try login..')
        elif len(emails)==1:
            CTkMessagebox(main,title='LOGIN ERROR!!',icon='warning',message='This Email already exist.')
        elif len(details[1])>=8:
            myCursor.execute('insert into logins(Name,Password,Email,role) values(%s,%s,%s,%s)',details)
            mydataBase.commit()
            CTkMessagebox(main,title='REGISTERED SUCCESSFULLY',icon='check',message='You are successfully registred your Account')
            myCursor.close()
            clear1()
        else:
            CTkMessagebox(main,title='Password Error',icon='cancel',message='Password needs to have atleast 8 characters !')
    
    # search by location and mapping based on the location list
    def marker(status,locationsList = None):
        if locationsList:
            for i in locationsList:
                i = str(i).replace('(','').replace(')','').replace("'",'')
                loc = i.split(',')
                map.set_marker(float(loc[0]),float(loc[1]),text=items.get(),text_color = 'black',marker_color_circle = 'white',command=lambda x : pricePopUp(x.position) if fetch() == 'farmer' else showDetails(x.position))
        else:
            map.set_address(location.get(),marker=status)
    
    # take locations wrt items
    def takeLocations():
        myCursor = mydataBase.cursor()
        myCursor.execute(f"select location from items where item = '{items.get()}'")
        locationList = myCursor.fetchall()
        myCursor.close()
        marker(True,locationList)
              
    # changing the type of map
    def mapWidget(option):
        if option=='Satellite':
            map.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga") 
        elif option == 'Street':
            map.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png") 
        else:
            map.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga")
    
    # setting the role entry        
    def setRoleEntry():
        roleEntry.insert(0,role)
        
    def showHover(event):
        global noticeLable
        noticeLable = CTkLabel(main,text='Notice: Kindly get your location from your Gmaps and Enter your location .\n If your location is not entered correct not to worry much , you can change your location on menu',text_color=colour,fg_color='black'if colour == 'white' else 'white',font=('Times New Roman', 10))
        noticeLable.place(x=180,y=(270-event.y))
        
    def hideHover(event):
        noticeLable.destroy()
        
    def changeLocation():
        CTkInputDialog(title='Change Your Location',text='Your past Location is ')
    
    # menu function        
    def menu():
        global menuOption
        if menuOption == 0:
            menuFrame = CTkFrame(main,width=125,height = 150,fg_color='white' if colour=='black' else 'black')
            menuFrame.place(x=390,y=30)
            CTkLabel(menuFrame,text='Theme',text_color=colour,font=('Times New Roman',15)).place(x=2,y=2)
            CTkOptionMenu(menuFrame,values=['Light','Dark'],command=theme,width=30).place(x=50,y=2)
            CTkButton(menuFrame,text='Change Location',width=80,command=changeLocation).place(x=7,y=40)
            menuOption = 1
        else:
            menuOption = 0
            showScreen(1,colour)
         
    # screen switch destroy prev screen    
    for i in main.winfo_children():
        i.destroy()
     
    # first screen   
    if num == 1:
        user = StringVar(value='nikis')
        pass354 = StringVar(value='daniel354')
        topFrame = CTkFrame(main,width = 520,height=30,fg_color='white' if colour=='black' else 'black')
        topFrame.place(x=0,y=0)
        menuImage = CTkImage(Image.open(r'C:\Users\Nikish daniel\Downloads\menu1-modified.png'))
        CTkButton(topFrame,text='menu',text_color=colour,height=26,width = 50,fg_color='white' if colour=='black' else 'black',image=menuImage,command=menu).place(x=442,y=0)
        CTkLabel(main,text='Vanakkam Nanba',text_color= 'red',font = ('Times New Roman',25),anchor='center').place(x=190,y=80)       
        CTkLabel(main,text='UserName',text_color=colour).place(x=170,y= 150)
        userName = CTkEntry(main,placeholder_text='Your UserName',textvariable=user)
        userName.place(x=240,y=150)
        CTkLabel(main,text='Password',text_color=colour).place(x=170,y=190)
        password = CTkEntry(main,placeholder_text='Your Password',textvariable=pass354,show = '*',width=130)
        password.place(x=240,y=190)
        CTkButton(main,text='Login',fg_color='red',width=70,image=CTkImage(Image.open(r'C:\Users\Nikish daniel\Downloads\redkey-modified.png')),command=check).place(x=190,y = 240) 
        CTkButton(main,text='Register',width=50,image=CTkImage(Image.open(r'C:\Users\Nikish daniel\Downloads\register.png')),command=lambda:showScreen(2,colour)).place(x=280,y=240)
        CTkButton(main,text='Close',hover_color='red',command=main.destroy).place(x=200,y = 320)
        
    # it shows second screen
    elif num == 2:
        role = StringVar(main,value='farmer')
        menuOption = 0
        col1 = 'gray8' if colour == 'white' else 'gainsboro'
        topFrame = CTkFrame(main,width=520,height=30,fg_color=col1,bg_color=col1)
        topFrame.place(x=0,y=0)
        CTkLabel(main,text='Registration form',text_color= colour,font = ('Times New Roman',25),anchor='center').place(x=190,y=60)
        CTkLabel(main,text='UserName',text_color='red').place(x=170,y=110)
        userName1 = CTkEntry(main,placeholder_text='Your UserName')
        userName1.place(x=240,y=110)
        CTkLabel(main,text='Password',text_color='red').place(x=170,y=150)
        password1 = CTkEntry(main,placeholder_text='Your Password',show = '*')
        password1.place(x=240,y=150)
        CTkLabel(main,text='Email Id',text_color='red').place(x=170,y=190)
        email = CTkEntry(main,placeholder_text='Your Email')
        email.place(x=240,y=190)
        CTkLabel(main,text='Role',text_color='red').place(x=170,y=230)
        roleEntry = CTkEntry(main,textvariable=role,state=DISABLED)
        roleEntry.place(x=240,y=230)
        CTkLabel(main,text='Location',text_color='red').place(x=170,y=270)
        locationEntry = CTkEntry(main,placeholder_text='Your location')
        locationEntry.place(x=240,y=270)
        locationEntry.bind('<Enter>',showHover)
        locationEntry.bind('<Leave>',hideHover)
        CTkRadioButton(main,text='Farmer',variable=role,value='farmer',command = setRoleEntry).place(x=200,y=320)
        CTkRadioButton(main,text='Consumer',variable=role,value='consumer',command = setRoleEntry).place(x=285,y=320)
        CTkButton(main,text='Submit',image=CTkImage(Image.open(r'C:\Users\Nikish daniel\Downloads\save1.jpg')),command=register,width=50).place(x= 200,y = 400)
        CTkButton(topFrame,text='',image=CTkImage(Image.open(r'C:\Users\Nikish daniel\Downloads\back-modified.png')),command=lambda:showScreen(1,colour),height=30,width=15).place(x=0,y=0)
    
    # if num is 3 then show thrid screen
    elif num == 3:
        menuOption=0
        leftFrame = CTkFrame(main,width=180,height=520)
        leftFrame.grid(row= 0,column=0,padx=0,pady=0)
        rightFrame = CTkFrame(main,width=320,height=520)
        rightFrame.grid(row=0,column=1,padx=0,pady=0)
        CTkLabel(leftFrame,text='Location',text_color=colour).place(x=10,y = 10)
        location = CTkEntry(leftFrame,placeholder_text='Search',width=130)
        location.place(x=10,y=35)
        CTkButton(leftFrame,text = '',image=CTkImage(Image.open(r'C:\Users\Nikish daniel\Downloads\search-modified.png')),command=lambda:marker(False),width=15,height=20).place(x=141,y=35)
        CTkLabel(leftFrame,text='Items',text_color=colour).place(x=10,y = 75)
        items = CTkEntry(leftFrame,placeholder_text='Search',width=130)
        items.place(x=10,y=100)
        CTkButton(leftFrame,text='',image=CTkImage(Image.open(r'C:\Users\Nikish daniel\Downloads\icons8-location-48.png')),command=takeLocations,width=15,height=20).place(x=141,y=100)
        map = TkinterMapView(rightFrame,width=425,height=650)
        map.grid(row= 1,padx=0,pady=0)
        map.set_address('tamil nadu')
        if fetch() == 'farmer':
            map.add_right_click_menu_command(label='Add Place',command=addPlace,pass_coords=True)
        CTkButton(rightFrame,text='',command=map.delete_all_marker,image=CTkImage(Image.open(r'C:\Users\Nikish daniel\Downloads\disable-location-3706160-3087334.png'),size=(18,18)),width=12,height=12,bg_color='white',fg_color='black',hover_color='white').place(x=290,y=45)
        CTkLabel(rightFrame,text='',image=CTkImage(Image.open(r'C:\Users\Nikish daniel\Downloads\globalre.png'),size=(26,26))).place(x=164,y=10)
        CTkOptionMenu(rightFrame,values=['Satellite','Normal','Street'],command=mapWidget).place(x=190,y=10)
        CTkButton(leftFrame,text='Back',command=screenClose).place(x=20,y=420)
        
                   
# main ctk screen and its necessaries
main = CTk()
main.geometry('520x520')
main.title('Farmers Friends')
#print(getpass.getuser())
main.resizable(False,False)
set_appearance_mode('Dark')
showScreen(1,'white')
main.mainloop()

#nikish
#daniel354
#9.672445,78.096734