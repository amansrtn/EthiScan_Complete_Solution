// ignore_for_file: file_names

import 'package:ethiscan/ChatSection/User_Message.dart';
import 'package:flutter/material.dart';

class ChatMessage extends StatelessWidget {
  final String text;
  final bool isUserMessage;

  const ChatMessage(
      {super.key, required this.text, required this.isUserMessage});

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.symmetric(vertical: 10.0),
      child: isUserMessage
          ? User_Message(text: text, isUserMessage: isUserMessage)
          : Row(
              mainAxisAlignment: isUserMessage
                  ? MainAxisAlignment.end
                  : MainAxisAlignment.start,
              children: <Widget>[
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
                Container(
                  constraints: BoxConstraints(
                    maxWidth: MediaQuery.of(context).size.width * 0.7,
                  ),
                  decoration: BoxDecoration(
                    color: const Color.fromARGB(209, 0, 0, 0),
                    borderRadius: BorderRadius.circular(24.0),
                  ),
                  padding: const EdgeInsets.all(16.0),
                  child: Text(
                    text,
                    style: const TextStyle(
                        color: Colors.white,
                        fontSize: 18,
                        fontWeight: FontWeight.w500),
                  ),
                ),
              ],
            ),
    );
  }
}
