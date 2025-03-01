from customtkinter import *
from CTkMessagebox import CTkMessagebox
from rembg import remove
import cv2 , pytesseract , numpy as np , smtplib , shutil , sys , email , re
from os import *
from tkinter import filedialog , font
from PIL import Image , ImageOps , ImageGrab , ImageFilter , ImageEnhance
from pywinstyles import set_opacity
from requests import get
from io import BytesIO
from collections import defaultdict
import email.encoders
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from CTkTable import CTkTable
from pandas import *
from translate import *

mouse = ''
greatest = []
fileFormat = [('JPEG Files','*.jpeg'),('PNG Files','*.png'),('PDF Files','*.pdf'),('All Files','*.*'),('ICO Files','*.ico'),('IM Files','*.im'),('WebP Files', '*.webp'),('BMP Files', '*.bmp'),]
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
greatestArea = off = 0
currentWidget = previous = current = original = None
textVisited = []
sliderFunctions = defaultdict(list)

filters = {'Invert':{'Size':[50,50],'Sliders':0,'Function':lambda:[filterApply(ImageOps.invert(imaged.convert("RGB"))) if imageChecker() else None]},'Remove BG':{'Size':[50,50],'Sliders':0,'Function':lambda:[filterApply(remove(imaged)) if imageChecker() else None]},'HSV-FULL Code':{'Size':[50,50],'Sliders':0,'Function':lambda:[filterApply(Image.fromarray(cv2.cvtColor(original,cv2.COLOR_RGB2HLS_FULL))) if imageChecker() else None]},'GreyScale':{'Size':[50,50],'Sliders':0,'Function':lambda:[filterApply(imaged.convert('L')) if imageChecker() else None]},'Cartoonize':{'Size':[50,50],'Sliders':0,'Function':lambda:[filterApply(Image.fromarray(cartoonize(cvImage))) if imageChecker() else None]},'Flip':{'Size':[50,50],'Sliders':0,'Function':lambda:[filterApply(ImageOps.flip(imaged)) if imageChecker() else None]},
           'Pencil Sketch Colour':{'Size':[50,100],'Sliders':1,'Function':lambda:[pencilFilter('Pencil Sketch Colour',1) if imageChecker() else None]},'Pencil Sketch Grey':{'Size':[50,100],'Sliders':1,'Function':lambda:[pencilFilter('Pencil Sketch Grey',0) if imageChecker() else None]},'Mirror':{'Size':[50,50],'Sliders':0,'Function':lambda:[filterApply(ImageOps.mirror(imaged)) if imageChecker() else None]},'Text Extract':{'Size':[50,150],'Sliders':0,'Operation':'extractFrame','Function':lambda:textExtractValue.set(pytesseract.image_to_string(imaged)) if imageChecker() else None},'Transpose':{'Size':[50,50],'Sliders':0,'Function':lambda:[filterApply(imaged.transpose(Image.TRANSPOSE)) if imageChecker() else None]},'Transverse':{'Size':[50,50],'Sliders':0,'Function':lambda:[filterApply(imaged.transpose(Image.TRANSVERSE)) if imageChecker() else None]},
           'Rotate':{'Size':[50,100],'Sliders':1,'Function':lambda:[rotateImage() if imageChecker() else None]},'Erosion':{'Size':[50,50],'Sliders':0,'Function':lambda:[filterApply(Image.fromarray(cv2.erode(original,np.ones((5,5), np.uint8),iterations=1))) if imageChecker() else None]},'Gradient Map':{'Size':[50,50],'Sliders':0,'Function':lambda:[filterApply(Image.fromarray(cv2.applyColorMap(cv2.cvtColor(original, cv2.COLOR_BGR2GRAY), cv2.COLORMAP_JET))) if imageChecker() else None]},'Certificate':{'Size':[50,100],'Sliders':0,'Operation':'sendMailCheck','Function':lambda:showTableFrame() if imageChecker() else None},'Blur':{'Size':[50,100],'Sliders':1,'Function':lambda:[filterApply(Image.fromarray(original).filter(ImageFilter.GaussianBlur(sliderFunctions['Blur'][0].get()))) if imageChecker() else None]},
           'Emboss':{'Size':[50,50],'Sliders':0,'Function':lambda:[filterApply(imaged.filter(ImageFilter.EMBOSS)) if imageChecker() else None]},'Edge Detect':{'Size':[50,50],'Sliders': 0,'Function':lambda:[filterApply(imaged.convert('L').filter(ImageFilter.FIND_EDGES)) if imageChecker() else None]},'Sharpen':{'Size':[50,50],'Sliders':0,'Function':lambda:[filterApply(imaged.filter(ImageFilter.SHARPEN)) if imageChecker() else None]},'Detail Enhance':{'Size':[50, 50],'Sliders':0,'Function':lambda:[filterApply(imaged.filter(ImageFilter.DETAIL)) if imageChecker() else None]},'Sepia':{'Size':[50, 50],'Sliders': 0,'Function':lambda:[filterApply(ImageEnhance.Color(imaged.convert("RGB")).enhance(0.5).convert("L").convert("RGB").point(lambda p:p*1.2 if p<200 else 255)) if imageChecker() else None]},
           'Brightness':{'Size':[50,100],'Sliders':1,'Function':lambda:[filterApply(ImageEnhance.Brightness(Image.fromarray(original)).enhance(sliderFunctions['Brightness'][0].get())) if imageChecker() else None]},'Contrast':{'Size':[50,100],'Sliders':1,'Function':lambda:[filterApply(ImageEnhance.Contrast(Image.fromarray(original)).enhance(sliderFunctions['Contrast'][0].get()//10)) if imageChecker() else None]},'Solarize':{'Size':[50,100],'Sliders':1,'Function':lambda:[filterApply(ImageOps.solarize(Image.fromarray(original),threshold=(sliderFunctions['Solarize'][0].get()*255))) if imageChecker() else None]},'Equalize':{'Size':[50,50],'Sliders':0,'Function':lambda:[filterApply(ImageOps.equalize(imaged.convert("RGB"))) if imageChecker() else None]},'Autocontrast':{'Size':[50,50],'Sliders':0,'Function':lambda:[filterApply(ImageOps.autocontrast(imaged.convert("RGB"))) if imageChecker() else None]},
           'Invert L':{'Size':[50,50],'Sliders':0,'Function':lambda:[filterApply(ImageOps.invert(imaged.convert("L")).convert("RGB")) if imageChecker() else None]},'Color Swap':{'Size':[50,50],'Sliders':0,'Function':lambda:[filterApply(imaged.convert("RGB").point(lambda p:255-p)) if imageChecker() else None]},'Emboss High':{'Size':[50,50],'Sliders':0,'Function':lambda:[filterApply(imaged.filter(ImageFilter.CONTOUR)) if imageChecker() else None]},'Min Filter':{'Size':[50,50],'Sliders':0,'Function':lambda:[filterApply(imaged.filter(ImageFilter.MinFilter(3))) if imageChecker() else None]},'Max Filter':{'Size':[50,50],'Sliders':0,'Function':lambda:[filterApply(imaged.filter(ImageFilter.MaxFilter(3))) if imageChecker() else None]},'Posterize':{'Size':[50,100],'Sliders':1,'Function':lambda:[filterApply(ImageOps.posterize(Image.fromarray(original).convert("RGB"),max(1,int(sliderFunctions['Posterize'][0].get()//32)))) if imageChecker() else None]},
           'Mode Filter':{'Size':[50,50],'Sliders':0,'Function':lambda:[filterApply(imaged.filter(ImageFilter.ModeFilter(3))) if imageChecker() else None]},'Edge Enhance':{'Size':[50,50],'Sliders':0,'Function':lambda:[filterApply(imaged.filter(ImageFilter.EDGE_ENHANCE)) if imageChecker() else None]},'Edge Enhance More':{'Size':[50,50],'Sliders':0,'Function':lambda:[filterApply(imaged.filter(ImageFilter.EDGE_ENHANCE_MORE)) if imageChecker() else None]},'Box Blur':{'Size':[50,100],'Sliders':1,'Function':lambda:[filterApply(Image.fromarray(original).filter(ImageFilter.BoxBlur(sliderFunctions['Box Blur'][0].get()))) if imageChecker() else None]},'Unsharp Mask':{'Size':[50,100],'Sliders':1,'Function':lambda:[filterApply(Image.fromarray(original).filter(ImageFilter.UnsharpMask(radius=sliderFunctions['Unsharp Mask'][0].get(),percent=150,threshold=3))) if imageChecker() else None]},
           'Saturation':{'Size':[50,100],'Sliders':1,'Function':lambda:[filterApply(ImageEnhance.Color(Image.fromarray(original)).enhance(sliderFunctions['Saturation'][0].get())) if imageChecker() else None]},'Gamma Correction':{'Size':[50,100],'Sliders':1,'Function':lambda:[filterApply(Image.fromarray(original).point(lambda p:((p/255.0)**(1/(sliderFunctions['Gamma Correction'][0].get()+1)))*255)) if imageChecker() else None]},'Color Boost':{'Size':[50,100],'Sliders':1,'Function':lambda:[filterApply(ImageEnhance.Color(Image.fromarray(original)).enhance(sliderFunctions['Color Boost'][0].get())) if imageChecker() else None]},'Shadow Enhance':{'Size':[50,100],'Sliders':1,'Function':lambda:[filterApply(ImageEnhance.Brightness(Image.fromarray(original)).enhance(sliderFunctions['Shadow Enhance'][0].get()*0.01+1)) if imageChecker() else None]},
           'Highlight Reduce':{'Size':[50,100],'Sliders':1,'Function':lambda:[filterApply(Image.fromarray(original).point(lambda p:max(p-sliderFunctions['Highlight Reduce'][0].get(),0))) if imageChecker() else None]},'Desaturate':{'Size':[50,50],'Sliders':0,'Function':lambda:[filterApply(ImageEnhance.Color(imaged).enhance(0)) if imageChecker() else None]},'Lighten':{'Size':[50,100],'Sliders':1,'Function':lambda:[filterApply(Image.fromarray(original).point(lambda p:min(p+sliderFunctions['Lighten'][0].get(),255))) if imageChecker() else None]},'Darken':{'Size':[50,100],'Sliders':1,'Function':lambda:[filterApply(Image.fromarray(original).point(lambda p:max(p-sliderFunctions['Darken'][0].get(),0))) if imageChecker() else None]},'Threshold':{'Size':[50,100],'Sliders':1,'Function':lambda:[filterApply(Image.fromarray(original).convert("L").point(lambda p:255 if p>sliderFunctions['Threshold'][0].get() else 0).convert("RGB")) if imageChecker() else None]},
           'Negative':{'Size':[50,50],'Sliders':0,'Function':lambda:[filterApply(ImageOps.invert(imaged.convert("RGB"))) if imageChecker() else None]},'Posterize Extreme':{'Size':[50,50],'Sliders':0,'Function':lambda:[filterApply(ImageOps.posterize(imaged.convert("RGB"),2)) if imageChecker() else None]},'Glow Effect':{'Size':[50,100],'Sliders':1,'Function':lambda:[filterApply(ImageEnhance.Brightness(Image.fromarray(original).filter(ImageFilter.GaussianBlur(sliderFunctions['Glow Effect'][0].get() * 2))).enhance(1.5)) if imageChecker() else None]},'Soft Blur':{'Size':[50,100],'Sliders':1,'Function':lambda:[filterApply(Image.fromarray(original).filter(ImageFilter.GaussianBlur(sliderFunctions['Soft Blur'][0].get()))) if imageChecker() else None]},'Dilation':{'Size':[50,100],'Sliders':1,'Function':lambda:[filterApply(Image.fromarray(cv2.dilate(original,np.ones((int(sliderFunctions['Dilation'][0].get()),int(sliderFunctions['Dilation'][0].get())),np.uint8),iterations=1))) if imageChecker() else None]},
           'Halftone Effect':{'Size':[50,50],'Sliders':0,'Function':lambda:[filterApply(imaged.convert("L").filter(ImageFilter.EMBOSS)) if imageChecker() else None]},'High Pass Filter':{'Size':[50,50],'Sliders':0,'Function':lambda:[filterApply(imaged.filter(ImageFilter.FIND_EDGES).convert("RGB")) if imageChecker() else None]},'Denoise':{'Size':[50,50],'Sliders':0,'Function':lambda:[filterApply(Image.fromarray(original).filter(ImageFilter.SMOOTH_MORE)) if imageChecker() else None]},'Dreamy Effect':{'Size':[50,100],'Sliders':1,'Function':lambda:[filterApply(Image.fromarray(original).filter(ImageFilter.SMOOTH).filter(ImageFilter.GaussianBlur(sliderFunctions['Dreamy Effect'][0].get()*2))) if imageChecker() else None]},'Hue Shift': {'Size': [50,50], 'Sliders': 0, 'Function': lambda: [filterApply(Image.fromarray(cv2.cvtColor(cvImage if cvImage.ndim == 3 else cv2.cvtColor(cvImage, cv2.COLOR_GRAY2RGB), cv2.COLOR_RGB2HSV))) if imageChecker() else None]},
           'InvertBGR':{'Size':[50,50],'Sliders':0,'Function':lambda:[filterApply(Image.fromarray(cv2.bitwise_not(cvImage))) if imageChecker() else None]},'Oil Paint':{'Size':[50,100],'Sliders':1,'Function':lambda:[filterApply(Image.fromarray(cv2.stylization(original, sigma_s=sliderFunctions['Oil Paint'][0].get()//4, sigma_r=0.6))) if imageChecker() else None]},'Pixelate':{'Size':[50,50],'Sliders':0,'Function':lambda:[filterApply(Image.fromarray(cv2.resize(cv2.resize(cvImage,(10,10),interpolation=cv2.INTER_LINEAR),(cvImage.shape[1],cvImage.shape[0]),interpolation=cv2.INTER_NEAREST))) if imageChecker() else None]},}

tkinter_colors = ["alice blue", "antique white", "aqua", "aquamarine", "azure","beige", "bisque", "black", "blanched almond", "blue", "blue violet","brown", "burlywood", "cadet blue", "chartreuse", "chocolate","coral", "cornflower blue", "cornsilk", "crimson", "cyan","dark blue", "dark cyan", "dark goldenrod", "dark gray", "dark green",
    "dark khaki", "dark magenta", "dark olive green", "dark orange", "dark orchid","dark red", "dark salmon", "dark sea green", "dark slate blue", "dark slate gray","dark turquoise", "dark violet", "deep pink", "deep sky blue", "dim gray","dodger blue", "firebrick", "floral white", "forest green", "fuchsia",
    "gainsboro", "ghost white", "gold", "goldenrod", "gray","green", "green yellow", "honeydew", "hot pink", "indian red","indigo", "ivory", "khaki", "lavender", "lavender blush","lawn green", "lemon chiffon", "light blue", "light coral", "light cyan",
    "light goldenrod yellow", "light gray", "light green", "light pink", "light salmon","light sea green", "light sky blue", "light slate gray", "light steel blue", "light yellow","lime", "lime green", "linen", "magenta", "maroon","medium aquamarine", "medium blue", "medium orchid", "medium purple", "medium sea green",
    "medium slate blue", "medium spring green", "medium turquoise", "medium violet red", "midnight blue","mint cream", "misty rose", "moccasin", "navajo white", "navy","old lace", "olive", "olive drab", "orange", "orange red","orchid", "pale goldenrod", "pale green", "pale turquoise", "pale violet red",
    "papaya whip", "peach puff", "peru", "pink", "plum","powder blue", "purple", "red", "rosy brown", "royal blue","saddle brown", "salmon", "sandy brown", "sea green", "seashell","sienna", "silver", "sky blue", "slate blue", "slate gray","snow", "spring green", "steel blue", "tan", "teal",
    "thistle", "tomato", "turquoise", "violet", "wheat","white", "white smoke", "yellow", "yellow green"]
       
def checkFunction(function):
    try:function;return 1
    except Exception as e:CTkMessagebox(main,title=e,message=f'Error occurred at {e}');return 0
    
def rotateImage():
    rotated = Image.fromarray(original).convert('RGBA').rotate(sliderFunctions['Rotate'][0].get(),expand=1)
    transparent = Image.new("RGBA", rotated.size, (0, 0, 0, 0))
    transparent.paste(rotated, (0, 0), rotated.convert('RGBA'))
    filterApply(transparent)
    
def filterApply(imageValue):currentWidget.configure(image=CTkImage(imageValue,size=(currentWidget.cget('width'),currentWidget.cget('height'))))

def imageChecker():
    global cvImage , imaged
    try:
        imaged = currentWidget.cget('image')._light_image
        cvImage = np.array(imaged)
        return 1     
    except:
        CTkMessagebox(main,title='No Image Selected',message='Kindly select the Image before any operations')
        return 0
            
def pencilFilter(filter,index):filterApply(Image.fromarray(cv2.pencilSketch(cv2.cvtColor(original, cv2.COLOR_RGBA2RGB),sigma_s=sliderFunctions[filter][0].get()//4,sigma_r=0.1,shade_factor=0.03)[index]))
    
# Text Updater
def textUpdate(key,backspace = 0):
    try:
        currentChar = key.char
        currentText = currentWidget.cget('text')
        if currentChar and currentText and currentWidget == main.focus_get().master:
            if currentWidget not in textVisited:textVisited.append(currentWidget);currentText = '';currentWidget.configure(text = currentText)
            if backspace:currentText = currentText[:-1]
            else:currentText += currentChar
            currentWidget.configure(text = currentText)
    except:pass
    
def sendMail(tableData):
    mailFrame.destroy()
    tableAllData = allColumns.split()
    sender = 'nikishdaniel1@gmail.com'
    try:
        mailSend = smtplib.SMTP('smtp.gmail.com',587)
        mailSend.starttls()
        mailSend.login(sender, 'jpns gozh cnce wbkq')
    except:
        CTkMessagebox(main,icon='warning',title_color='red',title='Connection Error',message='Sending Mail connection seemed to be lost.Kindly check your internet connection or it may be error from the server or the host')
        return
    bodyLabels = [x for x in re.findall(r'{{([a-zA-Z]+)}}',body)]
    print(tableData,tableAllData)
    for i in tableData:
        buffer = BytesIO()
        createdBody = body
        for x in range(len(i)):
            currentColumn = tableAllData[x]
            ValueCurrent = i[x].strip()
            if currentColumn in bodyLabels:
                createdBody = createdBody.replace('{{'+currentColumn+'}}',ValueCurrent)
            if currentColumn in labelsDictionary:
                labelsDictionary[currentColumn].configure(text = ValueCurrent)
                labelsDictionary[currentColumn].update_idletasks()
        measureBBox()
        certificate = ImageGrab.grab(bbox=greatest)
        formatValue = formatOption.get()
        certificate.save(buffer,format=formatValue)
        buffer.seek(0)
        message = MIMEMultipart()
        receiver = i[emailIndex]
        message['From'] = sender
        message['To'] = receiver
        message['Subject'] = subject
        message.attach(MIMEText(createdBody, "plain"))
        attachment = MIMEBase('application','octet-stream')
        attachment.set_payload(buffer.read())
        email.encoders.encode_base64(attachment)
        attachment.add_header('Content-Disposition','attachment',filename=f"certificate_{i}.{formatValue}")
        message.attach(attachment)
        try:mailSend.sendmail(sender,receiver,message.as_string())
        except:pass
        buffer.close()
    mailSend.close()

def fetchEmailDatas():
    global subject , body
    subject , body = subjectEntry.get() , bodyText.get('1.0','end')
    
def sendCertificateMail():
    global currentWord
    currentWord = ''
    def destroyer():
        try:txtLable.destroy()
        except:pass
    def trackRecommendation(event):
        global txtLable , currentWord , stream
        cursorIndex = bodyText.index(INSERT)
        val = event.keysym.lower()
        if val in ['period','comma','semicolon','Caps_Lock','Tab','shift_l','shift_r','control_l','control_r','space','left','right']:
            currentWord = ''
            destroyer()
            return
        elif val == 'return':
            try:
                if currentWord:
                    labeledValue = txtLable.cget('text')
                    bodyText.delete(f'{cursorIndex}-{len(currentWord)}c',cursorIndex)
                    bodyText.insert('end','{{'+labeledValue.strip()+'}}')
                    txtLable.destroy()
                    return 'break'
            except:None
        elif val == 'backspace':currentWord = currentWord[:-1]
        else:currentWord += val
        destroyer()
        if len(currentWord) == 1:stream = [x for x in tableAllData if x[0] == currentWord or x[0] == currentWord.upper()]
        x, y , _ , height = bodyText.bbox(cursorIndex)
        try:
            txtLable = CTkLabel(mailFrame, text=stream[0] if len(currentWord) == 1 else [x for x in stream if x.startswith(currentWord) or x.startswith(currentWord.capitalize())][0], width=1, bg_color="gray")
            txtLable.place(x=40, y=170)
        except:pass
    global subjectEntry , bodyText , formatOption , tableAllData , sendMailCondition , mailFrame
    tableAllData = allColumns.split()
    tableData = table.values[1:]
    mailFrame = CTkFrame(main,width=380,height=330,fg_color='black')
    CTkLabel(mailFrame,text='Body').place(x=10,y=55)
    CTkLabel(mailFrame,text='Subject').place(x=10,y=20)
    subjectEntry = CTkEntry(mailFrame,placeholder_text='Subject of the Mail',width=230)
    subjectEntry.place(x=70,y=20)
    CTkButton(mailFrame,width=100,text='Send',hover_color='grey32',fg_color='red',image=CTkImage(Image.open(rf"{targetPath}\Icons\icons8-send-64 (1).png")),command=lambda:[fetchEmailDatas(),sendMail(tableData)]).place(x=20,y=270)
    CTkLabel(mailFrame,text='Send As',font=('Times New Roman',15),text_color='blue').place(x=165,y=270)
    formatOption = CTkOptionMenu(mailFrame,values=['pdf', 'jpeg', 'xbm', 'webp', 'ppm', 'png', 'pcx', 'pcd', 'msp', 'im', 'ico', 'icns', 'grib', 'gbr', 'dib', 'dcx', 'dds', 'bufr', 'bmp'])
    formatOption.place(x=225,y=270)
    bodyText = CTkTextbox(mailFrame,width=330,height=160)
    bodyText.place(x=20,y=90)
    bodyText.bind('<Key>',trackRecommendation)
    CTkButton(mailFrame,width=10,fg_color='black',hover_color='black',text='',image=CTkImage(Image.open(fr'{targetPath}\Icons\close-red-icon.webp')),command=lambda:[mailFrame.destroy()]).place(x=340,y=0)
    mailFrame.place(x=100,y=100)
    
def plot():
    global totalPlot , labelsDictionary , unpackIndex , tableColumnValues , emailIndex , allColumns
    totalPlot = unpackIndex = 0
    labelsDictionary = {}
    tableColumnValues = table.values[0]
    allColumns = ' '.join(tableColumnValues)
    columns = allColumns.lower()
    warningPopUp = CTkLabel(tableFrame,text='Please add Email column',font=('Times New Roman',25),text_color='red')
    if 'email' not in columns:
        warningPopUp.place(x=100,y=100)
        warningPopUp.after(1000,warningPopUp.place_forget)
        return
    emailIndex = columns.split().index('email')
    for i in fethchedLabels.winfo_children():
        if i.get():
            upload(text = 1,textValue=i.cget('text'))
            totalPlot += 1
    tableFrame.destroy()
    sendButton.configure(state = 'normal')
    
def checkTable(widget,operation):
    try:exec(f'{widget}.{operation}()')
    except:pass
    
def packLabels(datas):
    try:
        for i in fethchedLabels.winfo_children():i.destroy()
        for i in datas:CTkCheckBox(fethchedLabels,text=i,fg_color='black',hover_color='white',onvalue=1,offvalue=0).pack(pady=10)
    except:pass
    
def tableCreateOrEdit(flag):
    global table , editTableButton
    functions = {'.csv':read_csv,'.xls':read_excel,'.xml':read_xml,'.xlsx':read_excel,'.json':read_json}
    addColumn = CTkButton(sideFrame,text='Add Column',fg_color='black',hover_color='grey32',command=lambda:table.add_column(values=''))
    addColumn.place(x=20,y=130)
    addRow = CTkButton(sideFrame,text='Add Row',fg_color='black',hover_color='grey32',command=lambda:table.add_row(values=''))
    addRow.place(x=20,y=170)
    tableSaveButton = CTkButton(sideFrame,text='',fg_color='grey12',hover_color='grey32',width=1,height=1,image=CTkImage(Image.open(rf"{targetPath}\Icons\png-clipart-black-n-white-white-refresh-icon-removebg-preview.png"),size=(16,13)))
    tableSaveButton.place(x=144,y=210)
    fethchedLabels.place(x=20,y=210)
    datas = [[''],['']]
    attributes = ['Email']
    if flag:
        try:
            file = filedialog.askopenfile('r',filetypes=[('CSV File','*.csv'),('Excel File','*.xls;*.xlsx'),('All Files','*.*')])
            value = file.name
            extension = value[value.rfind('.'):]
            data = functions.get(extension, lambda x: None)(file.name)
            attributes = list(data.columns)
            datas = data.values.tolist()
            tableSaveButton.configure(state = 'disabled')
            addColumn.configure(state = 'disabled')
            addRow.configure(state = 'disabled')
        except:
            CTkMessagebox(main,title='File Error',icon='warning',message=f'Unable to open the selected file. Please select a valid {file} file.')
            return
    datas.insert(0,attributes)
    table = CTkTable(scrollable,values=datas,write=False if flag else True)
    table.pack(expand=True, fill='both')
    if flag:
        editTableButton = CTkButton(sideFrame,image=CTkImage(dark_image=Image.open(rf'{targetPath}\Icons\icons8-edit-30.png')),text='Edit',fg_color='black',hover_color='grey32',command=lambda : [table.configure(write = True),addRow.configure(state = 'normal'),addColumn.configure(state = 'normal'),tableSaveButton.configure(state = 'normal')])
        editTableButton.place(x=20,y=90)
    else:checkTable('editTableButton','place_forget')
    canvaFrame.configure(yscrollcommand=v_scrollbar.set,xscrollcommand=h_scrollbar.set)
    scrollable.bind("<Configure>",lambda x:canvaFrame.configure(scrollregion=canvaFrame.bbox("all")))
    tableSaveButton.configure(command = lambda:packLabels(table.values[0]))
    packLabels(table.values[0])
    CTkButton(sideFrame,text='Plot',fg_color='black',hover_color='grey32',command=plot).place(x=20,y=430)
    
def sendMailCheck(frame):
    global sendButton
    sendButton = CTkButton(frame,text='Send Mail',fg_color='grey13',state='disabled',hover_color='grey',image=CTkImage(Image.open(fr'{targetPath}\Icons\icons8-send-64.png')),command= lambda : [sendCertificateMail()])
    sendButton.place(x=40,y=60)
    
def showTableFrame():
    global tableFrame , scrollable , sideFrame , canvaFrame , v_scrollbar , h_scrollbar , fethchedLabels , tableSaveButton
    tableFrame = CTkFrame(main,width=500,height=500,fg_color='black')
    canvaFrame = CTkCanvas(tableFrame,width=375,height=555,bg = 'black')
    scrollable = CTkFrame(canvaFrame,width=290,height=435,fg_color='black')
    sideFrame = CTkFrame(tableFrame,width=180,height=470,fg_color='grey12',bg_color='grey12')
    CTkButton(sideFrame,text='Upload Data',fg_color='black',hover_color='grey32',image=CTkImage(dark_image=Image.open(fr"{targetPath}\Icons\whiteUpload-removebg-preview.png"),size=(15,15)),command=lambda:[checkTable('table','pack_forget'),tableCreateOrEdit(1)]).place(x=20,y=10)
    CTkButton(sideFrame,text='Create Data',fg_color='black',hover_color='grey32',command=lambda:[checkTable('table','pack_forget'),tableCreateOrEdit(0)]).place(x=20,y=50)
    CTkButton(tableFrame,text='',fg_color='black',hover_color='white',image= CTkImage(Image.open(rf'{targetPath}\Icons\close-red-icon.webp')))
    canvaFrame.create_window((8,8), window=scrollable, anchor="nw")
    fethchedLabels = CTkScrollableFrame(sideFrame,width=100,height=100)
    v_scrollbar = CTkScrollbar(tableFrame,height=450,command=canvaFrame.yview)
    v_scrollbar.place(x=485, y=35)
    h_scrollbar = CTkScrollbar(tableFrame,width=320,orientation='horizontal', command=canvaFrame.xview)
    h_scrollbar.place(x=180, y=485)
    sideFrame.place(x=0,y=30)
    canvaFrame.place(x=225,y=45)
    tableFrame.place(x=20,y=60)

def measureBBox():
    global greatest , greatestArea
    for i in frame.winfo_children():
        if isinstance(i,CTkLabel):
            width , height = i.winfo_width() , i.winfo_height()
            area = width*height
            position1 , position2 = i.winfo_rootx() , i.winfo_rooty()
            if area >= greatestArea:greatestArea = area;greatest = [position1,position2,position1+width,position2+height]
    
def changeCursor(type):global mouse;mouse = type

def changeFont(stmt):
    try:exec(stmt)
    except:pass

def cartoonize(image):
    if image.shape[-1] == 4:image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY) if len(image.shape) != 2 else image
    gray = cv2.medianBlur(gray, 1)
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
    color = cv2.bilateralFilter(image, d=9, sigmaColor=300, sigmaSpace=300)
    return cv2.bitwise_and(color, color, mask=edges)
    
# Function for taking Online images 
def takeOnline():
    try:
        imageUrl = get(textBox.get())
        if imageUrl.raise_for_status():CTkMessagebox(main,title='Request Denied',icon='cancel',message='Image address URL doesn"t support copy/paste')
        buffer = BytesIO(imageUrl.content)
        upload(image=buffer,online=1)
        buffer.close()
    except:CTkMessagebox(main,title='URL Error',icon='warning',message='Invalid Image address.Kindly check the image address,if the it is correct and this error rise then the URL doesn"t supports copy')
  
# Function to save the Image  
def saveImage(saveimg):
    savePath = filedialog.asksaveasfile(defaultextension='.jpg',filetypes=fileFormat)
    if savePath:
        try:
            values = savePath.name
            saveimg.save(savePath.name,format=values[values.rfind('.')+1:].upper())
            CTkMessagebox(main,icon='check',message='Image saved successfully',title='Saved',title_color='white')
        except:CTkMessagebox(main,icon='warning',title='Download Failed',title_color='white',message='There was an error in Downloading try to upload image or choose another image')
    else:CTkMessagebox(main, icon='warning', title='Save Canceled',title_color='white', message='Save operation canceled by the user')
    
# Function for taking the current focused widget
def takeStart(sub,event,focuser,previous = None):
    global currentWidget , start1 , end1 , original
    currentWidget = sub
    if focuser:
        result = imageChecker()
        updateAttributes()
        focusedImage = np.array(currentWidget.cget('image')._light_image)
        if result and currentWidget != previous:original = focusedImage
    xValue.set(currentWidget.winfo_x())
    yValue.set(currentWidget.winfo_y())
    start1 , end1 = event.x , event.y
    previous = currentWidget
    
# Function for the widget movement
def movement(event,text):
    new_x = currentWidget.winfo_x() + (event.x - start1)
    new_y = currentWidget.winfo_y() + (event.y - end1)
    if mouse == 'plus' and new_x>0 and new_y > 0:
        currentWidget.configure(width = new_x,height = new_y)
        if not text:currentWidget.configure(image = CTkImage(imaged.resize((new_x,new_y),Image.Resampling.LANCZOS),size=(new_x,new_y)))
        else:currentWidget.configure(font = (fonts.get(),new_y))
    elif mouse == 'fleur':currentWidget.place(x=new_x, y=new_y)
    
def extractFrame(frame):
    global textExtractValue
    textExtractValue = StringVar(main,value='')
    def TranslateTo(x):
        try:
            textExtractValue.set(Translator(to_lang=x).translate(textExtractValue.get()))
        except:
            translateError = CTkLabel(frame,text='Unable to translate',width=20,height=10)
            translateError.place(x=10,y=60)
            translateError.after(1000,translateError.destroy)
    CTkLabel(frame,text='Extracted',width=0,text_color='yellow').place(x=5,y=60)
    CTkEntry(frame,textvariable=textExtractValue).place(x=60,y=60)
    CTkLabel(frame,text='Translate',width=0,text_color='yellow').place(x=5,y=100)
    CTkComboBox(frame,values=['english','german','spanish','chinese','french'],command=lambda x:TranslateTo(x)).place(x=60,y=100)
    
# For creating the base Widget 
def upload(text = 0,image = None,online = 0,textValue = ''):
    def assignTextValue(textValue):labelsDictionary[textValue] = sub;return textValue
    if text:
        sub = CTkLabel(frame,height=10,text_color='black',fg_color='#000001',bg_color='#000001',font=(fonts.get(),10,'normal'),anchor='w')
        sub.configure(text=assignTextValue(textValue) if textValue else 'Text')
        sub.bind('<Enter>',lambda x:sub.configure(fg_color = 'white'))
        sub.bind('<Leave>',lambda x:sub.configure(fg_color = '#000001'))
    else:
        sub = CTkLabel(frame,text='',width=100,height=100,bg_color='#000001',fg_color='#000001')
        try:sub.configure(image=CTkImage(light_image=Image.open(image if online else filedialog.askopenfilename(filetypes=fileFormat)),size=(100,100)))
        except:CTkMessagebox(main,title='Image Error',icon='warning',message='Invalid Image.Kindly check the image address or the image file')
    sub.place(x=20,y=20)
    sub.bind('<Button-1>',lambda x:takeStart(sub,x,0 if text else 1))
    set_opacity(sub,color='#000001')
    sub.bind('<B1-Motion>',lambda x:movement(x,text))
    
def Focus():
    global previous , current
    currentWidget = main.focus_get()
    filterName = ''
    while currentWidget and not isinstance(currentWidget, CTkFrame):
        currentWidget = main.nametowidget(currentWidget.winfo_parent())
        if isinstance(currentWidget, CTkButton):filterName = currentWidget.cget('text')
    if previous == None:previous = currentWidget
    current = currentWidget
    previous.configure(height = filters[previous.winfo_children()[0].cget('text')]['Size'][0],fg_color = 'transparent')
    previous.pack_propagate(False)
    currentWidgetSize = filters[filterName]['Size'][1]
    current.configure(height = currentWidgetSize,fg_color = 'grey32' if currentWidgetSize > 50 else 'transparent')
    current.pack_propagate(False)
    previous = current
    
def addFilters(i):
    frame = CTkFrame(filterFrame,width=220,height=50)
    button = CTkButton(frame,text=i,hover_color='red',command= lambda : filters[i]['Function'] if checkFunction(filters[i]['Function']()) else None)
    button.bind('<Button-1>',lambda x:[x.widget.focus_set(),Focus()])
    button.place(x=40,y=10)
    for x in range(filters[i]['Sliders']):
        slider = CTkSlider(frame,width=200,button_hover_color='red',fg_color='white',progress_color='red',from_=0,to=200,command=lambda val:filters[i]['Function']())
        slider.place(x=5,y=60+30*x)
        slider.set(0)
        sliderFunctions[i].append(slider)
    if 'Operation' in filters[i]:
        function = globals().get(filters[i]['Operation'])
        if callable(function):function(frame)
    frame.pack(pady = 10)
    frame.bind('<Enter>',lambda x:frame.configure(fg_color = 'grey32'))
    frame.bind('<Leave>',lambda x:frame.configure(fg_color = 'transparent' if current != frame else 'grey32'))
    
def updateAttributes():
    for i in attributes:
        try:attributes[i].set(eval(f'imaged.{i}'))
        except:pass
        
def attributeFrameImage(current):
    global index
    value = StringVar(main,value='')
    CTkLabel(attributeFrame,text=current,width=0).grid(row= index,column=0,pady=10,sticky = W)
    CTkEntry(attributeFrame,state='disabled',textvariable=value,width=150).grid(row= index,column=1,pady=10,padx = 10)
    attributes[current] = value
    index += 1
    
def topLevel(imageButton,i,popUp):
    movementButton = CTkButton(main,text='',width=0,fg_color='black',bg_color='black',image=CTkImage(Image.open(fr"{targetPath}\Icons\{imageButton}")),command=buttonImages[imageButton]['Function'])
    movementButton.place(x=i+5,y=105)
    movementButton.bind('<Enter>',lambda x:[showcase.configure(text = popUp),showcase.place(x=i+5,y=80)])
    movementButton.bind('<Leave>',lambda x:showcase.place_forget())

def pathCheck():
    global targetPath
    targetPath = os.path.join(os.path.expanduser('~'), 'ImageFilter')
    if not os.path.exists(targetPath):os.makedirs(targetPath)
    if hasattr(sys, '_MEIPASS'):
        basePath = sys._MEIPASS
    else:
        basePath = os.path.abspath(".")
    resource = os.path.join(basePath, 'ImageFilter')
    if not os.path.exists(resource):return
    for i in os.listdir(resource):
        source = os.path.join(resource, i)
        destination = os.path.join(targetPath, i)
        if os.path.isfile(source):shutil.copy(source, destination)
        elif os.path.isdir(source):
            if os.path.exists(destination):shutil.rmtree(destination)
            shutil.copytree(source, destination)
    
buttonImages = {'royalty-free-arrow-png-favpng-uFCai7qWyV6kb9Xj6qCQL9kvH-removebg-preview.png':{'PopUp':' Move ','x':330,'Function':lambda:changeCursor("fleur")},'back-sorting.png':{'PopUp':'  Lift  ','x':210,'Function':lambda:currentWidget.lift()},'icons8-resize-64.png':{'PopUp':'Resize','x':250,'Function':lambda:changeCursor("plus")},'images__7_-removebg-preview.png':{'PopUp':'Delete','x':290,'Function':lambda:changeFont("currentWidget.destroy()")}}
attributes = {'filename':'','format':'','mode':'','size':'','width':'','height':''}
main = CTk()
pathCheck()
index = 4
CTkLabel(main,text='PIXELCRAFT',width=700,fg_color='black',bg_color='black',font=('Algerian',40),text_color='Red').place(x=0,y=0)
userName = getlogin()
currentSize = StringVar(main,value=10)
text = StringVar(main)
set_appearance_mode('dark')
topFrame = CTkFrame(main,width=375,height=420,fg_color='black')
topFrame.place(x=7,y=90)
frame = CTkLabel(main,text='',fg_color='grey',bg_color='black',corner_radius=3,width = 350,height = 350)
frame.place(x=20,y=145)
textBox = CTkEntry(main,width=100,placeholder_text='Image Address')
textBox.place(x=38,y=105)
CTkLabel(topFrame,text='',width=0,image=CTkImage(dark_image=Image.open(rf"{targetPath}\Icons\erasebg-transformed.webp"),size=(30,30))).place(x=0,y=12)
CTkButton(main,text='apply',width=30,command=takeOnline).place(x=142,y=105)
tab = CTkTabview(main,width=300,height=649,fg_color='#121212',segmented_button_selected_color='black',segmented_button_selected_hover_color='grey23')
tab.place(x=400,y=50)
tab.add('Filters')
filterFrame = CTkScrollableFrame(tab.tab('Filters'),width=220,height=500)
filterFrame.pack(pady=10, padx=10, fill="both", expand=True)
tab.add('Attributes')
attributeFrame = CTkScrollableFrame(tab.tab('Attributes'), width=220, height=500)
attributeFrame.pack(pady=10, padx=10, fill="both", expand=True)
CTkLabel(attributeFrame,text='Positions',text_color='red',font=('Algerian',20),anchor="center").grid(row= 0,column=1,pady=10,sticky = EW)
CTkLabel(attributeFrame,text='X').grid(row= 1,column=0,pady=10,sticky = W)
xValue , yValue = StringVar(main,value='') , StringVar(main,value='')
CTkEntry(attributeFrame,width=150,textvariable=xValue,state='disabled').grid(row = 1,column = 1,pady=10,sticky = EW,padx = 10)
CTkLabel(attributeFrame,text='Y').grid(row= 2,column=0,pady=10,sticky = W)
CTkEntry(attributeFrame,width=150,textvariable=yValue,state='disabled').grid(row = 2,column = 1,pady=10,sticky = EW,padx = 10)
CTkLabel(attributeFrame,text='Image',text_color='red',width=0,font=('Algerian',20),anchor="center").grid(row = 3,column = 1,pady=10,sticky = EW)
for x in attributes:
    attributeFrameImage(x)
CTkLabel(attributeFrame,text='Text',text_color='red',width=0,font=('Algerian',20),anchor="center").grid(row = index + 1,column = 1,pady=10,sticky = EW)
CTkLabel(attributeFrame,text='Fonts',width=0).grid(row= index + 2,column=0,pady=10,sticky = W)
fonts = CTkOptionMenu(attributeFrame,values=font.families(),width=150,dynamic_resizing=False,command=lambda x:changeFont(f'currentWidget.configure(font = ("{x}",{int(currentSize.get())}))'))
fonts.grid(row=index + 2,column=1,pady=10,sticky = W,padx = 10)
showcase = CTkLabel(main,width=10,height=10,fg_color='black',text='')
CTkLabel(attributeFrame,text='Colors',width=0).grid(row= index + 3,column=0,pady=10,sticky = W)
CTkOptionMenu(attributeFrame,values=tkinter_colors,width=150,dynamic_resizing=False,command=lambda x:currentWidget.configure(text_color = x) if currentWidget else None).grid(row=index + 3,column=1,pady=10,sticky = W,padx = 10)
CTkLabel(attributeFrame,text='Size',width=0).grid(row= index + 4,column=0,pady=10,sticky = W)
size = CTkEntry(attributeFrame,width=150,textvariable=currentSize)
size.grid(row=index + 4,column=1,pady=10,sticky = W,padx = 10)
size.bind('<Return>',command = lambda x: [currentSize.set(size.get()),changeFont(f'currentWidget.configure(font = ("{fonts.get()}",{int(currentSize.get())}))'),changeFont(f'currentWidget.configure(height = {int(currentSize.get())})')])
CTkButton(main,text='Upload',fg_color='black',hover_color='grey32',image=CTkImage(dark_image=Image.open(rf"{targetPath}\Icons\whiteUpload-removebg-preview.png"),size=(15,15)),command=upload).place(x=20,y=570)
CTkButton(main,text='Text',fg_color='black',hover_color='grey32',image=CTkImage(dark_image=Image.open(rf"{targetPath}\Icons\text.png")),command=lambda : upload(text = 1)).place(x=230,y=570)
CTkButton(main,text='Save',fg_color='black',hover_color='grey32',image=CTkImage(dark_image=Image.open(rf"{targetPath}\Icons\save-256.png"),size=(15,15)),command=lambda : [measureBBox(),saveImage(ImageGrab.grab(bbox=greatest))]).place(x=20,y=610)
CTkButton(main,text='Rectangle',fg_color='black',hover_color='grey32',command=lambda:upload(online=1,image=rf'{targetPath}\Icons\5895916-removebg-preview.png')).place(x=230,y=610)
for i in buttonImages:topLevel(i,buttonImages[i]['x'],buttonImages[i]['PopUp'])
for i in filters:
    addFilters(i)
frame.bind('<Enter>',lambda x:main.configure(cursor = mouse))
frame.bind('<Leave>',lambda x:main.configure(cursor = ''))
main.bind('<Button-1>',lambda x:x.widget.focus_set() if hasattr(x.widget, "focus_set") else None)
main.bind('<Key>',lambda x:textUpdate(x))
main.bind('<BackSpace>',lambda x:textUpdate(x,1))
main.title('PIXELCRAFT')
main.geometry('700x700')
main.resizable(0,0)
main.mainloop()