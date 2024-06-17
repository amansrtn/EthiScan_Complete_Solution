// ignore_for_file: file_names, non_constant_identifier_names, body_might_complete_normally_nullable, avoid_types_as_parameter_names
import 'package:ethiscan/Data/AbourDarkPatternData.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

class AboutDarkPattern extends StatefulWidget {
  const AboutDarkPattern({super.key});

  @override
  State<AboutDarkPattern> createState() => _AboutDarkPatternState();
}

class _AboutDarkPatternState extends State<AboutDarkPattern> {
  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      itemCount: 13,
      itemBuilder: (BuildContext context, int index) {
        return Card(
          margin: const EdgeInsets.all(8),
          color: Colors.amber,
          elevation: 12,
          shadowColor: Colors.green,
          shape: const ContinuousRectangleBorder(
            borderRadius: BorderRadius.all(Radius.circular(24)),
          ),
          child: Padding(
            padding: const EdgeInsets.all(8.0),
            child: ExpansionTile(
              tilePadding: const EdgeInsets.all(8),
              title: DarkPatternTitle[index],
              leading: Image(
                height: MediaQuery.of(context).size.width,
                image: AssetImage(
                  "assets/DarkpatternIcon/${DarkPatternImage[index]}",
                ),
              ),
              trailing: IsExpandedInfo[index]
                  ? const Icon(
                      CupertinoIcons.minus_circle_fill,
                      size: 28,
                      color: Color.fromARGB(255, 14, 90, 152),
                    )
                  : const Icon(
                      CupertinoIcons.add_circled_solid,
                      size: 28,
                      color: Color.fromARGB(255, 14, 90, 152),
                    ),
              children: [
                Padding(
                  padding: const EdgeInsets.all(8.0),
                  child: Text(
                    DarkPatternDescription[index],
                    style: const TextStyle(fontWeight: FontWeight.w500),
                    textAlign: TextAlign.justify,
                  ),
                ),
              ],
              onExpansionChanged: (value) {
                setState(() {
                  IsExpandedInfo[index] = !IsExpandedInfo[index];
                });
              },
            ),
          ),
        );
      },
    );
  }
}
