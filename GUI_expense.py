# GUI Basic.py  Vorsion 2.0 beta 
# เปลี่ยนมาใช้ database แทน csv
import builtins
from tkinter import *
from tkinter import ttk, messagebox
from tkinter.font import Font #theme
from datetime import datetime
import csv

#######################################################
import sqlite3

# สร้าง data base
conn = sqlite3.connect('expense.db')
# สร้างตัวดำเนินการ อยากได้อะไรใช้ตัวนี้ได้เลย
c = conn.cursor()

#สร้าง table ด้วยภาษา SQL
'''
['รหัสรายการ'(transactionid) text,
'วัน-เวลา'(datetime) text,
'ราการ'(title) text,
'ค่าใช้จ่าย'(expense) real(float),
'จำนวน'(count) integer,
'รวม'(total)] real
'''
c.execute("""CREATE TABLE IF NOT EXISTS expenselist (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                transactionid TEXT,
                datetime TEXT,
                title TEXT,
                expense REAL,
                count INTEGER,
                total REAL        
            )""")

def insert_expense(transactionid,datetime,title,expense,count,total):
    ID = None
    with conn:
        c.execute("""INSERT INTO expenselist VALUES (?,?,?,?,?,?,?)""",
            (ID,transactionid,datetime,title,expense,count,total))
    conn.commit() # บันทึกข้อมูลลงฐานข้อมูล
    #print ('Inset Success!')

def show_expense():
    with conn:
        c.execute("SELECT * FROM expenselist")
        expense = c.fetchall() # คำสั่งดึงข้อมูล
       # print(expense)

    return expense

def Update(transactionid,title,expense,count,total):
    with conn:
        c.execute("""UPDATE expenselist SET 
                    title=?,
                    expense=?,
                    count=?,
                    total=?
                    WHERE transactionid=?""",
                    ([title,expense,count,total,transactionid,]))
    conn.commit()
    # print ('Data updated')

def Delete(transactionid):
    with conn:
        c.execute("""DELETE FROM expenselist WHERE transactionid=?""",([transactionid]))
    conn.commit()
    # print ('Deleted')

#######################################################

root = Tk () 
root.title('โปรแกรมบันทึกค่าใช้จ่าย By ปาร์ค')
root.geometry ('600x600') 

Font1 = (None,20) #None เปลี่ยนเป็น 'Angsana New' ได้
Font2 = ('Sans Serif',12) #None เปลี่ยนเป็น 'Angsana New' ได้
#ใส่รูป ต้องเป็น PNG เท่านั้น .subsample = ย่อขนาดรูป
bg = PhotoImage(file='bag.png').subsample(4)
ic1 = PhotoImage(file='money.png').subsample(22)
ic2 = PhotoImage(file='ic2.png').subsample(22)
ic3 = PhotoImage(file='ic3.png').subsample(22)

############MANU##############
menubar = Menu(root)
root.config(menu = menubar)

# File menu
filemenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='File' , menu = filemenu)
filemenu.add_command(label = 'Import CSV')
filemenu.add_command(label = 'Export to Googlesheet')
# Help menu
helpmenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='Help' , menu = helpmenu)
def About():
    messagebox.showwarning('About','Nodata')
helpmenu.add_command(label = 'About',command=About)
##############################

#สร้าง tab
tabControl = ttk.Notebook(root)
tab1 = ttk.Frame(tabControl)
tabControl.add(tab1,image=ic3 ,text = 'Add Expense',compound=TOP)

tab2 = ttk.Frame(tabControl)
tabControl.add(tab2,image=ic2, text = 'Expense list',compound=TOP)

tabControl.pack(expand = 1, fill = 'both')


days = {'Mon':'จันทร์',
        'Tue':'อังคาร',
        'Wed':'พุธ',
        'Thu':'พฤหัสบดี',
        'Fri':'ศุกร์',
        'Sat':'เสาร์',
        'Sun':'อาทิตย์'}

F1 = Frame(tab1)
F1.pack()

bagpic = ttk.Label (F1, image=bg)
bagpic.pack (pady=10)

