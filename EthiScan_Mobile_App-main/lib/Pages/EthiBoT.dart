// ignore_for_file: file_names, prefer_typing_uninitialized_variables, unused_field, unused_element, no_leading_underscores_for_local_identifiers, avoid_print, unused_local_variable, use_build_context_synchronously, unnecessary_null_comparison, non_constant_identifier_names, prefer_final_fields

import 'package:ethiscan/ChatSection/MyChatScreen.dart';
import 'package:flutter/material.dart';

class EthiBoT extends StatefulWidget {
  const EthiBoT({super.key});

  @override
  State<EthiBoT> createState() => _EthiBoTState();
}

class _EthiBoTState extends State<EthiBoT> {
  TextEditingController _textEditingController = TextEditingController();
  @override
  Widget build(BuildContext context) {
    return const MyChatScreen();
  }
}
