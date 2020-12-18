from tkinter import *
from time import sleep
from fetchData import *
from datetime import date

# main window
root = Tk()
root.title("Renting Page")
root.geometry("1500x700")

def test():
    updateRentTable()
    updatePayTable()

def createCustomerButton():
    nic = nicEntry.get()
    name = nameEntry.get()
    tp = tpEntry.get()
    # saving data
    createCustomer(nic, name, tp)

def searchCustomerButton():
    nic = nicEntry.get()
    data = getCustomer(nic)
    if data:
        nameEntry.insert(0, data['name'])
        tpEntry.insert(0, data['tp'])

def calculateCost():
    ammount = 0
    for item in rentList:
        if item[8]:
            returnedDate = date.fromisoformat(item[7])
        else:
            returnedDate = date.today()
        rentedDate = date.fromisoformat(item[2])
        days = (returnedDate-rentedDate).total_seconds()/(3600*24)
        days = max(1, days)
        # calculating the cost
        item[6] = '{:20,.2f}'.format(float(item[4])*float(item[5])*days)

# calculate tehe ammount to be recieved
def calculateAmmountRec():
    tot = 0
    for item in rentList:
        try:
            tot += float(item[6].replace(',', ''))
        except:
            pass

    for item in paymentList:
        try:
            tot -= float(item[2].replace(',', ''))
        except:
            pass
    
    print("Total = ", tot)
    amountLabel.configure(text='Rs. {:10,.2f}'.format(tot))

# command for returning item
def returnItem(index):
    rentList[index][8] = True
    rentList[index][7] = date.today().isoformat()
    updateRentTable()
    print("Item returned: {}".format(index))

# frame for the costomer details
customerDetail = Frame(root, highlightbackground="black", highlightthickness=1)
customerDetail.grid(row=0, column=0, padx=10, pady=10)
# creating the items inside the customer Frame
nicLabel = Label(customerDetail, text="National Id No ",)
nicLabel.grid(row=0, column=0)
nameLabel = Label(customerDetail, text="Name ")
nameLabel.grid(row=1, column=0, sticky=W) 
tpLabel = Label(customerDetail, text="Tp No ")
tpLabel.grid(row=2, column=0, sticky=W) 

nicEntry = Entry(customerDetail, width=60)
nicEntry.grid(row=0, column=1, pady=10)
searchButton = Button(customerDetail, text="Search Customer", width=20, command=searchCustomerButton)
searchButton.grid(row=0, column=2, padx=5)
nameEntry = Entry(customerDetail, width=80)
nameEntry.grid(row=1, column=1, pady=10)
addButton = Button(customerDetail, text="Add Customer", width=20, command=createCustomerButton)
addButton.grid(row=1, column=2, padx=5)
tpEntry = Entry(customerDetail, width=40)
tpEntry.grid(row=2, column=1, sticky=W, pady=5)

# frame for the item details
itemDetail = Frame(root, highlightbackground="black", highlightthickness=1)
itemDetail.grid(row=1, column=0, padx=10, sticky=NSEW)
# creating items inside the item details
itemCodeLabel = Label(itemDetail, text="Item code ")
itemCodeLabel.grid(row=0, column=0, sticky=W, columnspan=2)
itemRateLabel = Label(itemDetail, text="Item Rate                 ---> ")
itemRateLabel.grid(row=1, column=0, sticky=W, pady=10)
itemQtyLabel = Label(itemDetail, text="Item Available Qty  ---> ")
itemQtyLabel.grid(row=2, column=0, sticky=W, columnspan=2, pady=10)
itemRentQtyLabel = Label(itemDetail, text="Renting Qty")
itemRentQtyLabel.grid(row=3, column=0, sticky=W,)

itemCodeEntry = Entry(itemDetail, width=30, )
itemCodeEntry.grid(row=0, column=1, pady=10)
itemRentQtyEntry = Entry(itemDetail, width=30, )
itemRentQtyEntry.grid(row=3, column=1, pady=10)

searchItemButton = Button(itemDetail, text="Search Item", width=20)
searchItemButton.grid(row=0, column=2, padx=5)
rentItemButton = Button(itemDetail, text="Rent Item", width=20)
rentItemButton.grid(row=3, column=2, padx=5)

