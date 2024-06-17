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
        "Under-the-Table Costs", "Unacknowledged Dues","high demand surge charge"
    ] #update more keywords if needed

    # Convert the input string and keywords to lowercase for case-insensitive comparison
    input_string_lower = [inpu.lower() for inpu in input_string]

    print("-----",input_string_lower)

    hidden_cost_keywords_lower = [keyword.lower() for keyword in hidden_cost_keywords]

    # Check if any hidden cost keyword is present in the input string
    hidden_cost_present = any(keyword in input_string_lower for keyword in hidden_cost_keywords_lower)

    # If a hidden cost keyword is present, find and return the first one in its original case
    if hidden_cost_present:
        for keyword, keyword_lower in zip(hidden_cost_keywords, hidden_cost_keywords_lower):
            if keyword_lower in input_string_lower:
                return {'flag': "Found", "keyword": keyword}

    # If no hidden cost keyword is present, return False
    return {"flag": "Not Found", "keyword": "Not Found"}