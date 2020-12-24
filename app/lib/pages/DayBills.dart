import 'package:app/data_types/Bill.dart';
import 'package:app/services/GetDayBills.dart';
import 'package:app/shared/loading.dart';
import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'package:toast/toast.dart';

class DayBills extends StatefulWidget {
  @override
  _TodayBillsState createState() => _TodayBillsState();
}

class _TodayBillsState extends State<DayBills> {
  List<Bill> bills = [
    Bill(billNo: '0001', date: '2020-12-20 12:00:00', amount: '1000'),
  ]; // bill list
  double total = 15000;
  bool loading = true; // true if loading
  final oCcy = new NumberFormat("#,##0.00", "en_US");
  DateTime dateSelected; // date time to store the current date

  @override
  void initState() {
    // TODO: implement initState
    super.initState();
    // do the fetching
    updateBills(DateTime.now());
  }

  void updateBills(date) async {
    if (date != null) {
      bool res = await GetDayBills.getDayBills(date);
      if (res) {
        setState(() {
          bills = GetDayBills.bills;
          total = GetDayBills.total;
          loading = false;
        });
      } else {
        setState(() {
          loading = false;
        });
        Toast.show(
          "Error loading data, Please try again",
          this.context,
          duration: Toast.LENGTH_LONG,
          gravity: Toast.BOTTOM,
        );
        Navigator.pop(context);
      }
    } else {
      loading = false;
    }
  }

  @override
  Widget build(BuildContext context) {
    return loading
        ? Loading()
        : Scaffold(
            appBar: AppBar(
              title: Text("Day Bills"),
              backgroundColor: Colors.blue,
            ),
            body: Column(
              children: [
                Card(
                  color: Colors.blue[600],
                  child: Row(
                    children: [
                      Padding(
                        padding: const EdgeInsets.symmetric(
                          horizontal: 8.0,
                          vertical: 4.0,
                        ),
                        child: RaisedButton(
                          color: Colors.amber,
                          child: Text(
                            "Pick a date",
                            style: TextStyle(
                              color: Colors.black,
                            ),
                          ),
                          onPressed: () {
                            showDatePicker(
                              context: context,
                              initialDate: DateTime.now(),
                              firstDate: DateTime(2020),
                              lastDate: DateTime(2025),
                            ).then((date) {
                              setState(() {
                                dateSelected = date;
                                loading = true;
                                updateBills(date);
                              });
                            });
                          },
                        ),
                      ),
                      Expanded(
                        child: SizedBox(),
                      ),
                      Padding(
                        padding: const EdgeInsets.only(right: 15.0),
                        child: Text(
                          dateSelected == null
                              ? DateFormat('yyyy-MM-dd').format(DateTime.now())
                              : DateFormat('yyyy-MM-dd').format(dateSelected),
                          style: TextStyle(
                              color: Colors.white,
                              fontSize: 22,
                              fontWeight: FontWeight.bold),
                        ),
                      ),
                    ],
                  ),
                ),
                Expanded(
                  child: ListView.builder(
                    itemCount: bills == null ? 0 : bills.length,
                    itemBuilder: (context, index) {
                      return Padding(
                        padding: const EdgeInsets.symmetric(
                          vertical: 1.0,
                          horizontal: 4.0,
                        ),
                        child: Card(
                          child: Padding(
                            padding: EdgeInsets.all(8.0),
                            child: Row(
                              children: [
                                Column(
                                  children: [
                                    Text(bills[index].date),
                                    Text(
                                      bills[index].billNo,
                                      style: TextStyle(
                                        fontSize: 16,
                                        fontWeight: FontWeight.bold,
                                      ),
                                    ),
                                  ],
                                ),
                                Expanded(child: SizedBox()),
                                Text(
                                  "Rs. ${oCcy.format(double.parse(bills[index].amount))}",
                                  style: TextStyle(
                                    fontWeight: FontWeight.bold,
                                    fontSize: 20,
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ),
                      );
                    },
                  ),
                ),
                Padding(
                  padding: const EdgeInsets.symmetric(
                    vertical: 1.0,
                    horizontal: 4.0,
                  ),
                  child: Card(
                    color: Colors.blue[600],
                    child: Padding(
                      padding: const EdgeInsets.all(8.0),
                      child: Row(
                        children: [
                          Text(
                            "Total",
                            style: TextStyle(
                              color: Colors.white,
                              fontSize: 25,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                          Expanded(
                            child: SizedBox(),
                          ),
                          Text(
                            "Rs. ${oCcy.format(total)}",
                            style: TextStyle(
                              color: Colors.white,
                              fontSize: 25,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                ),
              ],
            ),
          );
  }
}
