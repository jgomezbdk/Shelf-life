import streamlit as st
from recipe_matcher import load_recipes, match_recipes

st.set_page_config(page_title="Shelf Life 🍽️", layout="wide")

# App title
st.title("🥦 Shelf Life – Find Recipes from Your Fridge!")

# Load recipes dataset
recipes_df = load_recipes()

# User input
ingredients_input = st.text_area(
    "📝 Enter ingredients you currently have (separate by commas):",
    "tomato, cheese, bread"
)

# Button to trigger recipe matching
if st.button("🍳 Find Recipes"):
    user_ingredients = [item.strip().lower() for item in ingredients_input.split(",")]
    
    # Call your matching function
    matched_recipes = match_recipes(user_ingredients, recipes_df)

    # Display results
    if matched_recipes:
        st.success(f"✅ Found {len(matched_recipes)} recipe(s) you can cook!")
        for recipe in matched_recipes:
            with st.expander(f"📌 {recipe['name']} ({recipe['minutes']} min) – Match: {round(recipe['score'] * 100)}%"):
                st.write("**Ingredients:**")
                st.write(", ".join(recipe['ingredients']))
                st.write("**Cooking Steps:**")
                for step in recipe['steps']:
                    st.write(f"- {step}")
    else:
        st.warning("⚠️ No recipes found. Try different or fewer ingredients.")