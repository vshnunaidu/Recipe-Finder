import pandas as pd
import math
from typing import List, Dict
import json
import numpy as np

class RecipeSearchEngine:
    def __init__(self):
        self.recipes_df = None
        self.ingredient_idf = {}
        self.avgdl = 0
        self.k1 = 1.5
        self.b = 0.75

    def load_recipes(self, file_path: str):
        """Load recipes from CSV file"""
        self.recipes_df = pd.read_csv(file_path)
        self._calculate_idf()
        self._calculate_avgdl()

    def _get_ingredients_list(self, ingredients_str: str) -> List[str]:
        """Convert ingredients string to list and clean"""
        try:
            ingredients = json.loads(ingredients_str)
            return [ing.lower().strip() for ing in ingredients]
        except:
            return []

    def _calculate_idf(self):
        """Calculate IDF values for all ingredients"""
        N = len(self.recipes_df)
        ingredient_doc_count = {}
        
        # Count documents containing each ingred.
        for idx, row in self.recipes_df.iterrows():
            ingredients = self._get_ingredients_list(row['ingredients'])
            # Create a single string of all ingredients for partial matching
            ingredient_text = ' '.join(ingredients).lower()
            
            # Count partial matches
            for common_ingredient in ['chicken', 'mushroom', 'beef', 'pork', 'fish', 'rice', 
                                    'potato', 'tomato', 'onion', 'garlic']:
                if common_ingredient in ingredient_text:
                    ingredient_doc_count[common_ingredient] = ingredient_doc_count.get(common_ingredient, 0) + 1

        # Calculate IDF
        for ingredient, doc_count in ingredient_doc_count.items():
            self.ingredient_idf[ingredient] = math.log((N - doc_count + 0.5) / (doc_count + 0.5) + 1)

    def _calculate_avgdl(self):
        """Calculate average ingredient list length"""
        total_length = sum(len(self._get_ingredients_list(row['ingredients'])) 
                          for _, row in self.recipes_df.iterrows())
        self.avgdl = total_length / len(self.recipes_df)

    def _bm25_score(self, query_ingredients: List[str], recipe_row) -> float:
        """Calculate BM25 score for a recipe given query ingredients"""
        score = 0
        recipe_ingredients = self._get_ingredients_list(recipe_row['ingredients'])
        doc_length = len(recipe_ingredients)
        
        # Create a single string of all ingredients for partial matching
        ingredient_text = ' '.join(recipe_ingredients).lower()
        
        for q_ingredient in query_ingredients:
            q_ingredient = q_ingredient.lower().strip()
            # More lenient matching - check for partial matches
            tf = sum(1 for ing in recipe_ingredients if q_ingredient in ing.lower())
            if tf == 0 and q_ingredient in ingredient_text:
                tf = 1
                
            # BM25 scoring formula
            idf = self.ingredient_idf.get(q_ingredient, 0)
            if idf == 0:  # If ingredient not in IDF, give it a default value
                idf = 1.0
            numerator = tf * (self.k1 + 1)
            denominator = tf + self.k1 * (1 - self.b + self.b * doc_length / self.avgdl)
            score += idf * numerator / denominator
            
        return score

    def search(self, ingredients: List[str], top_k: int = None) -> List[Dict]:
        """Search for recipes matching given ingredients"""
        if not ingredients:
            return []
            
        # Print debug info
        print(f"Total recipes in dataset: {len(self.recipes_df)}")
            
        # Calculate scores for all recipes
        scored_recipes = []
        for _, recipe in self.recipes_df.iterrows():
            score = self._bm25_score(ingredients, recipe)
            recipe_ingredients = self._get_ingredients_list(recipe['ingredients'])
            
            # Count partial matches - make this more lenient
            matching_count = sum(1 for ing in ingredients 
                               if any(ing.lower() in recipe_ing.lower() 
                                   for recipe_ing in recipe_ingredients))
            
            # Include recipe if it has any ingredient match
            if any(ing.lower() in ' '.join(recipe_ingredients).lower() for ing in ingredients):
                scored_recipes.append({
                    'title': recipe['title'],
                    'ingredients': recipe_ingredients,
                    'directions': recipe['directions'],
                    'link': recipe['link'],
                    'source': recipe['source'],
                    'score': score,
                    'matching_ingredients': matching_count
                })
        
        # Debug print
        print(f"Found {len(scored_recipes)} recipes with matches")
        
        # Sort by score and return results
        scored_recipes.sort(key=lambda x: (-x['matching_ingredients'], -x['score']))
        
        if top_k:
            return scored_recipes[:top_k]
        return scored_recipes
