def find_Disguised_UI(paragraph):
    word_list = [
        "Download",
        "Property",
        "Install",
        "Instant",
        "Continue",
        "Click Here",
        "Press",
        "Available",
        "Join",
        "Free",
        "Discount",
        "Latest",
        "Updates",
        "Play",
        "Price",
        "Money",
        "Bonus",
        "Up to",
    ]
    word_count = {}
    for word in word_list:
        count = paragraph.lower().count(word.lower())
        word_count[word] = count

    max_word = max(word_count, key=word_count.get)
    max_count = word_count[max_word]
    Disguised_flag = "Not Found"
    if max_count > 3:
        Disguised_flag = "Found"
        return {
            "Disguised_flag": Disguised_flag,
            "max_word": max_word,
            "max_count": max_count,
        }
    return {
            "Disguised_flag": Disguised_flag,
            "max_word": "Not Found Any",
            "max_count": max_count,
        }
    
