from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from core.models import Website
@csrf_exempt
def default(request):
    text = request.POST.get("text")
    webName = request.POST.get("name")
    if(text == None):
        result = {"status": "error", "flag": "false", "keyword": "No text param in header of request"}
    else:
        result = analyze(text)
        result["status"] = "clear"
    addFlagToDB(baseURL= webName+"."+"android_dev", webName= webName, category="Hidden Cost")
    return JsonResponse(result, status=200)


def addFlagToDB(baseURL, webName, category):
    category_lis = [category]
    Website.create_or_update_website(baseURL= baseURL, webName= webName, category_names= category_lis)


def analyze(text):
    processed_text = preprocess(text)
    flag_res = flag_hidden_cost(processed_text)
    return flag_res

# Function to extract the substring we care about.
def preprocess(input_string):
    starting_keywords = ["Price Details", "Order Summary", "Bill details", "Payment Details", 
                         "Price Summary", "Bill Summary", "Order Details", "Bill Amount", 
                         "Amount Details", "Amount Summary"]

    ending_keywords = ["Grand Total", "Total Amount", "Total Payable", "Net Payable", 
                       "Net Amount", "Subtotal", "Total", "Grand total"]

    start_index = -1
    end_index = len(input_string)

    # Find the starting keyword
    for keyword in starting_keywords:
        if keyword in input_string:
            start_index = max(start_index, input_string.find(keyword))

    # Find the ending keyword
    for keyword in ending_keywords:
        if keyword in input_string:
            end_index = min(end_index, input_string.rfind(keyword))

    # Return the substring based on starting and ending indices
    if start_index != -1 and end_index > start_index:
        return input_string[start_index:end_index + len(keyword)].strip()
    else:
        return ""
    
def flag_hidden_cost(input_string):
    hidden_cost_keywords = [
        "Hidden Fees", "Unforeseen Expenses", "Additional Charges", "Platform Markup",
        "Transaction Fees", "Surprise Costs", "Scalability Charges", "Data Storage Costs",
        "Maintenance Fees", "Integration Costs", "Microtransactions", "Nickel-and-Diming",
        "Bait-and-Switch Pricing", "Handling Charges", "Care Charges", "Care and Handling Charges", 
        "Handling Charge", "Care Charges", "Care and Handling Charge", 
        "Concealed Expenses", "Invisible Charges", "Fine Print Fees", "Operational Costs",
        "Hidden Upgrades", "Incidental Charges", "Subscription Surprises", "Obscure Fees",
        "Unexpected Overheads", "Add-on Expenses", "Implicit Costs", "Backend Charges",
        "Unnoticed Fees", "Inconspicuous Tariffs", "Sneaky Pricing", "Behind-the-Scenes Costs",
        "Unseen Dues", "Non-disclosed Levies", "Cryptic Expenses", "Under-the-Radar Fees",
        "Secret Charges", "Silent Costs", "Hidden Tariffs", "Stealthy Fees", "Camouflaged Expenses",
        "Veiled Charges", "Covert Expenses", "Hushed Fees", "Subtle Tariffs", "Inherent Costs",
        "Quiet Charges", "Unspoken Fees", "Backdoor Expenses", "Behind-the-Scenes Fees",
        "Latent Charges", "Unexpressed Costs", "Undercover Fees", "Subterranean Costs",
        "Veiled Tariffs", "Unannounced Dues", "Masked Expenses", "Cloaked Charges",
        "Under-the-Surface Costs", "Unrevealed Fees", "Hidden Assessments",
        "Behind-Closed-Doors Costs", "Unpublicized Charges", "Surreptitious Fees",
        "Under-the-Table Costs", "Unacknowledged Dues"
    ] #update more keywords if needed

    # Convert the input string and keywords to lowercase for case-insensitive comparison
    input_string_lower = input_string.lower()
    hidden_cost_keywords_lower = [keyword.lower() for keyword in hidden_cost_keywords]

    # Check if any hidden cost keyword is present in the input string
    hidden_cost_present = any(keyword in input_string_lower for keyword in hidden_cost_keywords_lower)

    # If a hidden cost keyword is present, find and return the first one in its original case
    if hidden_cost_present:
        for keyword, keyword_lower in zip(hidden_cost_keywords, hidden_cost_keywords_lower):
            if keyword_lower in input_string_lower:
                return {'flag': "true", "keyword": keyword}

    # If no hidden cost keyword is present, return False
    return {"flag": "false", "keyword": "null"}

class NoTextInHeaderException(Exception):
    def __init__(self, message="No text param found in header of request") -> None:
        super().__init__(message)
