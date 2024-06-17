// ignore_for_file: file_names, non_constant_identifier_names, avoid_print, unused_local_variable, unused_element
import 'package:dash_bubble/dash_bubble.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

// import 'package:shared_preferences/shared_preferences.dart';

bool isGreen = true;

int ProtectionMode = 0;

Uint8List imageData = Uint8List(0);

Future<void> requestOverlayPermission() async {
  final hasPermission = await DashBubble.instance.hasOverlayPermission();
  if (hasPermission) {
    final isGranted = await DashBubble.instance.requestOverlayPermission();
  }
}



List<String> Voucher_Image = [
  "assets/Voucher/50.png",
  "assets/Voucher/100.png",
  "assets/Voucher/200.png",
  "assets/Voucher/500.png",
  "assets/Voucher/800.png",
  "assets/Voucher/1000.png"
];

List<String> Voucher_Price = [
  "200 Coins",
  "400 Coins",
  "800 Coins",
  "2000 Coins",
  "3200 Coins",
  "4000 Coins",
];


late Widget child;
