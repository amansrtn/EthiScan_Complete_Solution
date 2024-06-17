// ignore_for_file: file_names, non_constant_identifier_names, unused_element, unnecessary_string_interpolations, camel_case_types, avoid_print

import 'dart:convert';

import 'package:ethiscan/ChatSection/ChatMessage.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

TextEditingController messageController = TextEditingController();
List<ChatMessage> messages = [];
bool CanSend = true;

Future<String> simulateHttpRequest(String text) async {
  try {
    const apiUrl =
        'https://f677-49-39-40-53.ngrok-free.app/Ethibot/';
    final response = await http.post(
      Uri.parse(apiUrl),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({"user_message": text}),
    );
    if (response.statusCode == 200) {
      Map<String, dynamic> rB = jsonDecode(response.body);
      return rB["result"];
    } else {
      print('Error: ${response.statusCode}, ${response.body}');
      return "Server Error";
    }
  } catch (error) {
    return "Internet Error";
  }
}