# frame for the rentd item list
rentdItems = Frame(root, highlightbackground="black", highlightthickness=1, height=100)
rentdItems.grid(row=2, column=0, padx=10, pady=10, sticky=NSEW)

def on_configure(event):
    # update scrollregion after starting 'mainloop'
    # when all widgets are in canvas
    canvas.configure(scrollregion=canvas.bbox('all'))

canvas = Canvas(rentdItems)
canvas.pack(side=LEFT, expand=True, fill="both")
scrollbar = Scrollbar(rentdItems, command=canvas.yview)
scrollbar.pack(side=RIGHT, fill='y', expand=False)
canvas.configure(yscrollcommand = scrollbar.set)
canvas.bind('<Configure>', on_configure)
frame = Frame(canvas)
canvas.create_window((0,0), window=frame, anchor='nw')

# crating the header of the table
H01 = Label(frame, text="Item Code", height=2, bg='grey', fg='white', borderwidth=3, relief="groove").grid(row=0, column=0, sticky='we')
H02 = Label(frame, text="Item Name", height=2, bg='grey', fg='white', borderwidth=3, relief="groove").grid(row=0, column=1, sticky='we')
H03 = Label(frame, text="Bill No", height=2, bg='grey', fg='white', borderwidth=3, relief="groove").grid(row=0, column=2, sticky='we')
H04 = Label(frame, text="Rented Date", height=2, bg='grey', fg='white', borderwidth=3, relief="groove").grid(row=0, column=3, sticky='we')
H05 = Label(frame, text="Qty", height=2, bg='grey', fg='white', borderwidth=3, relief="groove").grid(row=0, column=4, sticky='we')
H06 = Label(frame, text="Rate/ Day", height=2, bg='grey', fg='white', borderwidth=3, relief="groove").grid(row=0, column=5, sticky='we')
H07 = Label(frame, text="Amount", height=2, bg='grey', fg='white', borderwidth=3, relief="groove").grid(row=0, column=6, sticky='we')
H08 = Label(frame, text="Returned Date", height=2, bg='grey', fg='white', borderwidth=3, relief="groove").grid(row=0, column=7, sticky='we')
H09 = Label(frame, text="Returned", height=2, bg='grey', fg='white', borderwidth=3, relief="groove").grid(row=0, column=8, sticky='we')

listItems = []

rentList = [
    ['0001', '***************************************', '2020-12-12', 'B001', 2, 1500, 0, '', False],
    ['0001', '***************************************', '2020-12-12', 'B001', 2, 1500, 0, '', False],
    ['0001', '***************************************', '2020-12-12', 'B001', 2, 1500, 0, '', False],
    ['0001', '***************************************', '2020-12-12', 'B001', 2, 1500, 0, '', False],
    ['0001', '***************************************', '2020-12-12', 'B001', 2, 1500, 3000, '2020-12-13', True],
]

def updateRentTable():
     # calculating the calculate cost
    calculateCost()
    
    global scrollbar
    global listItems

    # removing previous items
    for item in listItems:
        item.destroy()
    
    listItems = []

    for index in range(len(rentList)):
        for dataIndex in range(len(rentList[0])):
            if not dataIndex == len(rentList[0])-1:
                label = Label(frame, text=str(rentList[index][dataIndex]), height=1, bg='grey10', fg='white', borderwidth=1, relief="groove")
                #label.after(1000, label.master.destroy)
            else:
                if (rentList[index][dataIndex]):
                    label = Label(frame, height=1, bg='green', fg='white', borderwidth=1, relief="groove")
                else:
                    label = Label(frame, height=1, bg='red', fg='white', borderwidth=1, relief="groove") 
                    button = Button(frame, text="Returned", command=lambda idx = index:returnItem(idx))
                    button.grid(row=index+1, column=dataIndex+1)
                    listItems.append(button)
            label.grid(row=index+1, column=dataIndex, sticky='we')
            listItems.append(label)
    try:
        # destroy and create new scrol bar
        scrollbar.destroy()
        root.update()
        scrollbar = Scrollbar(rentdItems, command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill='y', expand=False)
        canvas.configure(yscrollcommand = scrollbar.set)
        canvas.bind('<Configure>', on_configure)   
    except:
        pass

    # calculate the ammount ot be recieved
    calculateAmmountRec()

