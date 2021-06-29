from tkinter import *
from tkinter import ttk,messagebox
#tkk is theme of Tk
import csv
from datetime import datetime

GUI = Tk()
GUI.title('โปรแกรมบันทึกค่าใช้จ่าย v 1.0 By Sim')
#GUI.geometry('720x700+500+50')

w = 720
h = 500

ws = GUI.winfo_screenwidth() #screen width | check ว่าหน้าจอคอมพิวเตอร์ของเรานั้นกว้างเท่าไหร่
hs = GUI.winfo_screenheight() #screen height


x = (ws/2) - (w/2)
y = (hs/2) - (h/2) - 50

GUI.geometry(f'{w}x{h}+{x:.0f}+{y:.0f}')


#B1 = Button(GUI,text='Hello')
#B1.pack(ipadx=50,ipady=10) #.pack() ติดปุ่มเข้ากับ GUI หลัก


############MENU###########
menubar = Menu(GUI)
GUI.config(menu=menubar)

#file menu
filemenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='File',menu=filemenu)
filemenu.add_command(label='Import CSV')
filemenu.add_command(label='Export to Googlesheet')

#Help
def About():
    print('About Menu')
    messagebox.showinfo('About','โปรแกรมนี้คือโปรแกรมบันทึกข้อมูล\nสนใจบริจาคไหม? จ่ายแค่ 1 BTC')

helpmenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='Help',menu=helpmenu)
helpmenu.add_command(label='About',command=About)
#Donate

donatemenu = Menu(menubar)
menubar.add_cascade(label='Donate',menu=donatemenu)

###########################

"""T1 = Frame(Tab,width=400,height=400) ใส่ width ได้
T2 = Frame(Tab,width=400)
Tab.pack()"""

Tab = ttk.Notebook(GUI)
T1 = Frame(Tab)
T2 = Frame(Tab)
Tab.pack(fill=BOTH, expand=1)

icon_t1 = PhotoImage(file='t1_expense.png')
icon_t2 = PhotoImage(file='t2_expenselist.png')

Tab.add(T1,text=f'{"เพิ่มค่าใช้จ่าย":^{30}}',image=icon_t1,compound='top')
Tab.add(T2,text=f'{"ค่าใช้จ่ายทั้งหมด":^{30}}',image=icon_t2,compound='top')


F1 = Frame(T1)
#F1.place(x=100,y=50)
F1.pack()

days = {'Mon':'จันทร์',
        'Tue':'อังคาร',
        'Wed':'พุธ',
        'Thu':'พฤหัสบดี',
        'Fri':'ศุกร์',
        'Sat':'เสาร์',
        'Sun':'อาทิตย์'}

def Save(event=None):
    expense = v_expense.get()
    price = v_price.get()
    quantity = v_quantity.get()

    if expense == '':
        print('No Data')
        messagebox.showwarning('Error','กรุณากรอกข้อมูลค่าใช้จ่าย')
        return
    elif price == '':
        messagebox.showwarning('Error','กรุณากรอกราคา')
        return
    elif quantity == '':
        quantity = 1

    total = float(price) * float(quantity)

    try:
        total = float(price) * float(quantity)
        #.get() คือดึงค่ามาจาก v_expense = StringVar()
        print('รายการ: {} ราคา: {}'.format(expense,price))
        print('จำนวน: {} รวมทั้งหมด {} บาท'.format(quantity,total))
        text = 'รายการ: {} ราคา: {}\n'.format(expense,price)
        text = text + 'จำนวน: {} รวมทั้งหมด: {} บาท'.format(quantity,total)
        v_result.set(text)
        v_expense.set('')
        v_price.set('')
        v_quantity.set('')

        #บันทึกข้อมูลลง csv
        today = datetime.now().strftime('%a')
        print(today)
        stamp = datetime.now()
        dt = stamp.strftime('%Y-%m-%d %H:%M:%S')
        transactionid = stamp.strftime('%Y%m%d%H%M%f')
        dt = days[today] + '-' + dt

        with open('savedata.csv','a',encoding='utf-8',newline='') as f: # 'a' เป็นตัว stamp เวลาเข้าไปเรื่อยๆ
            #with คือสั่งเปิดไฟล์แล้วปิดอัตโนมัติ
            # 'a' การบันทึกเรื่อยๆ เพิ่มข้อมูลต่อจากข้อมูลเก่า
            #newline='' ทำให้ข้อมูลไม่มีบรรทัดดว่าง
            fw = csv.writer(f) #สร้างฟังก์ชันสำหรับเขียนข้อมูล
            data = [transactionid,dt,expense,price,quantity,total]
            fw.writerow(data)

        #ทำให้เคอเซอร์กลับไปตำแหน่งช่องกรอก E1

        E1.focus()
        update_table()
    except Exception as e:
        print('ERROR:',e)
        messagebox.showwarning('Error','กรุณากรอกข้อมูลใหม่ ให้กรอกในช่องราคาเฉพาะตัวเลข')
        v_expense.set('')
        v_price.set('')
        v_quantity.set('')


