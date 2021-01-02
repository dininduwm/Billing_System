import requests
import json
from tkinter import messagebox

URL = "https://aldermanly-dwell.000webhostapp.com/api/"

# create new coustomer
def createCustomer(nic, name, tp):
    data = {'nic': nic, 'name': name, 'tp': tp}

    with requests.get(url=URL+'insertUserNew.php', params=data) as req:
        if req.status_code == 200:
            # decoding the json string
            data = json.loads(req.text)
            if (data['response'] == 'Ok'):
                messagebox.showinfo(title="Rent Page", message="Adding user successful")
                return True
            else:
                messagebox.showerror(title="Rent Page", message="Adding new user faild")
        else:
            messagebox.showerror(title="Rent Page", message="Network or server Error")
    return False


# taking a customer
def getCustomer(nic):
    data = {'nic': nic}

    with requests.get(url=URL+'getUser.php', params=data) as req:
        if req.status_code == 200:
            print(req.text)
            data = json.loads(req.text)
            print(data)
            if len(data['details']) > 0:
                messagebox.showinfo(title="Rent Page", message="Customer details loaded")
                return (data['details'][0], data['billed_item'], data['payments'])
            else:
                messagebox.showinfo(title="Rent Page", message="Customer not found. Please create a new user")
        else:
            messagebox.showerror(title="Rent Page", message="Network or server Error")

    return None

# taking a equip
def getEquipment(code):
    data = {'code': code}

    with requests.get(url=URL+'getEquip.php', params=data) as req:
        if req.status_code == 200:
            print(req.text)
            data = json.loads(req.text)
            print(data)
            if len(data['details']) > 0:
                messagebox.showinfo(title="Rent Page", message="Equipment details loaded")
                return data['details'][0]
            else:
                messagebox.showinfo(title="Rent Page", message="Invalid code.")
        else:
            messagebox.showerror(title="Rent Page", message="Network or server Error")

    return None

# sending the bill data to the server
def setBillData(rentListNew, rentListChange, payment, date, bill_no, nic, availQtyChange):
    #chage data type
    qty = []
    for key in availQtyChange:
        qty.append(availQtyChange[key])

    data = {
        'rent_new': rentListNew,
        'rent_change': rentListChange,
        'payment': payment,
        'qty': qty,
    }

    print(data)

    reqData = {
        'data': json.dumps(data),
        'date': date,
        'nic': nic,
        'bill_no': bill_no,
    }

    with requests.post(url=URL+'saveBill.php', data=reqData) as req:
        if req.status_code == 200:
            print(req.text)
            messagebox.showinfo(title="Rent Page", message="Data saving successfull")
            return True
        else:
            messagebox.showerror(title="Rent Page", message="Network or server Error")

    return False