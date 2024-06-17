// ignore_for_file: file_names, non_constant_identifier_names, unnecessary_import, unnecessary_string_interpolations, unused_element, camel_case_types, use_super_parameters, unnecessary_const
import 'dart:ui';
import 'package:ethiscan/Data/API_DATA.dart';
import 'package:ethiscan/Data/AbourDarkPatternData.dart';
import 'package:flutter/material.dart';

Widget InitialHomepageWidget = const InitialList_Temp();
Widget InitialHomePageText = const InitialText();
String MainText = "Dark Pattern Results Will Be Displayed Here.";

class InitialText extends StatelessWidget {
  const InitialText({super.key});

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: MediaQuery.of(context).size.height / 20,
      child: Text(
        MainText,
        style: const TextStyle(
            fontSize: 16,
            fontWeight: FontWeight.w500,
            fontStyle: FontStyle.italic),
      ),
    );
  }
}

class InitialList extends StatelessWidget {
  const InitialList({super.key});

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: ListView.builder(
          itemCount: DarkpatternTypes.length,
          itemBuilder: (BuildContext context, int index) {
            var resultValue = resultList[index];
            return Center(
                child: Card(
              elevation: 3,
              margin: const EdgeInsets.symmetric(vertical: 8, horizontal: 16),
              child: Container(
                width: MediaQuery.of(context).size.width,
                padding: const EdgeInsets.all(16),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text(
                      DarkpatternTypes[index],
                      style: const TextStyle(
                          fontSize: 16,
                          color: Colors.blue,
                          fontWeight: FontWeight.w500),
                    ),
                    // work is to be done here

                    const SizedBox(
                      height: 8,
                    ),
                    if (index == 0)
                      resultValue.toString().isEmpty
                          ? const Text(
                              "Everything Looks Fine",
                              style: const TextStyle(
                                  fontSize: 16,
                                  color: Colors.green,
                                  fontWeight: FontWeight.w500),
                            )
                          : ResultTableWidget(resultValue)
                    else
                      _buildResultText(resultValue)
                  ],
                ),
              ),
            ));
          }),
    );
  }
}

Widget _buildResultText(dynamic resultValue) {
  if (resultValue is bool) {
    return Text(
      resultValue ? 'True'.toUpperCase() : 'Not Unique'.toUpperCase(),
      style: TextStyle(
          fontSize: 16,
          color: resultValue ? Colors.green : Colors.red,
          fontWeight: FontWeight.w500),
    );
  } else if (resultValue is int) {
    return Text(
      '$resultValue'.toUpperCase(),
      style: const TextStyle(
          fontSize: 16, color: Colors.black, fontWeight: FontWeight.w500),
    );
  } else {
    if (resultValue.toString().toUpperCase() == "TRUE") {
      return Text(
        'True'.toUpperCase(),
        style: const TextStyle(
            fontSize: 16, color: Colors.red, fontWeight: FontWeight.w500),
      );
    } else if (resultValue.toString().toUpperCase() == "NOT FOUND") {
      return Text(
        'Not Found'.toUpperCase(),
        style: const TextStyle(
            fontSize: 16, color: Colors.green, fontWeight: FontWeight.w500),
      );
    } else if (resultValue.toString().toUpperCase() == "NULL") {
      return Text(
        'Not Found'.toUpperCase(),
        style: const TextStyle(
            fontSize: 16, color: Colors.green, fontWeight: FontWeight.w500),
      );
    } else if (resultValue.toString().toUpperCase() == "NOT FOUND ANY") {
      return Text(
        'Not Found'.toUpperCase(),
        style: const TextStyle(
            fontSize: 16, color: Colors.green, fontWeight: FontWeight.w500),
      );
    } else {
      return Text(
        '$resultValue'.toUpperCase(),
        style: const TextStyle(
            fontSize: 16, color: Colors.red, fontWeight: FontWeight.w500),
      );
    }
  }
}

class InitialList_Temp extends StatelessWidget {
  const InitialList_Temp({super.key});

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: ListView.builder(
          itemCount: DarkpatternTypes.length,
          itemBuilder: (BuildContext context, int index) {
            return Center(
                child: Card(
              elevation: 3,
              margin: const EdgeInsets.symmetric(vertical: 8, horizontal: 16),
              child: Container(
                padding: const EdgeInsets.all(16),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text(
                      DarkpatternTypes[index],
                      style: const TextStyle(
                          fontSize: 16,
                          color: Colors.blue,
                          fontWeight: FontWeight.w500),
                    ),
                  ],
                ),
              ),
            ));
          }),
    );
  }
}

class ResultTableWidget extends StatelessWidget {
  final Map<String, dynamic> resultValue;

  const ResultTableWidget(this.resultValue, {Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      scrollDirection: Axis.horizontal,
      child: Container(
        decoration: BoxDecoration(
          border: Border.all(color: Colors.black), // Set border color and width
        ),
        child: DataTable(
          border: TableBorder.symmetric(inside: const BorderSide()),
          columns: const <DataColumn>[
            DataColumn(
              label: Text(
                'Text Involved',
                style: const TextStyle(fontSize: 16),
              ),
            ),
            DataColumn(
                label: Text(
              'Type Of Dark Pattern',
              style: const TextStyle(fontSize: 16),
            )),
            DataColumn(
                label: Text(
              'Status Of  Dark Pattern',
              style: const TextStyle(fontSize: 16),
            )),
            DataColumn(
                label: Text(
              'Showing Since',
              style: const TextStyle(fontSize: 16),
            )),
          ],
          rows: resultValue.entries.map((entry) {
            String key = entry.key;
            dynamic value = entry.value;
            List<DataCell> cells = _getCellsForValue(value);
            return DataRow(cells: [
              DataCell(Text(
                key,
              )),
              ...cells, // Add all cells to the DataRow
            ]);
          }).toList(),
        ),
      ),
    );
  }

  List<DataCell> _getCellsForValue(dynamic value) {
    if (value is List) {
      if (value.isEmpty) {
        // If the list is empty, return empty cells for each column
        return List<DataCell>.generate(
          3, // Number of columns except the first one
          (index) => const DataCell(Text('')), // Empty DataCell for each column
        );
      } else {
        return value
            .map(
              (item) => DataCell(
                Text(
                  item.toString().toUpperCase(),
                  style: TextStyle(color: whatcolor(item.toString())),
                ),
              ),
            )
            .toList();
      }
    } else {
      return [
        DataCell(
          Text(
            value.toString(),
          ),
        ),
      ];
    }
  }
}
