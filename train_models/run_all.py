import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from train_model import train_category_model

for category in ["toys", "furniture", "clothing", "electronics", "groceries"]:
    train_category_model(category)