#ทำให้สามารถกด enter ได้
GUI.bind('<Return>',Save) #ต้องเพิ่มใน def Save(event=None) ด้วย

FONT1 = (None,10) #None คือไม่ได้เปลี่ยน font แต่ถ้าอยากเปลี่ยนให้กำหนดเป็น 'Angsana New'

#------------------Image---------
main_icon = PhotoImage(file='icon_money.png')

Mainicon = Label(F1,image=main_icon)
Mainicon.pack()

#------text1----------
L = ttk.Label(F1,text='รายการค่าใช้จ่าย',font=FONT1).pack()
v_expense = StringVar() # StringVar() คือตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
E1 = ttk.Entry(F1,textvariable=v_expense,font=FONT1)
E1.pack()
#----------------

#------text2----------
L = ttk.Label(F1,text='ราคา (บาท)',font=FONT1).pack()
v_price = StringVar() # StringVar() คือตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
E2 = ttk.Entry(F1,textvariable=v_price,font=FONT1)
E2.pack()
#----------------

#--------------text3--------------
L = ttk.Label(F1,text='จำนวน (ชิ้น)',font=FONT1).pack()
v_quantity = StringVar()
E3 = ttk.Entry(F1,textvariable=v_quantity,font=FONT1)
E3.pack()
#------------------

icon_t3 = PhotoImage(file='t3_save.png')

B2 = ttk.Button(F1,text=f'{"Save": >{6}}',image=icon_t3,compound='left',command=Save)
B2.pack(ipadx=50,ipady=20,pady=20)

v_result = StringVar()
v_result.set('----------ผลลัพธ์--------------')
result = ttk.Label(F1,textvariable=v_result,font=FONT1,foreground='#de237e')
result.pack(pady=20)


##################################Tab2##################

def read_csv():
    with open('savedata.csv',newline='',encoding='utf-8') as f: # มีไว้ป้องกันการลืมปดิไฟล์ csv
        fr = csv.reader(f)
        data = list(fr)
    return data

#table

L = ttk.Label(T2,text='ตารางแสดงผลลัพธ์ทั้งหมด',font=FONT1).pack(pady=20)
header = ['รหัสรายการ','วัน-เวลา','รายการ','ค่าใช้จ่าย','จำนวน','รวม']
resulttable = ttk.Treeview(T2,columns=header,show='headings',height=30)
resulttable.pack()

#for i in range(len(header)):
 #   resulttable.heading(header[i],text=header[i])


for h in header:
    resulttable.heading(h,text=h)

headerwidth = [100,150,170,80,80,80]
for h,w in zip(header,headerwidth):
    resulttable.column(h,width=w)


#resulttable.insert('','end',value=['จันทร์','น้ำดื่ม',30,5,150])
#resulttable.insert('','end',value=['อังคาร','น้ำดื่ม',30,5,150])
alltransaction = {}


def UpdateCSV():
    with open('savedata.csv','w',newline='',encoding='utf-8') as f: # 'w' มีไว้ replace หรือการเขียนทับไปเลย
        fw = csv.writer(f)
        # เตรียมข้อมูลจาก alltransaction ให้กลายเป็น list
        data = list(alltransaction.values())
        fw.writerows(data) # เป็นการเขียนแบบ multiple line from nested list [[],[],[]]
        print('Tables was updated')
    update_table()

