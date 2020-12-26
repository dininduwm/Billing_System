from tkinter import *
from tkinter import simpledialog, messagebox
from time import sleep
from fetchData import *
from createBill import createBill
from datetime import date, datetime

# variables to handle the preocess
isItemLoaded = False
itemData = None
billNo = '0022'
listItems_pay = []
paymentList = []
rentListChanges = []
rentListNew = []
payment = None
dataToPrint = {
    'bill_no': '',
    'id': '',
    'name': '',
    'tp': '',
    'date': '',
    'payment': 0,
    'amountToBe': 0,
    'RentedItems': [],
    'ItemTotal': 0,
}
amountToBePaid = 0

# main window
root = Tk()
root.title("Renting Page")
root.geometry("1600x700")

def createCustomerButton():
    nic = nicEntry.get()
    name = nameEntry.get()
    tp = tpEntry.get()
    # saving data
    createCustomer(nic, name, tp)

def searchCustomerButton():
    global dataToPrint

    nic = nicEntry.get()
    data = getCustomer(nic)
    if data[0]:
        nameEntry.delete(0, 'end')
        tpEntry.delete(0, 'end')
        nameEntry.insert(0, data[0]['name'])
        tpEntry.insert(0, data[0]['tp'])
        # adding details to print
        dataToPrint['bill_no'] = billNo
        dataToPrint['id'] = nic
        dataToPrint['name'] = data[0]['name']
        dataToPrint['tp'] = data[0]['tp']

        fillRentedList(data[1])
        fillPaymentList(data[2])
        fillPrintData()

def searchEquipButton():
    global isItemLoaded
    global itemData

    code = itemCodeEntry.get()
    data = getEquipment(code)
    if data:
        # setting the variables
        isItemLoaded = True
        itemData = data
        itemData['code'] = code

        itemRateLabel.configure(text='Item Rate                 ---> {:0,.2f}'.format(float(data['rate'])))
        itemQtyLabel.configure(text='Item Available Qty  ---> {}'.format(int(data['qty'])))
        itemDescLabel.configure(text='Item Description     ---> {}'.format(data['desc']))

# renting new item button
def rentItemButton():
    # date format
    format = "%Y-%m-%d %H:%M:%S"

    if (isItemLoaded):
        qty = int(itemRentQtyEntry.get())
        if qty <= int(itemData['qty']):
            # add new Item to the renting list
            rentList.append([itemData['code'], itemData['desc'], datetime.now().strftime(format), billNo, qty, int(itemData['rate']), 0, 0, '', False])
            # list to be updated
            rentListNew.append([itemData['code'], datetime.now().strftime(format), billNo, qty])
            
            # adding data to the bill
            calculateCost()
            item = rentList[-1]
            # converting the date
            date = datetime.strptime(item[2], "%Y-%m-%d %H:%M:%S")
            # adding to the print bill list
            arr = [item[1], date.strftime("%Y-%m-%d"), item[6], item[4], '{:0,.2f}'.format(item[5]), item[7]]
            dataToPrint['RentedItems'].append(list(map(str, arr)))

            # updating the rent table
            updateRentTable()
        else:
            messagebox.showerror(title="Rent Page", message="Qty exceed the available qty")
    else:
        messagebox.showerror(title="Rent Page", message="Item not loaded")

    itemRentQtyEntry.delete(0, 'end')

# button to make a payment
def makePaymentButton():
    # date format
    format = "%Y-%m-%d %H:%M:%S"
    paymentList.append([datetime.now().strftime(format), billNo, descEntry.get(), int(amountEntry.get())])
    updatePayTable()    

    global payment
    # date format
    payment = [datetime.now().strftime(format), billNo, descEntry.get(), int(amountEntry.get())]
    descEntry.delete(0, 'end')
    amountEntry.delete(0, 'end')
    payButton.config(state='disabled')

# printing the bill
def printBillButton():
    global dataToPrint
    global billNo

    print('change rent', rentListChanges)
    print('new rent', rentListNew)
    print('payment', payment)
    print('print data', dataToPrint)

    # printin bill procedure    
    dataToPrint['amountToBe'] = amountToBePaid
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dataToPrint['date'] = date
    tot = 0
    for item in dataToPrint['RentedItems']:
        tot += float(item[5].replace(',',''))
    dataToPrint['ItemTotal'] = tot
    if payment:
        dataToPrint['payment'] = float(payment[-1])

    # send bil to database
    if (setBillData(rentListNew, rentListChanges, payment, date, billNo, nicEntry.get())):
        # creating the bill
        createBill(dataToPrint, billNo)
        billNo = "%04d"%(int(billNo)+1)
        print(billNo)