'''
B1 = ttk.Button(root, text = 'Hello')
B1.pack(ipadx=30,ipady=20)
'''
def Save (event = None):
    expense = v_expense.get() #.get = ดึงข้อมูลจาก v_expense
    price = float(v_price.get())
    count = int(v_count.get())
    if expense == '':
        messagebox.showwarning('Error','กรุณากรอกชื่อสินค้า')
    elif price == '':
        messagebox.showwarning('Error','กรุณากรอกราคาสินค้า')
    elif count == '':
        count = 1
    today = datetime.now().strftime('%a')
    stamp = datetime.now() #สร้าง id ให้ข้อมูลโดยใช้ timestamp
    tran_id = stamp.strftime('%Y%m%d%H%M%f') #%f หน่วยเป็น microsecond
    dt = datetime.now().strftime('%d-%m-%Y %H:%M')
    dt = days[today] + 'ที่ ' + dt
    total = price*count

    insert_expense(tran_id,dt,expense,price,count,total)

    try:
        # print('วัน {} ซื้อ{} ราคา {:,.2f} บาท จำนวน {} รวมทั้งหมด {:,.2f} บาท'.format(dt,expense,price,count,total))
        text = 'วัน{}\nซื้อ{} \nราคา {:,.2f} บาท จำนวน {} \nรวมทั้งหมด {:,.2f} บาท'.format(dt,expense,total,count,total)
        v_result.set(text)
        #เคลียร์ข้อมูลเก่า
        v_expense.set('')
        v_price.set('')
        v_count.set('')
        #บันทึกข้อมูลลง csv อย่าลืม import csv ด้วย
        with open ('savedata.csv', 'a' ,encoding='utf-8',newline='') as f: 
            # with คือสั่งเปิดไฟล์แล้วปิดอัตโนมัติ
            # 'a' คือการบันทึกต่อเรื่อย ๆ ถ้าใช้ 'w' จะเป็นการลบเขียนใหม่
            # newline = '' ทำให้ข้อมูลไม่มีบรรทัดว่าง
            fw = csv.writer(f) #สร้างฟังก์ชั่นสำหรับเขียนข้อมูล
            data = [tran_id,dt,expense,price,count,total]
            fw.writerow(data)
        # ทำให้เคเซอร์กลับไปช่อง E1
        E1.focus()
        upadate_table()
    except Exception as e:
        print('ERROR:',e)
        #messagebox.showerror('Error','ข้อความผิด กรุณากรอกข้อมูลใหม่')
        messagebox.showwarning('Error','ข้อความผิด กรุณากรอกข้อมูลใหม่')
        #messagebox.showinfo('Error','ข้อความผิด กรุณากรอกข้อมูลใหม่')
        v_expense.set('')
        v_price.set('')
        v_count.set('')
        E1.focus()
        

# ทำให้สามารถกด enter ได้
root.bind('<Return>',Save) #.bind = เช็คว่ามีการกดปุ่มอะไรบ้าง , <Return> = ปุ่ม enter

#-------text1--------
L1 = ttk.Label(F1,text='รายการค่าใช้จ่าย',font=Font1).pack()
v_expense = StringVar() #ตัวแปลพิเศษสำหรับเก็บข้อมูลใน GUI
E1 = ttk.Entry(F1,textvariable=v_expense,font=Font2)
E1.pack()
#-------------------------

#-------text2--------
L2 = ttk.Label(F1,text='ราคา (บาท)',font=Font1).pack()
v_price = StringVar()
E2 = ttk.Entry(F1,textvariable=v_price,font=Font2)
E2.pack()
#-------------------------

#-------text3--------
L3 = ttk.Label(F1,text='จำนวน (ชิ้น)',font=Font1).pack()
v_count = StringVar()
E3 = ttk.Entry(F1,textvariable=v_count,font=Font2)
E3.pack()
#-------------------------

B1 = ttk.Button(F1, image=ic1, text = 'Save' , command=Save,compound=LEFT)
B1.pack(pady=15)

v_result = StringVar()
v_result.set('------ผลลัพธ์------')
result = ttk.Label(F1, textvariable=v_result,font=Font2,foreground='green')
result.pack(pady=10)

#-----------------------Tab 2-------------------------
def read_csv ():
    with open ('savedata.csv',newline='',encoding='utf-8') as f:
        fr = csv.reader(f)
        data = list(fr)
    return data

# table

L = ttk.Label(tab2,text='ตารางค่าใช้จ่ายทั้งหมด',font=Font1).pack()

# สร้างตาราง
header = ['รหัสรายการ','วัน-เวลา','ราการ','ค่าใช้จ่าย','จำนวน','รวม']
resulttable = ttk.Treeview(tab2,columns=header,show='headings',height=20)
resulttable.pack(pady=10)

# ใส่ข้อความลง header ในตาราง
for h in header:
    resulttable.heading(h,text=h)

# กำหนดความกว้างของตาราง zip ใช้ในการรวมลิสเข้าด้วยกัน
headerwidth = [125,135,100,80,50,80]
for h,w in zip(header,headerwidth):
    resulttable.column(h,width=w)

All_T = {} #สร้าง Dic เพื่อรวมชุดข้อมูลสำหรับค้นหาใน CSV

#สร้างฟังชั่นสำหรับเขียน csv ใหม่
def UpdateCSV():
    with open ('savedata.csv','w',newline='',encoding='utf-8') as f:
        fw = csv.writer(f)
        # เตรียมข้อมูลให้กลายเป็น list
        data = list(All_T.values())
        fw.writerows(data) #multiple line from nest list
        # print('table was update')
        

def updateSQL():
    data = list(All_T.values())
    #print ('update:',data[0])
    for d in data:
        Update(d[0],d[2],d[3],d[4],d[5])

