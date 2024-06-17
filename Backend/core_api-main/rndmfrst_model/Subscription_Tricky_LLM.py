import os

os.environ["GRADIENT_ACCESS_TOKEN"] = "4qIVNL6ym9D4dBJotzfV1aIdIdhuWBeo"
os.environ["GRADIENT_WORKSPACE_ID"] = "55ae1e95-beff-4fd0-99b0-aa0d23c29729_workspace"

from llama_index.llms import GradientBaseModelLLM


def SubscriptionTricky(text):
    if True:
        # text = text.replace("\n", "").replace("\t", "").replace("  ", "")
        llm = GradientBaseModelLLM(
            base_model_slug="nous-hermes2",
            max_tokens=300,
        )
        result = llm.complete(
            f"I will give you a list of buttons from a e-commerce website your task is to find out that button from the given list which has the highest probablity of getting an option to cancel subscription. in response return me the button name in the form of json, the list of button is {text}. Give Me JSON Response which include that button name. THE BUTTON YOU CHOOSE MUST BE FROM IN THE LIST OF BUTTON WHICH I PROVIDED IT IS MANDATORY. GIVE IMPORTANCE TO THAT BUTTON WHICH INCLUDE TERMS LIKE MEMBERSHIP, SUBSCRIPTION"
        )
        result = str(result)
        print(result)
        result = result.split('''"button_name": ''')[1]
        result = result.replace("\n", "")
        result = result.replace("}", "")
        result = result.replace("/", "")
        print(result)
        return result


# print(SubscriptionTricky("['account', 'membership']"))
# print(AppNameFinder(text = """Vo
# 1:08 PM
# 5
# WiFi
# 11
# 4
# Temu | Shop for Clo.
# temu.com
# TEMU
# Q containers f_
# E
# 8 R
# AII
# Office
# Women
# Home
# Men
# Jewelry
# S
# Free shipping for you
# Exclusive offer
# BIG GAME
# Jeab
# Deal
# 1
# Piece High Suction Cordless
# 18pcs/set Square Clear Storag:
# Best Seller  in Vacuums & Floor Ca:
# Most Repurchased
# in Organization,
# (14,143)
# (1,887)
# S9.48
# 19K+sold
# S4.28 1.7K+sold
# 246PCS
# 2 Rolls in Package
# EthiScan
# PET protectiver
# film
# 0.39in/0.99
# 18in/3.0c
# 0.078in/0.2cm
# BIG GAME
# Jeal
# eab
# 246pcs Drill Bit Set With Stora_
# Double Sided Adhesive Tape H.
# Only 1 Left
# just added to cart
# (68,813)
# (362)
# S67.28 33sold
# S5.93 1K+sold
# Sign in for the best experience
# Sign in"""))