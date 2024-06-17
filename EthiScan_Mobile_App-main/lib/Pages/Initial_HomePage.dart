// ignore_for_file: file_names, non_constant_identifier_names, must_be_immutable, avoid_print, unused_element, unused_local_variable

import 'dart:async';
import 'dart:convert';
import 'dart:typed_data';
import 'package:ethiscan/Data/API_DATA.dart';
import 'package:ethiscan/TTS/text_speaker.dart';
import 'package:ethiscan/Widget/Initial_HomePage_widget.dart';
import 'package:http/http.dart' as http;
import 'package:ethiscan/Data/Initial_HomePage_Data.dart';
import 'package:ethiscan/NativeCalls/NativeCalls.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

class InitialHomepage extends StatefulWidget {
  const InitialHomepage({super.key, required this.UpdateUI});
  final Function() UpdateUI;

  @override
  State<InitialHomepage> createState() => _InitialHomepageState();
}

class _InitialHomepageState extends State<InitialHomepage> {
  @override
  void initState() {
    super.initState();
    startColorChangeTimer();
    _setupMethodChannel();
  }

  void startColorChangeTimer() {
    const duration = Duration(seconds: 2);
    Timer.periodic(duration, (Timer timer) {
      if (mounted) {
        setState(() {
          isGreen = !isGreen;
        });
      }
    });
  }

  void _setupMethodChannel() {
    platform.setMethodCallHandler((call) async {
      if (call.method == 'onScreenshotReceived') {
        List<int> byteArray = call.arguments.cast<int>();
        Uint8List receivedImageData = Uint8List.fromList(byteArray);
        setState(() {
          imageData = receivedImageData;
        });
        print('Received image data from Kotlin');
        sendImageToAPI(imageData);
      }
    });
  }

  void sendImageToAPI(Uint8List imageData) async {
    try {
      if (EnableAssistant) {
        await speakforsome("I Will Tell Your Results. Please Wait.");
      }
      String base64Image = base64Encode(imageData);
      const apiUrl = 'https://f677-49-39-40-53.ngrok-free.app/pureimganalyzer/';

      setState(() {
        InitialHomepageWidget = const CircularProgressIndicator(
          color: Colors.black,
        );
      });
      final response = await http.post(
        Uri.parse(apiUrl),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'base64_image': base64Image}),
      );

