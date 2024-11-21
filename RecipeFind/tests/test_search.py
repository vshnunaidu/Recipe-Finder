import os
import sys
import unittest
import json


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.recipe_search import RecipeSearchEngine

class TestRecipeSearch(unittest.TestCase):
    def setUp(self):
        self.search_engine = RecipeSearchEngine()
        data_path = os.path.join('data', 'sample_recipes.csv')
        self.search_engine.load_recipes(data_path)
        
        # Print some debug information
        print("\nDebug Information:")
        print(f"Number of recipes loaded: {len(self.search_engine.recipes_df)}")
        
        # Print first few recipes and their ingredients
        print("\nSample of loaded recipes:")
        for _, recipe in self.search_engine.recipes_df.head().iterrows():
            print(f"\nTitle: {recipe['title']}")
            try:
                ingredients = json.loads(recipe['ingredients'])
                print(f"Ingredients: {ingredients}")
            except json.JSONDecodeError:
                print(f"Raw ingredients string: {recipe['ingredients']}")

    def test_basic_search(self):
        # Test with ingredients (in this case chicken&mushroom)
        search_terms = ['chicken', 'mushroom']
        print(f"\nSearching for: {search_terms}")
        
        results = self.search_engine.search(search_terms)
        
        print(f"\nNumber of results found: {len(results)}")
        
        if len(results) == 0:
            # Print debug info
            print("\nDebug: Checking first few recipes for matches...")
            for _, recipe in self.search_engine.recipes_df.head().iterrows():
                score = self.search_engine._bm25_score(search_terms, recipe)
                ingredients = json.loads(recipe['ingredients'])
                print(f"\nTitle: {recipe['title']}")
                print(f"Score: {score}")
                print(f"Ingredients: {ingredients}")
        
        self.assertTrue(len(results) > 0, "No results found in search")
        
        # Print results if found
        if len(results) > 0:
            print("\nSearch Results:")
            for i, result in enumerate(results, 1):
                print(f"\n{i}. {result['title']}")
                print(f"Matching ingredients: {result['matching_ingredients']}")
                print(f"Score: {result['score']:.2f}")
                print(f"Ingredients: {result['ingredients']}")

    def test_empty_query(self):
        results = self.search_engine.search([])
        self.assertEqual(len(results), 0)

if __name__ == '__main__':
    unittest.main()