#สร้างฟังก์ชั่นสำหรับปุ่ม delete
def Del_Rec(event=None): #ผูกไฟล์แล้วอย่าลืมใส่ event = None
    try:
        check = messagebox.askyesno('Confirm?','คุณต้องการลบข้อมูลใช่หรือไม่?') 
        #สร้าง checkbox yes/no
        # print ('Yes/No:',check)

        if check == True:
            # print('delete')
            select = resulttable.selection()
            #print (select)
            data = resulttable.item(select)
            data = data['values']
            t_id = data[0]
            #print(T_ID)
            del All_T[str(t_id)]
            #print(All_T)
            #UpdateCSV()
            Delete(str(t_id))
            upadate_table() #ลบแล้วอย่าลืมอัพเดท
        else:
            # print('Canceled')
            pass
    except:
        # print('ERROR:')
        messagebox.showwarning('Error','กรุณาเลือกข้อมูลที่ต้องการลบ')


# สร้างปุ่ม delete
B_Del = ttk.Button(tab2,text='Delete',command=Del_Rec)
B_Del.place(x=50,y=500)

resulttable.bind('<Delete>',Del_Rec)

# ใส่ value ให้ตารางที่สร้างไว้ อัพเดทข้อมูล
def upadate_table():
    resulttable.delete(*resulttable.get_children()) #ล้างข้อมูลเก่าเพื่อไม่ให้เขียนซ้ำ
    try: #ตรวจหาไฟล์ในกรณไม่มีไฟล์ข้อมูล ถ้าไม่มีก็ให้ข้ามไป
        data = show_expense()#read_csv()
        for d in data:
            # สร้าง All_T data
            All_T[d[1]] = d[1:]
            resulttable.insert('',0,values=d[1:])
        #print(All_T)
    except:
        # print('No File')
        pass

#########Right Click Manu##########
def Edit_Rec():
    POPUP = Toplevel()
    POPUP.geometry('300x300')
    POPUP.title('แก้ไขข้อมูล')

    L1 = ttk.Label(POPUP,text='รายการค่าใช้จ่าย',font=Font1).pack()
    v_expense = StringVar() #ตัวแปลพิเศษสำหรับเก็บข้อมูลใน GUI
    E1 = ttk.Entry(POPUP,textvariable=v_expense,font=Font2)
    E1.pack()
    #-------------------------

    #-------text2--------
    L2 = ttk.Label(POPUP,text='ราคา (บาท)',font=Font1).pack()
    v_price = StringVar()
    E2 = ttk.Entry(POPUP,textvariable=v_price,font=Font2)
    E2.pack()
    #-------------------------

    #-------text3--------
    L3 = ttk.Label(POPUP,text='จำนวน (ชิ้น)',font=Font1).pack()
    v_count = StringVar()
    E3 = ttk.Entry(POPUP,textvariable=v_count,font=Font2)
    E3.pack()
    #-------------------------

    def Edit():
        old_data = All_T[str(t_id)] #ดึงข้อมูลเก่า
        #print('OLD:',old_data)
        v1 = v_expense.get()
        p1 = float(v_price.get())
        c1 = float(v_price.get())
        total = p1*c1
        new_data = [old_data[0],old_data[1],v1,p1,c1,total] #เปลี่ยนเป็นข้อมูลใหม่
        All_T[str(t_id)] = new_data #อัพเดทข้อมูลในทรานเซคชั่น
        #UpdateCSV()
        updateSQL()
        #Update(old_data[0],old_data[1],v1,p1,c1,total)#single record
        upadate_table() #เสร็จแล้วอย่าลืมอัพเดตนะ
        POPUP.destroy() #สั่งปิดหน้าต่าง

    B1 = ttk.Button(POPUP, image=ic1, text = 'Save' , command=Edit,compound=LEFT)
    B1.pack(pady=15)

    
    # เลือกข้อมูลสำหรับช่องแก้ไข
    select = resulttable.selection()
    data = resulttable.item(select)
    data = data['values']
    t_id = data[0]

    #เซ็ตค่าเก่าข้อมูล
    v_expense.set(data[2])
    v_price.set(data[3])
    v_count.set(data[4])

    POPUP.mainloop()

r_click = Menu(root,tearoff=0)
r_click.add_command(label='Edit',command=Edit_Rec)
r_click.add_command(label='Delete',command=Del_Rec)

def m_pop(event):
    # print(event.x_root, event.y_root) #event.x_root, event.y_root ขอกตำแหน่งเมาส์
    r_click.post(event.x_root, event.y_root) # .post สร้าง popup

resulttable.bind('<Button-3>',m_pop) # เมื่อมีการคลิกขวาที่ resulable

upadate_table()
#updateSQL()
#print('Get CHILD:',resulttable.get_children())
root.bind('<Tab>', lambda x: E2.focus())
root.mainloop ()