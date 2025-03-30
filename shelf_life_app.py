import streamlit as st
from recipe_matcher import load_recipes, match_recipes

st.set_page_config(
    page_title="Shelf Life 🍽️",
    layout="wide",
    page_icon="🍽️"
)

# Load recipes
data_load_state = st.text("Loading recipes...")
recipes_df = load_recipes()
data_load_state.text("Recipes loaded successfully! 🍾")

# App Header with custom style
st.markdown("""
    <style>
        .main-title {
            font-size: 3em;
            font-weight: bold;
            color: #4CAF50;
            text-align: center;
        }
        .subheader {
            text-align: center;
            font-size: 1.2em;
            color: #666;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
            border-radius: 8px;
            padding: 10px 24px;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #45a049;
            color: white;
        }
    </style>
    <div class='main-title'>🍽️ Shelf Life</div>
    <div class='subheader'>Turn your fridge leftovers into recipes you'll love</div>
""", unsafe_allow_html=True)

st.markdown("---")

# User Input Section
st.subheader("📃 Enter the ingredients you have")
ingredients_input = st.text_area(
    "Separate each item with a comma:",
    placeholder="e.g., eggs, milk, tomato, spinach"
)

# Match Recipes Button
if st.button("🍳 Find Recipes"):
    if ingredients_input.strip():
        user_ingredients = [item.strip().lower() for item in ingredients_input.split(",") if item.strip()]
        matched_recipes = match_recipes(user_ingredients, recipes_df)

        if matched_recipes:
            st.success(f"✅ Found {len(matched_recipes)} matching recipe(s)!")
            for recipe in matched_recipes:
                with st.expander(f"🔖 {recipe['name']} ({recipe['minutes']} min) – Match: {round(recipe['score'] * 100)}%"):
                    st.markdown("**Ingredients:**")
                    st.write(", ".join(recipe['ingredients']))
                    st.markdown("**Cooking Steps:**")
                    for step in recipe['steps']:
                        st.markdown(f"- {step}")
        else:
            st.warning("⚠️ No recipes found. Try fewer or different ingredients.")
    else:
        st.error("❌ Please enter at least one ingredient.")

# Footer
st.markdown("""
    <hr style='border: 1px solid #ccc;'>
    <div style='text-align: center; color: #999;'>
        🌍 Built with love by Jeff | ShelfLife &copy; 2025
    </div>
""", unsafe_allow_html=True)
