import 'package:app/pages/DayBills.dart';
import 'package:app/pages/Home.dart';
import 'package:app/pages/MonthBills.dart';
import 'package:flutter/material.dart';

void main() => runApp(MaterialApp(
      debugShowCheckedModeBanner: false,
      routes: {
        '/': (context) => Home(),
        '/dayBills': (context) => DayBills(),
        '/monthBills': (context) => MonthBills(),
      },
    ));