def calculateCost():
    # date format
    format = "%Y-%m-%d %H:%M:%S"

    ammount = 0
    for item in rentList:
        if item[9]:
            returnedDate = datetime.strptime(item[8], format)
        else:
            returnedDate = datetime.now()
        rentedDate = datetime.strptime(item[2], format)
        hours = (returnedDate-rentedDate).total_seconds()/(3600)
        if (hours <= 6):
            days = 0.5
        else:
            days = hours//24
            if hours%24 > 2:
                days += 1
            days = max(1, days)
        # calculating the cost
        item[6] = str(days)
        item[7] = '{:0,.2f}'.format(float(item[4])*float(item[5])*days)

# calculate tehe ammount to be recieved
def calculateAmmountRec():
    global amountToBePaid

    tot = 0
    for item in rentList:
        try:
            tot += float(item[7].replace(',', ''))
        except:
            pass

    for item in paymentList:
        try:
            tot -= item[3]
        except:
            pass
    
    print("Total = ", tot)
    amountToBePaid = tot
    amountLabel.configure(text='Rs. {:0,.2f}'.format(tot))

# fill the rented item list after fetching a costomer
def fillRentedList(data):
    #['0001', '***************************************', '2020-12-10 17:36:41', 'B001', 2, 1500, 0, 0, '', False],
    global rentList
    global dataToPrint
    rentList = []
    dataToPrint['RentedItems'] = []

    for item in data:
        if item['returned_date']:
            returnedState = True
            returnedDate = item['returned_date']
        else:
            returnedState = False
            returnedDate = '' 
        rentList.append([item['code'], item['description'], item['rented_date'], item['bill_no'], int(item['qty']), float(item['rate']),0,0,returnedDate, returnedState])
        
    #print(rentList)
    updateRentTable()

# filling the print data list initialy
def fillPrintData():
    for item in rentList:
        if not item[-1]:
            #['Poker', '2020-12-10', '2', '2', '1,500', '12,000'],
            # converting the date
            date = datetime.strptime(item[2], "%Y-%m-%d %H:%M:%S")
            # adding to the print bill list
            arr = [item[1], date.strftime("%Y-%m-%d"), item[6], item[4], '{:0,.2f}'.format(item[5]), item[7]]
            dataToPrint['RentedItems'].append(list(map(str, arr)))

# fill the payment item list after fetching a costomer
def fillPaymentList(data):
    global paymentList    
    paymentList = []
    for item in data:
        #['2020-12-12', 'asdjfasdjfalsdfasdfasdf', 1500]
        paymentList.append([item['date'], item['bill_no'], item['description'], float(item['amount'])])
    updatePayTable()

# command for returning item
def returnItem(index):    
    # date format
    format = "%Y-%m-%d %H:%M:%S"

    if rentList[index][4] > 1:
        # asking for the number of qty returened
        USER_INP = simpledialog.askinteger(title="Test",
                                    prompt="Number of items returened (Enter -1 if all the items returned)")
        if (USER_INP == -1 or int(USER_INP) > rentList[index][4]):
            pass
        else:
            rentList.append(rentList[index].copy())
            rentList[-1][4] -= int(USER_INP)
            rentList[-1][3] = billNo
            rentList[index][4] = int(USER_INP)
            # add the item to new item added list
            rentListNew.append([rentList[-1][0], rentList[-1][2], rentList[-1][3], rentList[-1][4]])

    rentList[index][9] = True
    rentList[index][8] = datetime.now().strftime(format)

    # new item added to the item chnged list
    rentListChanges.append([rentList[index][0], rentList[index][3], rentList[index][4], rentList[index][8]])
    
    updateRentTable()

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
itemDescLabel = Label(itemDetail, text="Item Description     ---> ")
itemDescLabel.grid(row=1, column=0, sticky=W, columnspan=2, pady=10)
itemRateLabel = Label(itemDetail, text="Item Rate                 ---> ")
itemRateLabel.grid(row=2, column=0, sticky=W)
itemQtyLabel = Label(itemDetail, text="Item Available Qty  ---> ")
itemQtyLabel.grid(row=3, column=0, sticky=W, columnspan=2, pady=10)
itemRentQtyLabel = Label(itemDetail, text="Renting Qty")
itemRentQtyLabel.grid(row=4, column=0, sticky=W,)

itemCodeEntry = Entry(itemDetail, width=30, )
itemCodeEntry.grid(row=0, column=1, pady=10)
itemRentQtyEntry = Entry(itemDetail, width=30, )
itemRentQtyEntry.grid(row=4, column=1, pady=10)

