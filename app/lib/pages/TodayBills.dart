import 'package:app/data_types/Bill.dart';
import 'package:app/shared/loading.dart';
import 'package:flutter/material.dart';
import 'package:intl/intl.dart';

class TodayBills extends StatefulWidget {
  @override
  _TodayBillsState createState() => _TodayBillsState();
}

class _TodayBillsState extends State<TodayBills> {
  List<Bill> bills = [
    Bill(billNo: '0001', date: '2020-12-20 12:00:00', amount: '1000'),
    Bill(billNo: '0001', date: '2020-12-20 12:00:00', amount: '1000'),
    Bill(billNo: '0001', date: '2020-12-20 12:00:00', amount: '1000'),
    Bill(billNo: '0001', date: '2020-12-20 12:00:00', amount: '1000'),
    Bill(billNo: '0001', date: '2020-12-20 12:00:00', amount: '1000'),
    Bill(billNo: '0001', date: '2020-12-20 12:00:00', amount: '1000'),
    Bill(billNo: '0001', date: '2020-12-20 12:00:00', amount: '1000'),
    Bill(billNo: '0001', date: '2020-12-20 12:00:00', amount: '1000'),
    Bill(billNo: '0001', date: '2020-12-20 12:00:00', amount: '1000'),
    Bill(billNo: '0001', date: '2020-12-20 12:00:00', amount: '1000'),
    Bill(billNo: '0001', date: '2020-12-20 12:00:00', amount: '1000'),
    Bill(billNo: '0001', date: '2020-12-20 12:00:00', amount: '1000'),
  ]; // bill list
  double total = 15000;
  bool loading = false; // true if loading
  final oCcy = new NumberFormat("#,##0.00", "en_US");

  @override
  void initState() {
    // TODO: implement initState
    super.initState();
    // do the fetching
  }

  @override
  Widget build(BuildContext context) {
    return loading
        ? Loading()
        : Scaffold(
            appBar: AppBar(
              title: Text("Today Bills"),
              backgroundColor: Colors.blue,
            ),
            body: Column(
              children: [
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
                    color: Colors.blue[900],
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
