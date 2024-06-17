// ignore_for_file: file_names, camel_case_types
import 'package:flutter/material.dart';

class User_Message extends StatelessWidget {
  const User_Message(
      {super.key, required this.text, required this.isUserMessage});

  final String text;
  final bool isUserMessage;
  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisAlignment:
          isUserMessage ? MainAxisAlignment.end : MainAxisAlignment.start,
      children: <Widget>[
        Container(
          constraints: BoxConstraints(
            maxWidth: MediaQuery.of(context).size.width * 0.7,
          ),
          decoration: BoxDecoration(
            color: const Color.fromARGB(255, 18, 140, 126),
            borderRadius: BorderRadius.circular(24.0),
          ),
          padding: const EdgeInsets.all(16.0),
          child: Text(
            text,
            style: const TextStyle(
              color: Colors.white,
              fontSize: 18,
              fontWeight: FontWeight.w500,
            ),
          ),
        ),
        Container(
          margin: const EdgeInsets.only(right: 8.0, left: 8.0),
          child: CircleAvatar(
            backgroundColor: Colors.black,
            child: isUserMessage
                ? const Icon(
                    Icons.person,
                    color: Colors.white,
                  )
                : Image.asset('assets/Bot_Image.jpg'),
          ),
        ),
      ],
    );
  }
}
