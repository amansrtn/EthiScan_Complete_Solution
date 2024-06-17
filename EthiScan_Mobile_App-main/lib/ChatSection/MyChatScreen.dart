// ignore_for_file: prefer_final_fields, unused_element, library_private_types_in_public_api, file_names, avoid_unnecessary_containers, unnecessary_string_interpolations
import 'package:ethiscan/ChatSection/ChatMessage.dart';
import 'package:ethiscan/Data/Chat_Bot_Data.dart';
import 'package:flutter/material.dart';


class MyChatScreen extends StatefulWidget {
  const MyChatScreen({super.key});

  @override
  _MyChatScreenState createState() => _MyChatScreenState();
}

class _MyChatScreenState extends State<MyChatScreen> {

  void handleSubmitted(String text) async {
    messageController.clear();
    setState(() {
      messages.insert(
          0,
          ChatMessage(
            text: text,
            isUserMessage: true,
          ));
    });
    setState(() {
      messages.insert(
          0,
          const ChatMessage(
            text: "Thinking...",
            isUserMessage: false,
          ));
    });
    final response = await simulateHttpRequest(text);
    setState(() {
      if (messages.isNotEmpty) {
        messages.removeAt(0);
      }
      messages.insert(
          0,
          ChatMessage(
            text: response,
            isUserMessage: false,
          ));
      CanSend = !CanSend;
    });
 
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        const SizedBox(
          height: 24,
        ),
        const Text(
          "EthiBoT: Our Expert",
          style: TextStyle(
            fontSize: 24,
            fontWeight: FontWeight.bold,
            fontStyle: FontStyle.italic,
            color: Colors.black,
          ),
        ),
        const SizedBox(
          height: 24,
        ),
        Flexible(
          child: ListView.builder(
            reverse: true,
            padding: const EdgeInsets.all(8.0),
            itemCount: messages.length,
            itemBuilder: (_, int index) => messages[index],
          ),
        ),
        Container(
            decoration: BoxDecoration(
              color: Theme.of(context).cardColor,
            ),
            child: IconTheme(
              data: IconThemeData(color: Theme.of(context).cardColor),
              child: Container(
                child: Row(
                  children: <Widget>[
                    Flexible(
                      child: Padding(
                        padding: EdgeInsets.symmetric(
                            horizontal: MediaQuery.of(context).size.width / 12,
                            vertical: MediaQuery.of(context).size.height / 24),
                        child: TextFormField(
                          controller: messageController,
                          cursorColor: Colors.black,
                          decoration: InputDecoration(
                            hintText: "What Is Dark Pattern?",
                            contentPadding: const EdgeInsets.symmetric(
                                horizontal: 24, vertical: 12),
                            focusedBorder: OutlineInputBorder(
                              borderSide: const BorderSide(),
                              borderRadius: BorderRadius.circular(24.0),
                            ),
                            suffixIcon: IconButton(
                              onPressed: CanSend
                                  ? () {
                                      setState(() {
                                        CanSend = !CanSend;
                                      });
                                      handleSubmitted(messageController.text);
                                    }
                                  : () {},
                              icon: Icon(
                                Icons.send_rounded,
                                color: CanSend ? Colors.blue : Colors.red,
                              ),
                            ),
                            enabledBorder: OutlineInputBorder(
                              borderSide: const BorderSide(),
                              borderRadius: BorderRadius.circular(24.0),
                            ),
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            )),
      ],
    );
  }
}
