

// ignore_for_file: avoid_print

import "package:animated_splash_screen/animated_splash_screen.dart";
import "package:ethiscan/IntroductionPage/OnBoadring.dart";
import "package:ethiscan/NativeCalls/NativeCalls.dart";
import "package:ethiscan/Widget/MainEntryPage.dart";
import "package:flutter/material.dart";
import "package:flutter/services.dart";

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  SystemChrome.setSystemUIOverlayStyle(const SystemUiOverlayStyle(
    statusBarColor: Colors.white,
    systemNavigationBarColor: Colors.white,
  ));
  loadintro();
  runApp(const MyApp());
}

class MyApp extends StatefulWidget {
  const MyApp({super.key});

  @override
  State<MyApp> createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  @override
  initState() {
    super.initState();
    loadCoins();
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: "EthiScan",
      home: AnimatedSplashScreen(
        splashIconSize: MediaQuery.of(context).size.width,
        duration: 3000,
        splash: 'assets/App_Splash.png',
        nextScreen: whichScreen(),
        splashTransition: SplashTransition.fadeTransition,
        backgroundColor: Colors.black,
      ),
    );
  }
}

Widget whichScreen() {
  if (ShowIntro != 0) {
    return const MainEntryPage();
  } else {
    return const OnBoardingPage();
  }
}
