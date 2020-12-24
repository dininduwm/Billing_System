import 'package:app/data_types/Bill.dart';
import 'package:http/http.dart';
import 'dart:convert';

import 'package:intl/intl.dart';

class GetMonthBills {
  static List<Bill> bills = [
    Bill(date: '2020-12-10', amount: '1500', billNo: '0001')
  ];

  static double total;

  static Future<bool> getMonthBills(date) async {
    try {
      Response response = await get(
          'https://aldermanly-dwell.000webhostapp.com/api/getMonthBill.php?date=' +
              DateFormat('yyyy-MM').format(date));

      Map data = jsonDecode(response.body);
      print(data);

      // cleat the bills
      bills = [];

      // counting the total
      total = 0;

      data['details'].forEach((bill) {
        bills.add(Bill(
          billNo: bill['bill_no'],
          date: bill['date'],
          amount: bill['amount'],
        ));
        total += double.parse(bill['amount']);
      });

      return (true);
    } catch (e) {
      print('Error in data loading');
      return (false);
    }
  }
}