def DeleteRecord(event=None):
    check = messagebox.askyesno('Confirm?','คุณต้องการลบข้อมูลหรือไม่?')
    print('Yes/No',check)

    if check == True:
        print('delete')
        select = resulttable.selection()
       # print(select)
        data = resulttable.item(select)
        data = data['values']
        transactionid = data[0]
        #print(transactionid)
        del alltransaction[str(transactionid)] # delete data in dict
        #print(alltransaction)
        UpdateCSV()
        #update_table()
    else:
        print('cancel')


Bdelete = ttk.Button(T2,text='delete',command=DeleteRecord)
Bdelete.place(x=50,y=550)

resulttable.bind('<Delete>',DeleteRecord)


def update_table():
    resulttable.delete(*resulttable.get_children())
    try:
        data = read_csv()
        for d in data:
            #creat transaction data
            alltransaction[d[0]] = d # d[0] = transactionid
            resulttable.insert('',0,value=d)
        print(alltransaction)
    except Exception as e:
        print('No file')
        print('Error',e)

###########Right click Menu##############
def EditRecord():
    POPUP = Toplevel() #คล้ายๆ Tk()
    POPUP.title('Edit Record')
    #POPUP.geometry('500x400')

    w = 500
    h = 400

    ws = POPUP.winfo_screenwidth() #screen width | check ว่าหน้าจอคอมพิวเตอร์ของเรานั้นกว้างเท่าไหร่
    hs = POPUP.winfo_screenheight() #screen height


    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2) - 50

    POPUP.geometry(f'{w}x{h}+{x:.0f}+{y:.0f}')

    #------text1----------
    L = ttk.Label(POPUP,text='รายการค่าใช้จ่าย',font=FONT1).pack()
    v_expense = StringVar() # StringVar() คือตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
    E1 = ttk.Entry(POPUP,textvariable=v_expense,font=FONT1)
    E1.pack()
    #----------------

    #------text2----------
    L = ttk.Label(POPUP,text='ราคา (บาท)',font=FONT1).pack()
    v_price = StringVar() # StringVar() คือตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
    E2 = ttk.Entry(POPUP,textvariable=v_price,font=FONT1)
    E2.pack()
    #----------------

    #--------------text3--------------
    L = ttk.Label(POPUP,text='จำนวน (ชิ้น)',font=FONT1).pack()
    v_quantity = StringVar()
    E3 = ttk.Entry(POPUP,textvariable=v_quantity,font=FONT1)
    E3.pack()
    #------------------

    def Edit():
       # print(transactionid)
        #print(alltransaction)
        olddata = alltransaction[str(transactionid)]
        print('OLD:',olddata)
        v1 = v_expense.get()
        v2 = float(v_price.get())
        v3 = float(v_quantity.get())
        total = v2 * v3

        newdata = [olddata[0],olddata[1],v1,v2,v3,total]
        alltransaction[str(transactionid)] = newdata
        UpdateCSV()
        update_table()
        POPUP.destroy() #สั่งปิด popup 

    icon_t3 = PhotoImage(file='t3_save.png')

    B2 = ttk.Button(POPUP,text=f'{"Save": >{6}}',image=icon_t3,compound='left',command=Edit)
    B2.pack(ipadx=50,ipady=20,pady=20)

    # get data in selected record
    select = resulttable.selection()
    print(select)
    data = resulttable.item(select)
    data = data['values']
    print(data)
    transactionid = data[0]

    #สั่งเซตค่าเก่าไว้ตรงช่องกรอก
    v_expense.set(data[2])
    v_price.set(data[3])
    v_quantity.set(data[4])
    POPUP.mainloop()

rightclick = Menu(GUI,tearoff=0)
rightclick.add_command(label='Edit',command=EditRecord)
rightclick.add_command(label='Delete',command=DeleteRecord)


def menupopup(event):
    #print(event.x_root,event.y_root)
    rightclick.post(event.x_root,event.y_root)

resulttable.bind('<Button-3>',menupopup)



update_table()
print('GET CHILD:',resulttable.get_children())
GUI.bind('<Tab>',lambda x: E2.focus())
GUI.mainloop()