searchItemButton = Button(itemDetail, text="Search Item", width=20, command=searchEquipButton)
searchItemButton.grid(row=0, column=2, padx=5)
rentItemButton = Button(itemDetail, text="Rent Item", width=20, command=rentItemButton)
rentItemButton.grid(row=4, column=2, padx=5)

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
H03 = Label(frame, text="Rented Date", height=2, bg='grey', fg='white', borderwidth=3, relief="groove").grid(row=0, column=2, sticky='we')
H04 = Label(frame, text="Bill No", height=2, bg='grey', fg='white', borderwidth=3, relief="groove").grid(row=0, column=3, sticky='we')
H05 = Label(frame, text="Qty", height=2, bg='grey', fg='white', borderwidth=3, relief="groove").grid(row=0, column=4, sticky='we')
H06 = Label(frame, text="Rate/ Day", height=2, bg='grey', fg='white', borderwidth=3, relief="groove").grid(row=0, column=5, sticky='we')
H07 = Label(frame, text="Day", height=2, bg='grey', fg='white', borderwidth=3, relief="groove").grid(row=0, column=6, sticky='we')
H08 = Label(frame, text="Amount", height=2, bg='grey', fg='white', borderwidth=3, relief="groove").grid(row=0, column=7, sticky='we')
H09 = Label(frame, text="Returned Date", height=2, bg='grey', fg='white', borderwidth=3, relief="groove").grid(row=0, column=8, sticky='we')
H10 = Label(frame, text="Returned", height=2, bg='grey', fg='white', borderwidth=3, relief="groove").grid(row=0, column=9, sticky='we')

listItems = []

# list which use to build tables
rentList = []

def updateRentTable():
     # calculating the calculate cost
    calculateCost()
    
    global scrollbar
    global listItems
    global rentList

    # removing previous items
    for item in listItems:
        item.destroy()
    
    listItems = []

    # sorting the list
    rentList = sorted(rentList, key=lambda item: (~item[-1], item[2]), reverse=True)


    for index in range(len(rentList)):
        for dataIndex in range(len(rentList[0])):
            if not dataIndex == len(rentList[0])-1:
                label = Label(frame, text=str(rentList[index][dataIndex]), height=2, bg='grey10', fg='white', borderwidth=1, relief="groove")
                #label.after(1000, label.master.destroy)
            else:
                if (rentList[index][dataIndex]):
                    label = Label(frame, height=2, bg='green', fg='white', borderwidth=1, relief="groove")
                else:
                    label = Label(frame, height=2, bg='red', fg='white', borderwidth=1, relief="groove") 
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
H02 = Label(frame_pay, text="Bill No", height=2, bg='grey', fg='white', borderwidth=3, relief="groove").grid(row=0, column=1, sticky='we')
H03 = Label(frame_pay, text="Description", height=2, bg='grey', fg='white', borderwidth=3, relief="groove").grid(row=0, column=2, sticky='we')
H04 = Label(frame_pay, text="Ammount", height=2, bg='grey', fg='white', borderwidth=3, relief="groove").grid(row=0, column=3, sticky='we')

def updatePayTable():
    global scrollbar_pay
    global listItems_pay
    global paymentList

    # removing previous items
    for item in listItems_pay:
        item.destroy()
    
    listItems_pay = []

    # sorting the list
    paymentList = sorted(paymentList, key=lambda item: item[0], reverse=True)

    for index in range(len(paymentList)):
        for dataIndex in range(len(paymentList[0])):
            if (dataIndex == len(paymentList[index])-1):
                label = Label(frame_pay, text='{:0,.2f}'.format(paymentList[index][dataIndex]), height=1, bg='grey10', fg='white', borderwidth=1, relief="groove")
            else:
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

amountLabel_ = Label(paymentStat, text="Amount to be recieved", font=("Courier", 30))
amountLabel_.grid(row=0, column=0, padx=10, pady=10, columnspan=3)
amountLabel = Label(paymentStat, text="Rs. 100000", font=("Courier", 44))
amountLabel.grid(row=1, column=0, padx=10, pady=10, columnspan=3)

labelTmp = Label(paymentStat, text="Description ",)
labelTmp.grid(row=2, column=0)
descEntry = Entry(paymentStat, width=30)
descEntry.grid(row=2, column=1, pady=10)
labelTmp = Label(paymentStat, text="Amount Paid ",)
labelTmp.grid(row=3, column=0)
amountEntry = Entry(paymentStat, width=30)
amountEntry.grid(row=3, column=1, pady=10)

payButton = Button(paymentStat, text="Make Payment", height=3, bg="green", fg="white", command=makePaymentButton)
payButton.grid(row=4, column=0, sticky=EW, padx=10)
printBillButton = Button(paymentStat, text="Print Bill", height=3, bg="grey", fg="white", command=printBillButton)
printBillButton.grid(row=5, column=0, sticky=EW, padx=10, pady=5)

updatePayTable()
updateRentTable()
# main loop of the programme
root.mainloop()