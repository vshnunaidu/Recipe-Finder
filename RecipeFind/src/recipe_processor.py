import json
from typing import List, Dict

def prepare_sample_data(input_file: str, output_file: str, sample_size: int = 100):
    """Create a smaller sample dataset for testing"""
    with open(input_file, 'r') as f:
        recipes = []
        for i, line in enumerate(f):
            if i >= sample_size:
                break
            recipes.append(json.loads(line))
    
    with open(output_file, 'w') as f:
        json.dump(recipes, f, indent=2)

def clean_ingredient(ingredient: str) -> str:
    """Clean and normalize ingredient text"""
    return ingredient.lower().strip()

def process_ingredients(ingredients: List[str]) -> List[str]:
    """Process list of ingredients"""
    return [clean_ingredient(ing) for ing in ingredients]