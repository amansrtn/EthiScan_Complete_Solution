// ignore_for_file: file_names, non_constant_identifier_names
import 'package:flutter/material.dart';

List<String> DarkPatternImage = [
  "flase-urgency-high-resolution-logo-black.png",
  "basket-sneaking-high-resolution-logo-black.png",
  "confirm-shaming-high-resolution-logo-black.png",
  "forced-action-high-resolution-logo-black.png",
  "subscription-trap-high-resolution-logo-black.png",
  "interface-interference-high-resolution-logo-black.png",
  "bait-and-switch-high-resolution-logo-black.png",
  "drip-pricing-high-resolution-logo-black.png",
  "disguised-advertisement-high-resolution-logo-black.png",
  "nagging-high-resolution-logo-black.png",
  "trick-question-high-resolution-logo-black.png",
  "saas-billing-high-resolution-logo-black.png",
  "rogue-malwares-high-resolution-logo-black.png"
];

List<Widget> DarkPatternTitle = [
  Text("False Urgency", style: textstyle),
  Text("Basket Sneaking", style: textstyle),
  Text("Confirm Shaming", style: textstyle),
  Text("Forced Action", style: textstyle),
  Text("Subscription Trap", style: textstyle),
  Text("Interface Interference", style: textstyle),
  Text("Bait and Switch", style: textstyle),
  Text("Drip Pricing", style: textstyle),
  Text("Disguised Advertisement", style: textstyle),
  Text("Nagging", style: textstyle),
  Text("Trick Question", style: textstyle),
  Text("Saas Billing", style: textstyle),
  Text("Rogue Malwares", style: textstyle)
];

TextStyle textstyle = const TextStyle(
  fontSize: 18,
  fontWeight: FontWeight.bold,
  fontStyle: FontStyle.italic,
  color: Colors.black,
);

List<bool> IsExpandedInfo = [
  false,
  false,
  false,
  false,
  false,
  false,
  false,
  false,
  false,
  false,
  false,
  false,
  false,
];

