
# RecipeFind - Ingredient-Based Recipe Search Engine



## Installation

 Clone the repository:
```bash
git clone https://github.com/yourusername/RecipeFind.git
cd RecipeFind

Install the required packages:
pip install pandas numpy
pip install streamlit
Make sure it is the following directory structure:

CopyRecipeFind/
├── data/
│   └── sample_recipes.csv
├── src/
│   ├── __init__.py
│   └── recipe_search.py
├── tests/
│   ├── __init__.py
│   └── test_search.py
└── test_run.py

run test by running: 
streamlit run app.py

run sample search by running
python test_run.py