      if (response.statusCode == 200) {
        Map<String, dynamic> responseBody = jsonDecode(response.body);
        resultList.clear();

        resultList.add(responseBody["result_dark_pattern_type"]);
        print(resultList);
        // test
        Map<String, List<String>> darkPatternMap = {};
        responseBody["result_dark_pattern_type"].forEach((key, value) {
          darkPatternMap[key] = List<String>.from(value);
        });

        // Speak About Dark Pattern
        if (EnableAssistant) {
          await speakforsome("Here Are Your Results.");
          await speakforsome("Dark Pattern Type.");
          await speakdarkpattern(darkPatternMap);
        }
        // Done

        resultList.add(responseBody["result_hidden_cost_flag"]);
        // Speak Hidden Cost
        if (EnableAssistant &&
            responseBody["result_hidden_cost_flag"].toString().toUpperCase() ==
                "FOUND") {
          await speakforsome("Hidden Cost.");
          await speakforall(responseBody["result_hidden_cost_flag"]);
        }
        // Done

        resultList.add(responseBody["result_hidden_cost_type"]);
        // Speak Hidden Cost Type
        if (EnableAssistant &&
            responseBody["result_hidden_cost_flag"].toString().toUpperCase() ==
                "FOUND") {
          await speakforsome("Hidden Cost Type.");
          await speakforall(responseBody["result_hidden_cost_type"]);
        }
        // Done

        resultList.add(responseBody["Disguised_flag"]);

        // Speak disguised ui
        if (EnableAssistant &&
            responseBody["Disguised_flag"].toString().toUpperCase() ==
                "FOUND") {
          await speakforsome("Disguised UI.");
          await speakforall(responseBody["Disguised_flag"]);
        }
        // Done

        resultList.add(responseBody["Disguised_max_word"]);
        // Speak Hidden Cost
        if (EnableAssistant &&
            responseBody["Disguised_flag"].toString().toUpperCase() ==
                "FOUND") {
          await speakforsome("Disguised Word");
          await speakforall(responseBody["Disguised_max_word"]);
        }
        // Done

        resultList.add(responseBody["Disguised_max_count"]);

        resultList.add(responseBody["Fake_Review"]);
        // Speak  Fake Review
        if (EnableAssistant &&
            responseBody["Fake_Review"].toString().toUpperCase() == "FOUND") {
          await speakforsome("Fake Reviews.");
          await speakforall(responseBody["Fake_Review"]);
        }
        // Done

        resultList.add(responseBody["App_Name"]);

        resultList.add(responseBody["Unique"]);
        // new finding
        if (EnableAssistant) {
          await speakforsome("New Finding.");
          await speakforall(responseBody["Unique"].toString());
        }
        // Done

        if (responseBody["Unique"] == true) {
          incrementCoins();
        }
        setState(() {
          MainText = "Your Result";
          InitialHomepageWidget = const InitialList();
          InitialHomePageText;
        });
      } else {
        if (EnableAssistant) {
          await speakforsome("Some Error Occured.");
        }

        print('Error: ${response.statusCode}, ${response.body}');
        setState(() {
          MainText = "Server Error";
          InitialHomePageText;
          InitialHomepageWidget = const InitialList_Temp();
        });
      }
    } catch (error) {
      if (EnableAssistant) {
        await speakforsome("Some Error Occured.");
      }

      print('Error: $error');
      setState(() {
        MainText = "Internet Error";
        InitialHomePageText;
        InitialHomepageWidget = const InitialList_Temp();
      });
    }
    widget.UpdateUI();
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisSize: MainAxisSize.min,
      mainAxisAlignment: MainAxisAlignment.end,
      children: [
        const SizedBox(
          height: 20,
        ),
        Padding(
          padding: EdgeInsets.symmetric(
              horizontal: MediaQuery.of(context).size.width / 16),
          child: InkWell(
            onTap: () {
              print(ProtectionMode);
              if (ProtectionMode == 0) {
                setState(() {
                  ProtectionMode = 1;
                  widget.UpdateUI();
                  ShowOverlay();
                });
              } else if (ProtectionMode == 1) {
                setState(() {
                  ProtectionMode = 2;
                  widget.UpdateUI();
                  StopOverlay();
                });
              } else {
                setState(() {
                  ProtectionMode = 1;
                  widget.UpdateUI();
                  ShowOverlay();
                });
              }
            },
            child: AnimatedContainer(
              duration: const Duration(milliseconds: 1000),
              padding: EdgeInsets.only(
                left: MediaQuery.of(context).size.width / 12,
              ),
              height: MediaQuery.of(context).size.height / 6,
              decoration: BoxDecoration(
                color: ProtectionMode == 0
                    ? isGreen
                        ? Colors.green
                        : Colors.red
                    : ProtectionMode == 1
                        ? Colors.green
                        : Colors.red,
                borderRadius: const BorderRadius.all(
                  Radius.circular(30),
                ),
              ),
              child: const Row(
                children: [
                  Text(
                    "Protector Mode",
                    style: TextStyle(
                        color: Colors.white,
                        fontSize: 24,
                        fontStyle: FontStyle.italic,
                        fontWeight: FontWeight.w500),
                  ),
                  Icon(
                    CupertinoIcons.shield_lefthalf_fill,
                    size: 128,
                    color: Colors.white,
                  )
                ],
              ),
            ),
          ),
        ),
        SizedBox(
          height: MediaQuery.of(context).size.height / 40,
        ),
        Padding(
          padding: EdgeInsets.symmetric(
              horizontal: MediaQuery.of(context).size.width / 16),
          child: InkWell(
            onTap: () async {
              setState(() {
                EnableAssistant = !EnableAssistant;
              });
              if (EnableAssistant) {
                await speak("Voice Assistance Enabled.");
              } else {
                await speak("Voice Assistance Disabled.");
              }
            },
            child: Card(
              elevation: 6,
              child: Padding(
                padding: const EdgeInsets.all(8.0),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    const Text(
                      "Voice Assistance",
                      style: TextStyle(
                          color: Colors.teal,
                          fontSize: 22,
                          fontStyle: FontStyle.italic,
                          fontWeight: FontWeight.w500),
                    ),
                    Icon(
                      EnableAssistant
                          ? CupertinoIcons.mic_fill
                          : CupertinoIcons.mic_slash_fill,
                      size: 32,
                      color: Colors.teal,
                    )
                  ],
                ),
              ),
            ),
          ),
        ),
        SizedBox(
          height: MediaQuery.of(context).size.height / 28,
        ),
        InitialHomePageText,
        InitialHomepageWidget
      ],
    );
  }
}
