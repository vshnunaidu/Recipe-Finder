import streamlit as st
import pandas as pd
from src.recipe_search import RecipeSearchEngine
import json
import os
import urllib.parse

# Set up page configuration
st.set_page_config(
    page_title="RecipeFind",
    layout="wide"
)

# Custom CSS to improve appearance
st.markdown("""
    <style>
    .recipe-box {
        padding: 20px;
        border-radius: 5px;
        background-color: #f0f2f6;
        margin: 10px 0;
    }
    .recipe-title {
        color: #1e88e5;
        text-decoration: none;
    }
    .external-link {
        font-size: 0.8em;
        color: #666;
        text-decoration: none;
        margin-left: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize search engine
@st.cache_resource
def load_search_engine():
    engine = RecipeSearchEngine()
    engine.load_recipes('data/sample_recipes.csv')
    return engine

def create_google_search_link(recipe_title):
    """Create a Google search URL for the recipe"""
    query = urllib.parse.quote(f"recipe {recipe_title}")
    return f"https://www.google.com/search?q={query}"

def create_youtube_search_link(recipe_title):
    """Create a YouTube search URL for the recipe"""
    query = urllib.parse.quote(f"how to make {recipe_title} recipe")
    return f"https://www.youtube.com/results?search_query={query}"

# Main title
st.title('RecipeFind')
st.subheader('Find recipes based on ingredients you have')

# Create three columns for input
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    ingredients_input = st.text_input(
        "Enter ingredients (separated by commas)",
        placeholder="e.g., chicken, mushroom, garlic"
    )

with col2:
    dietary_restriction = st.selectbox(
        "Dietary Restrictions",
        ["None", "Vegetarian", "Hindu", "Gluten-Free", "Dairy-Free"]
    )

with col3:
    recipes_per_page = st.selectbox(
        "Recipes per page",
        [5, 10, 20, 50],
        index=1  # Default to 10 recipes per page
    )
    search_button = st.button("Search Recipes")

if ingredients_input and search_button:
    ingredients = [ing.strip() for ing in ingredients_input.split(',')]
    
    engine = load_search_engine()
    results = engine.search(ingredients, top_k=None)
    
    # Filter results based on dietary restrictions
    filtered_results = results
    if dietary_restriction != "None":
        restricted_ingredients = {
            "Vegetarian": ["chicken", "beef", "pork", "fish", "meat", "bacon", "ham", "turkey", "lamb"],
            "Hindu": ["beef", "veal", "calf", "cow", "cattle", "gelatin", "lard", "tallow", "rennet", "pepsin"],
            "Gluten-Free": ["flour", "bread", "pasta", "wheat", "barley", "rye"],
            "Dairy-Free": ["milk", "cheese", "cream", "butter", "yogurt"]
        }
        
        filtered_results = []
        for recipe in results:
            ingredients_text = ' '.join(recipe['ingredients']).lower()
            if not any(restricted in ingredients_text for restricted in restricted_ingredients.get(dietary_restriction, [])):
                filtered_results.append(recipe)

    total_results = len(filtered_results)
    total_pages = (total_results + recipes_per_page - 1)//recipes_per_page

    st.subheader(f"Found {total_results} recipes")
    
    if total_pages > 1:
        col1, col2 = st.columns([4, 1])
        with col2:
            current_page = st.selectbox("Page", range(1, total_pages + 1)) - 1
    else:
        current_page = 0

    start_idx = current_page * recipes_per_page
    end_idx = min(start_idx + recipes_per_page, total_results)

    st.write(f"Showing recipes {start_idx + 1} to {end_idx} of {total_results}")

    for recipe in filtered_results[start_idx:end_idx]:
        google_link = create_google_search_link(recipe['title'])
        youtube_link = create_youtube_search_link(recipe['title'])
        
        # Create a box for each recipe
        st.markdown(f"""
        <div class="recipe-box">
            <h3>
                {recipe['title']}
                <a href="{google_link}" target="_blank" class="external-link">Search Recipe</a>
                <a href="{youtube_link}" target="_blank" class="external-link">Watch Recipe on YouTube</a>
            </h3>
            <p><strong>Matching ingredients:</strong> {recipe['matching_ingredients']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Ingredients:**")
            for ing in recipe['ingredients']:
                st.write(f"• {ing}")
        
        with col2:
            st.markdown("**Directions:**")
            try:
                if isinstance(recipe['directions'], str):
                    directions = json.loads(recipe['directions'])
                else:
                    directions = recipe['directions']
                
                for j, step in enumerate(directions, 1):
                    st.write(f"{j}. {step}")
            except Exception as e:
                st.write("Directions not available in the correct format.")
        
        st.markdown("---")

    # Add pagination controls at the bottom
    if total_pages > 1:
        cols = st.columns(5)
        with cols[2]:
            if current_page > 0:
                if st.button("← Previous Page"):
                    current_page -= 1
        with cols[3]:
            if current_page < total_pages - 1:
                if st.button("Next Page →"):
                    current_page += 1

# Add footer
st.markdown("---")
st.markdown("🥘*RecipeFind*🥘 ")