// ignore_for_file: unused_element, avoid_print, unused_local_variable, non_constant_identifier_names, file_names, unused_import

import 'dart:io';
import 'package:flutter/services.dart';
import 'package:path_provider/path_provider.dart';

const platform = MethodChannel('flutter.native/helper');
Future<void> ShowOverlay() async {
  try {
    // Trigger the "changeColor" method on the native side
    var result = await platform.invokeMethod('changeColor');
  } on PlatformException catch (e) {
    // Handle exceptions if any
    print('Error: ${e.message}');
  }
}

Future<void> StopOverlay() async {
  try {
    // Trigger the "changeColor" method on the native side
    final List<String> result = await platform.invokeMethod('StopOverlay');
  } on PlatformException catch (e) {
    // Handle exceptions if any
    print('Error: ${e.message}');
  }
}

int Coins = 0;

loadCoins() async {
  try {
    final dynamic result = await platform.invokeMethod('getCount');
    final int currentCount = result as int;
    Coins = currentCount;
  } on PlatformException catch (e) {
    print('Error loading coins: ${e.message}');
  }
}

incrementCoins() async {
  try {
    final dynamic result = await platform.invokeMethod('incrementCount');
    final int newCount = result as int;
    Coins = newCount;
  } on PlatformException catch (e) {
    print('Error incrementing coins: ${e.message}');
  }
}

int ShowIntro = 0;

loadintro() async {
  try {
    final dynamic result = await platform.invokeMethod("GetIntro");
    final int currentCount = result as int;
    ShowIntro = currentCount;
  } on PlatformException catch (e) {
    print('Error loading coins: ${e.message}');
  }
  print(ShowIntro);
}

increintro() async {
  try {
    final dynamic result = await platform.invokeMethod("RemoveIntro");
    final int newCount = result as int;
    ShowIntro = newCount;
  } on PlatformException catch (e) {
    print('Error incrementing coins: ${e.message}');
  }
  print(ShowIntro);
}

Future<void> speak(String text) async {
    try {
      await platform.invokeMethod('speak', {"text": text});
    } on PlatformException catch (e) {
      print("Failed to invoke method: '${e.message}'.");
    }
  }