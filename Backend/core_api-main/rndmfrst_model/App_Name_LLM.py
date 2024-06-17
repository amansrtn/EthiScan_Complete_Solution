import os

os.environ["GRADIENT_ACCESS_TOKEN"] = "4qIVNL6ym9D4dBJotzfV1aIdIdhuWBeo"
os.environ["GRADIENT_WORKSPACE_ID"] = "55ae1e95-beff-4fd0-99b0-aa0d23c29729_workspace"

from llama_index.llms import GradientBaseModelLLM


def AppNameFinder(text):
    try:
        text = text.replace("\n", "").replace("\t", "").replace("  ", "")
        llm = GradientBaseModelLLM(
            base_model_slug="llama2-7b-chat",
            max_tokens=100,
        )
        result = llm.complete(
            f"From this text {text} Find the name of website name and product name and give answer stictly in the format App/website Name: Here should be the app/website name, Product Name: Here should be product name.")
        result = str(result)
        print(result)
        name_ind = result.find("App/website Name: ")
        prod_ind = result.find("Product Name: ")
        app_name = result[name_ind+18: prod_ind]
        prod_name = result[prod_ind+14: ]
        app_name = app_name.replace("\n", "")
        return [app_name, prod_name]
        
    except:
        return ['unkonwn', 'unkonwn']

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