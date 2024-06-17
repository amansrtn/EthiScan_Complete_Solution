// ignore_for_file: unused_local_variable, non_constant_identifier_names

import 'package:ethiscan/NativeCalls/NativeCalls.dart';

speakdarkpattern(Map<String, List<String>> map) async {
  int numberOfKeys = map.length * 10;
  String key = 'No Dark Pattern Found';
  List<String> values = [];
  for (var entry in map.entries) {
    key = entry.key;
    values = entry.value;
    if (numberOfKeys == 0) {
      String text = "No Dark Pattern Found!";
      await speak(text);
      await Future.delayed(const Duration(milliseconds: 2000));
      break;
    } else {
      String text =
          "The text $key is a dark pattern of type ${values.isNotEmpty ? values[0] : ''}, having Severity of ${values.length > 1 ? values[1] : ''}, and it's being detected since ${values.length > 2 ? values[2] : ''}";
      await speak(text);
      await Future.delayed(const Duration(seconds: 10));
    }
  }
  if (numberOfKeys == 0) {
    String text = "No Dark Pattern Found!";
    await speak(text);
    await Future.delayed(const Duration(milliseconds: 2000));
  }
}

speakforall(String text) async {
  await speak(text);
  await Future.delayed(const Duration(milliseconds: 2000));
}

speakforsome(String text) async {
  await speak(text);
  await Future.delayed(const Duration(milliseconds: 2000));
}

bool EnableAssistant = false;
