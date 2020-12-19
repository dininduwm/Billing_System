from docx import Document
from docx.shared import Inches

# document = Document()

# document.add_heading('Document Title', 0)

# p = document.add_paragraph('A plain paragraph having some ')
# p.add_run('bold').bold = True
# p.add_run(' and some ')
# p.add_run('italic.').italic = True

# document.add_heading('Heading, level 1', level=1)
# document.add_paragraph('Intense quote', style='Intense Quote')

# document.add_paragraph(
#     'first item in unordered list', style='List Bullet'
# )
# document.add_paragraph(
#     'first item in ordered list', style='List Number'
# )

# #document.add_picture('monty-truth.png', width=Inches(1.25))

# records = (
#     (3, '101', 'Spam'),
#     (7, '422', 'Eggs'),
#     (4, '631', 'Spam, spam, eggs, and spam')
# )

# table = document.add_table(rows=1, cols=3)
# hdr_cells = table.rows[0].cells
# hdr_cells[0].text = 'Qty'
# hdr_cells[1].text = 'Id'
# hdr_cells[2].text = 'Desc'
# for qty, id, desc in records:
#     row_cells = table.add_row().cells
#     row_cells[0].text = str(qty)
#     row_cells[1].text = id
#     row_cells[2].text = desc

# document.add_page_break()

# document.save('demo.docx')

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
    document.add_heading('Bill No: {}'.format(data['bill_no']), 0)

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
    row_cells[5].text = data['ItemTotal']
    make_rows_bold(row)

    document.add_heading('Amount to be paid:       Rs. {:,.2f}'.format(float(data['amount'])), level=1)

    document.save('demo.docx')


data = {
    'bill_no': '0001',
    'id': '199732400730',
    'name': 'Dinindu Udana Thilakarathna',
    'tp': '0777186434',
    'date': '2020-12-25',
    'amount': 12000,
    'RentedItems': [
        ['Poker sdrfgsdfgsdfg sdfg sdfgs', '2020-12-10', '2', '2', '1,500', '12,000'],
        ['Poker', '2020-12-10', '2', '2', '1,500', '12,000'],
        ['Poker', '2020-12-10', '2', '2', '1,500', '12,000'],
        ['Poker', '2020-12-10', '2', '2', '1,500', '12,000'],
    ],
    'ItemTotal': '48,000'
}

creatBill(data)