# frame for the payments item list
paymentItems = Frame(root, highlightbackground="black", highlightthickness=1, height=100, width=500)
paymentItems.grid(row=2, column=1, padx=10, pady=10, sticky=NSEW)

def on_configure_pay(event):
    # update scrollregion after starting 'mainloop'
    # when all widgets are in canvas
    canvas_pay.configure(scrollregion=canvas_pay.bbox('all'))
    
canvas_pay = Canvas(paymentItems)
canvas_pay.pack(side=LEFT, expand=True, fill="both")
scrollbar_pay = Scrollbar(paymentItems, command=canvas_pay.yview)
scrollbar_pay.pack(side=RIGHT, fill='y', expand=False)
canvas_pay.configure(yscrollcommand = scrollbar_pay.set)
canvas_pay.bind('<Configure>', on_configure_pay)
frame_pay = Frame(canvas_pay)
canvas_pay.create_window((0,0), window=frame_pay, anchor='nw')

# crating the header of the table
H01 = Label(frame_pay, text="Date", height=2, bg='grey', fg='white', borderwidth=3, relief="groove").grid(row=0, column=0, sticky='we')
H02 = Label(frame_pay, text="Description", height=2, bg='grey', fg='white', borderwidth=3, relief="groove").grid(row=0, column=1, sticky='we')
H03 = Label(frame_pay, text="Ammount", height=2, bg='grey', fg='white', borderwidth=3, relief="groove").grid(row=0, column=2, sticky='we')

listItems_pay = []

paymentList = [
    ['2020-12-12', 'asdjfasdjfalsdfasdfasdf', '1500'],
    ['2020-12-12', 'asdjfasdjfalsdfasdfasdf', '1500'],
    ['2020-12-12', 'asdjfasdjfalsdfasdfasdf', '1500'],
    ['2020-12-12', 'asdjfasdjfalsdfasdfasdf', '1500'],
    ['2020-12-12', 'asdjfasdjfalsdfasdfasdf', '1500'],
]

def updatePayTable():
    global scrollbar_pay
    global listItems_pay

    # removing previous items
    for item in listItems_pay:
        item.destroy()
    
    listItems_pay = []

    for index in range(len(paymentList)):
        for dataIndex in range(len(paymentList[0])):
            label = Label(frame_pay, text=str(paymentList[index][dataIndex]), height=1, bg='grey10', fg='white', borderwidth=1, relief="groove")
            #label.after(1000, label.master.destroy)
            label.grid(row=index+1, column=dataIndex, sticky='we')
            listItems_pay.append(label)

    try:
        # destroy and create new scrol bar
        scrollbar_pay.destroy()
        root.update()
        scrollbar_pay = Scrollbar(paymentItems, command=canvas_pay.yview)
        scrollbar_pay.pack(side=RIGHT, fill='y', expand=False)
        canvas_pay.configure(yscrollcommand = scrollbar_pay.set)
        canvas_pay.bind('<Configure>', on_configure_pay)
    except:
        pass

    # calculate the ammount ot be recieved
    calculateAmmountRec()

# frame for the payment status
paymentStat = Frame(root, highlightbackground="black", highlightthickness=1, height=100, width=500)
paymentStat.grid(row=0, column=1, padx=10, pady=10, rowspan=2, sticky=NSEW)

amountLabel_ = Label(paymentStat, text="Ammount to be recieved", font=("Courier", 30))
amountLabel_.grid(row=0, column=0, padx=10, pady=10, columnspan=3)
amountLabel = Label(paymentStat, text="Rs. 100000", font=("Courier", 44))
amountLabel.grid(row=1, column=0, padx=10, pady=10, columnspan=3)

labelTmp = Label(paymentStat, text="Ammount Paid ",)
labelTmp.grid(row=2, column=0)
amountEntry = Entry(paymentStat, width=30)
amountEntry.grid(row=2, column=1, pady=10)

payButton = Button(paymentStat, text="Make Payment", height=3, bg="green", fg="white")
payButton.grid(row=3, column=0, sticky=EW, padx=10)
printBillButton = Button(paymentStat, text="Print Bill", height=3, bg="grey", fg="white")
printBillButton.grid(row=4, column=0, sticky=EW, padx=10, pady=5)

updatePayTable()
updateRentTable()
# main loop of the programme
root.mainloop()