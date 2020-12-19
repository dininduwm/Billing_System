from docx import Document
from docx.shared import Inches

# make rows bold
def make_rows_bold(*rows):
    for row in rows:
        for cell in row.cells:
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    run.font.bold = True

# creating the bill for print
def creatBill(data):
    document = Document()
    document.add_heading('Bill No: {}'.format(data['bill_no']))

    table = document.add_table(rows=4, cols=2)
    table.rows[0].cells[0].text = 'Date'
    table.rows[0].cells[1].text = data['date']
    table.rows[1].cells[0].text = 'ID No'
    table.rows[1].cells[1].text = data['id']
    table.rows[2].cells[0].text = 'Name'
    table.rows[2].cells[1].text = data['name']
    table.rows[3].cells[0].text = 'TP No'
    table.rows[3].cells[1].text = data['tp']

    # rented item detailed section
    document.add_heading('Rented Item details')

    table = document.add_table(rows=1, cols=6)
    table.style = 'Table Grid'  
    table.rows[0].cells[0].text = 'Name'
    table.rows[0].cells[1].text = 'Rented date'
    table.rows[0].cells[2].text = 'Days'
    table.rows[0].cells[3].text = 'Qty'
    table.rows[0].cells[4].text = 'Rate'
    table.rows[0].cells[5].text = 'Amount'

    make_rows_bold(table.rows[0])

    for item in data['RentedItems']:
        row_cells = table.add_row().cells
        row_cells[0].text = item[0]
        row_cells[1].text = item[1]
        row_cells[2].text = item[2]
        row_cells[3].text = item[3]
        row_cells[4].text = item[4]
        row_cells[5].text = item[5]

    # total Row
    row = table.add_row()
    row_cells = row.cells
    row_cells[1].text = "Total"
    row_cells[5].text = '{:10,.2f}'.format(data['ItemTotal'])
    make_rows_bold(row)

    document.add_heading('Payment Details', level=1)
    table = document.add_table(rows=5, cols=2)
    table.style = 'Table Grid'  

    table.rows[0].cells[0].text = 'Previous Amount'
    table.rows[0].cells[1].text = 'Rs. {:10,.2f}'.format(data['payment']+data['amountToBe']-data['ItemTotal'])
    table.rows[1].cells[0].text = 'This bill Amount'
    table.rows[1].cells[1].text = 'Rs. {:10,.2f}'.format(data['ItemTotal'])
    table.rows[2].cells[0].text = 'Total Amount For this Bill'
    table.rows[2].cells[1].text = '            Rs. {:10,.2f}'.format(data['payment']+data['amountToBe'])
    table.rows[3].cells[0].text = 'Payment'
    table.rows[3].cells[1].text = '-(Rs. {:10,.2f})'.format(data['payment'])
    table.rows[4].cells[0].text = 'Amount to be paid'
    table.rows[4].cells[1].text = '            Rs. {:10,.2f}'.format(data['amountToBe'])

    make_rows_bold(table.rows[0], table.rows[1], table.rows[2], table.rows[3], table.rows[4])

    document.save('demo.docx')


data = {
    'bill_no': '0001',
    'id': '199732400730',
    'name': 'Dinindu Udana Thilakarathna',
    'tp': '0777186434',
    'date': '2020-12-10 17:36:41',
    'payment': 13000,
    'amountToBe': 12000,
    'RentedItems': [
        ['Poker sdrfgsdfgsdfg sdfg sdfgs', '2020-12-10', '2', '2', '1,500', '12,000'],
        ['Poker', '2020-12-10', '2', '2', '1,500', '12,000'],
        ['Poker', '2020-12-10', '2', '2', '1,500', '12,000'],
        ['Poker', '2020-12-10', '2', '2', '1,500', '12,000'],
    ],
    'ItemTotal': 10000,
}

creatBill(data)