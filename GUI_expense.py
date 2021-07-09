# GUI Basic.py
import builtins
from tkinter import *
from tkinter import ttk, messagebox
from tkinter.font import Font #theme
from datetime import datetime
import csv

root = Tk () 
root.title('โปรแกรมบันทึกค่าใช้จ่าย By ปาร์ค')
root.geometry ('600x500') 

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
        'Tus':'อังคาร',
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
    price = v_price.get()
    count = v_count.get()
    if expense == '':
        messagebox.showwarning('Error','กรุณากรอกชื่อสินค้า')
    elif price == '':
        messagebox.showwarning('Error','กรุณากรอกราคาสินค้า')
    elif count == '':
        count = 1
    today = datetime.now().strftime('%a')
    dt = datetime.now().strftime('%d-%m-%Y %H:%M')
    dt = days[today] + 'ที่ ' + dt
    try:
        total = float(price)*float(count)
        print('วัน {} ซื้อ{} ราคา {} บาท จำนวน {} รวมทั้งหมด {} บาท'.format(dt,expense,price,count,total))
        text = 'วัน{}\nซื้อ{} \nราคา {} บาท จำนวน {} \nรวมทั้งหมด {} บาท'.format(dt,expense,price,count,total)
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
            data = [dt,expense,price,count,total]
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
header = ['วัน-เวลา','ราการ','ค่าใช้จ่าย','จำนวน','รวม']
resulttable = ttk.Treeview(tab2,columns=header,show='headings',height=20)
resulttable.pack(pady=10)

# ใส่ข้อความลง header ในตาราง
for h in header:
    resulttable.heading(h,text=h)

# กำหนดความกว้างของตาราง zip ใช้ในการรวมลิสเข้าด้วยกัน
headerwidth = [150,170,80,80,80]
for h,w in zip(header,headerwidth):
    resulttable.column(h,width=w)

# ใส่ value ให้ตารางที่สร้างไว้ อัพเดทข้อมูล
def upadate_table():
    resulttable.delete(*resulttable.get_children()) #ล้างข้อมูลเก่าเพื่อไม่ให้เขียนซ้ำ
    data = read_csv()
    for d in data:
        resulttable.insert('',0,values=d)

upadate_table()

root.bind('<Tab>', lambda x: E2.focus())
root.mainloop ()