List<String> DarkPatternDescription = [
  """
“False Urgency” refers to the deceptive practice of falsely conveying or implying a sense of urgency or scarcity to mislead users into making immediate purchases or taking prompt actions, potentially resulting in a purchase. 

This includes falsely showcasing the popularity of a product or service to manipulate user decisions and misrepresenting that quantities of a particular product or service are more limited than they actually are.

Illustrations of such dark patterns include presenting false data on high demand without appropriate context (e.g., “Only 2 rooms left! 30 others are looking at this right now”) and falsely creating time-bound pressure for a purchase, such as labelling a sale as an ‘exclusive’ sale for a limited time only for a select group of users.
""",
  """
Basket Sneaking has been defined as the practice of including additional items, such as products, services, payments to charity, or donations, during the checkout process on a platform without the explicit consent of the user. This results in the total amount payable by the user exceeding the amount intended for the chosen product or service.

It’s important to note that the addition of free samples, complimentary services, or necessary fees disclosed at the time of purchase is not considered basket sneaking. “Necessary fees” refer to fees essential for completing the order, such as delivery charges, gift wrapping, additional government taxes on the product, or any other explicitly disclosed charges to the consumer during the purchase.

Examples of basket sneaking include the automatic addition of paid ancillary services with a pre-ticked box during the purchase of a product or service, the automatic addition of a subscription to a salon service when a user buys a single service, and the automatic inclusion of travel insurance when a user purchases a flight ticket.
""",
  """
Confirm Shaming is the practice of employing phrases, videos, audio, or any other means to instil a sense of fear, shame, ridicule, or guilt in the user’s mind. The objective is to subtly push the user into a specific action, such as purchasing a product or service from the platform or continuing a subscription, with the primary intent of achieving commercial gains by manipulating consumer choices.

This dark pattern includes a flight ticket booking platform using the phrase “I will stay unsecured” when a user opts not to include insurance in their cart and a platform adding a charity to the basket without the user’s consent while using a phrase like “charity is for the rich, I don’t care” when a user chooses to opt out of contributing toward charity.
""",
  """
Forced Action refers to the practice of compelling a user to take an action that necessitates purchasing additional goods, subscribing to unrelated services, signing up for other services, or sharing personal information. This is done in connection with the user’s original intent to buy or subscribe to a particular product or service.
""",
  """
A “Subscription Trap” involves tactics such as making the cancellation of a paid subscription overly complex or impossible, hiding the cancellation option, compelling users to provide payment details for auto-debits even for ostensibly free subscriptions, and employing ambiguous or confusing instructions regarding the cancellation process. These practices hinder users from easily opting out of subscriptions, potentially leading to unintended and continued financial commitments.
""",
  """
Interface Interference refers to a design element that manipulates the user interface by emphasising specific information while obscuring other relevant information relative to that data, with an intention to mislead the user and steer them away from the desired action. 

Examples of interface interference include employing a light-colored option for selecting “No” in response to a purchase pop-up or deliberately concealing the cancellation symbol in tiny font. Another example is using a ‘X’ icon on the top-right corner of a pop-up screen that, instead of closing it, opens another advertisement. 
""",
  """
Bait and switch is a deceptive practice that involves advertising a specific outcome based on the user’s action and then providing an alternative outcome that differs from what was initially presented.

Examples of this deceptive tactic include a seller advertising a high-quality product at a low price, but when the consumer is ready to make a purchase, claiming the product is unavailable and offering a similar-looking but more expensive item. Another instance is falsely displaying a product as available to entice the consumer to add it to their shopping cart, only to later reveal that the product is actually unavailable. 
""",
  """
Drip pricing is a practice characterised by several deceptive tactics, including not disclosing elements of prices upfront or revealing them subtly within the user experience, or disclosing the price only after the confirmation of purchase, leading to a charge higher than initially indicated at the checkout.

It also includes advertising a product or service as free without adequately disclosing that continued use requires in-app purchases and preventing a user from accessing a service already paid for unless an additional purchase is made. 
""",
  """
Disguised advertisement refers to the practice of presenting advertisements in a manner that conceals their true nature, making them appear as other types of content, such as user-generated content, news articles, or false advertisements. The intention is to seamlessly integrate these ads into the overall interface, tricking customers into clicking on them. 

It is to be noted that for the purposes of this definition, “disguised advertisement” includes misleading advertisements as defined in clause 2(28) of the Act, and the “Guidelines for Prevention of Misleading Advertisements and Endorsements for Misleading Advertisements, 2022” are applicable. Additionally, when sellers or advertisers post content on a platform, they bear the responsibility of disclosing that such content is, indeed, an advertisement.
""",
  """
Nagging is a dark pattern practice characterised by the repeated and persistent disruption and annoyance of a user through continuous interactions, requests, information, options, or interruptions to facilitate a transaction and achieve commercial gains unless explicitly permitted by the user. 

Nagging includes websites repeatedly prompting a user to download their app, platforms persistently requesting users to provide personal details under the guise of security purposes, and constant requests to enable notifications or accept cookies with no option to decline. This practice exploits persistent and intrusive tactics to influence user behaviour for commercial purposes.
""",
  """
Trick Question refers to the intentional use of confusing or vague language, such as confusing wording, double negatives, or other similar tricks, with an aim to mislead or divert a user from taking the desired action or prompting a specific response or action.

Trick Question includes providing a choice to opt-out with a question like, “Do you wish to opt out of receiving updates on our collection and discounts forever?” where the phrases “Yes. I would like to receive updates” and “Not Now” are used instead of a straightforward option like “Yes,” introducing confusion and potentially leading users to make unintended choices.
""",
  """
Saas billing refers to the process of generating and collecting payments from consumers on a recurring basis in a software-as-a-service (SaaS) business model, often exploiting positive acquisition loops in recurring subscriptions to discreetly obtain funds from users. 

This practice includes situations where users are not notified when a free trial is converted to a paid subscription, silent recurring transactions where the user’s account is debited without proper notification, auto-renewing monthly subscriptions without clear communication to users, charging customers for features and services they don’t use, and employing questionable credit card authorisation practices to deceive consumers. This method involves obtaining payments in a way that is less transparent and may not be readily apparent to the users involved.
""",
  """
Rogue Malwares involve the use of ransomware or scareware to deceive users by making them believe their computer is infected with a virus. The ultimate goal is to persuade them to pay for a fake malware removal tool, which, in reality, installs additional malware on their computer.

This practice includes pirating websites or apps that promise free content but lead to embedded malware upon accessing the links. Another scenario involves users gaining access to content on pirated platforms but encountering pop-ups with advertisements embedded with malware. Additionally, users may be prompted to click on an advertisement or automatically redirected to one, only to find their personal files locked, followed by a demand for payment to regain access.
""",
];

whatcolor(text) {
  if (text.toString().toUpperCase() == "CONFIRMED") {
    return Colors.redAccent;
  } else if (text.toString().toUpperCase() == "WARNING") {
    return Colors.amber;
  } else {
    return Colors.black;
  }
}
