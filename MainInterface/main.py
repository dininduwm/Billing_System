from tkinter import *
from time import sleep

# main window
root = Tk()
root.title("Purchase Page")

def test():
    print("destroy")
    for item in listItems:
        item.destroy()

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
searchButton = Button(customerDetail, text="Search Customer", width=20)
searchButton.grid(row=0, column=2, padx=5)
nameEntry = Entry(customerDetail, width=60)
nameEntry.grid(row=1, column=1, pady=10)
addButton = Button(customerDetail, text="Add Customer", width=20, command=test)
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

# frame for the purchased item list
purchasedItems = Frame(root, highlightbackground="black", highlightthickness=1, height=100)
purchasedItems.grid(row=2, column=0, padx=10, pady=10, sticky=NSEW)

def on_configure(event):
    # update scrollregion after starting 'mainloop'
    # when all widgets are in canvas
    canvas.configure(scrollregion=canvas.bbox('all'))

# --- create canvas with scrollbar ---

canvas = Canvas(purchasedItems)
canvas.pack(side=LEFT, expand=True, fill="both")

scrollbar = Scrollbar(purchasedItems, command=canvas.yview)
scrollbar.pack(side=RIGHT, fill='y', expand=False)

canvas.configure(yscrollcommand = scrollbar.set)

# update scrollregion after starting 'mainloop'
# when all widgets are in canvas
canvas.bind('<Configure>', on_configure)

# --- put frame in canvas ---

frame = Frame(canvas)
canvas.create_window((0,0), window=frame, anchor='nw')

# crating the header of the table
H01 = Label(frame, text="Item Code", height=2, bg='grey', fg='white', borderwidth=3, relief="groove").grid(row=0, column=0, sticky='we')
H02 = Label(frame, text="Item Name", height=2, bg='grey', fg='white', borderwidth=3, relief="groove").grid(row=0, column=1, sticky='we')
H03 = Label(frame, text="Purchased Date", height=2, bg='grey', fg='white', borderwidth=3, relief="groove").grid(row=0, column=2, sticky='we')
H04 = Label(frame, text="Qty", height=2, bg='grey', fg='white', borderwidth=3, relief="groove").grid(row=0, column=3, sticky='we')
H05 = Label(frame, text="Rate", height=2, bg='grey', fg='white', borderwidth=3, relief="groove").grid(row=0, column=4, sticky='we')
H06 = Label(frame, text="Amount", height=2, bg='grey', fg='white', borderwidth=3, relief="groove").grid(row=0, column=5, sticky='we')

listItems = []

for i in range(20):
    label = Label(frame, text="***************", height=1, bg='grey10', fg='white', borderwidth=1, relief="groove")
    #label.after(1000, label.master.destroy)
    label.grid(row=i+1, column=0)
    listItems.append(label)


# main loop of the programme
root.mainloop()


