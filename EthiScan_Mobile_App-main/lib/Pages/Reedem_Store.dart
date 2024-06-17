// ignore_for_file: file_names
import 'package:ethiscan/Data/Initial_HomePage_Data.dart';
import 'package:flutter/material.dart';

class StatiticsDarkPattern extends StatelessWidget {
  const StatiticsDarkPattern({super.key});

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        const SizedBox(
          height: 24,
        ),
        const Text("Reedem Store",
            style: TextStyle(
              fontSize: 24,
              fontWeight: FontWeight.bold,
              fontStyle: FontStyle.italic,
              color: Colors.black,
            )),
        const SizedBox(
          height: 24,
        ),
        Expanded(
          child: ListView.builder(
              itemCount: 6,
              itemBuilder: (BuildContext context, int index) {
                return Padding(
                  padding: const EdgeInsets.symmetric(
                      vertical: 12.0, horizontal: 20),
                  child: Column(
                    children: [
                      Container(
                        width: MediaQuery.of(context).size.width * 8,
                        height: MediaQuery.of(context).size.height * 0.2,
                        decoration: const BoxDecoration(
                          color: Color.fromARGB(255, 165, 157, 160),
                          borderRadius: BorderRadius.all(
                            Radius.circular(36),
                          ),
                        ),
                        child: ClipRRect(
                          borderRadius: BorderRadius.circular(36),
                          child: Image.asset(
                            Voucher_Image[index],
                            fit: BoxFit.fill,
                          ),
                        ),
                      ),
                      ElevatedButton(
                        style: ElevatedButton.styleFrom(
                            backgroundColor: Colors.black),
                        onPressed: () {},
                        child: Text(
                          "Get Voucher For ${Voucher_Price[index]}",
                          style: const TextStyle(
                              fontWeight: FontWeight.w800, color: Colors.white),
                        ),
                      ),
                    ],
                  ),
                );
              }),
        )
      ],
    );
  }
}
