// ignore_for_file: file_names, sized_box_for_whitespace, avoid_print, non_constant_identifier_names

import 'package:ethiscan/Data/Initial_HomePage_Data.dart';
import 'package:ethiscan/NativeCalls/NativeCalls.dart';
import 'package:ethiscan/Pages/About_Dark_Pattern.dart';
import 'package:ethiscan/Pages/Initial_HomePage.dart';
import 'package:ethiscan/Pages/EthiBoT.dart';
import 'package:ethiscan/Pages/Reedem_Store.dart';
import 'package:fluid_bottom_nav_bar/fluid_bottom_nav_bar.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

class MainEntryPage extends StatefulWidget {
  const MainEntryPage({
    super.key,
  });

  @override
  State<MainEntryPage> createState() => _MainEntryPageState();
}

class _MainEntryPageState extends State<MainEntryPage> {
  @override
  void initState() {
    super.initState();
    child = InitialHomepage(
      UpdateUI: UpdateUI,
    );
  }

  UpdateUI() {
    setState(() {});
  }

  void _handleNavigationChange(int index) {
    setState(() {
      switch (index) {
        case 0:
          child = InitialHomepage(
            UpdateUI: UpdateUI,
          );
          break;
        case 1:
          child = const AboutDarkPattern();
          break;
        case 2:
          child = const EthiBoT();
          break;
        case 3:
          child = const StatiticsDarkPattern();
          break;
      }
    });
    child = AnimatedSwitcher(
      switchInCurve: Curves.easeOut,
      switchOutCurve: Curves.easeIn,
      duration: const Duration(milliseconds: 500),
      child: child,
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        leading: const Icon(
          CupertinoIcons.text_justifyleft,
          size: 30,
          weight: 100,
          grade: 100,
          color: Colors.black,
          shadows: [Shadow(color: Colors.black26)],
        ),
        leadingWidth: MediaQuery.of(context).size.width / 4,
        actions: [
          Padding(
            padding:
                EdgeInsets.only(right: MediaQuery.of(context).size.width / 26),
            child: ElevatedButton(
              onPressed: () {},
              child: Text(
                "Your Coins: $Coins",
                style: const TextStyle(
                    color: Colors.black,
                    fontStyle: FontStyle.italic,
                    fontWeight: FontWeight.w500),
              ),
            ),
          ),
          Padding(
            padding:
                EdgeInsets.only(right: MediaQuery.of(context).size.width / 18),
            child: Icon(
              CupertinoIcons.asterisk_circle_fill,
              color: ProtectionMode == 1 ? Colors.green : Colors.red,
              size: 36,
            ),
          ),
        ],
        backgroundColor: Colors.white,
      ),
      body: child,
      bottomNavigationBar: FluidNavBar(
        icons: [
          FluidNavBarIcon(
              icon: CupertinoIcons.home,
              backgroundColor: const Color(0xFF4285F4),
              extras: {"label": "home"}),
          FluidNavBarIcon(
              icon: CupertinoIcons.book_solid,
              backgroundColor: const Color(0xFFEC4134),
              extras: {"label": "About"}),
          FluidNavBarIcon(
              icon: CupertinoIcons.chat_bubble_text_fill,
              backgroundColor: const Color(0xFFFCBA02),
              extras: {"label": "History"}),
          FluidNavBarIcon(
              icon: CupertinoIcons.money_dollar,
              backgroundColor: const Color(0xFF34A950),
              extras: {"label": "Setting"}),
        ],
        onChange: _handleNavigationChange,
        style: const FluidNavBarStyle(
          iconSelectedForegroundColor: Colors.black,
          iconUnselectedForegroundColor: Colors.white,
          barBackgroundColor: Color.fromARGB(255, 14, 52, 117),
        ),
        scaleFactor: 1.5,
        defaultIndex: 0,
        itemBuilder: (icon, item) => Semantics(
          label: icon.extras!["label"],
          child: item,
        ),
      ),
    );
  }
}
