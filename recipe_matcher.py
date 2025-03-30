import pandas as pd
import os
from rapidfuzz import fuzz

def load_recipes(filepath='data/recipes_cleaned.csv'):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(current_dir, filepath)

    # Load the cleaned CSV file
    recipes_df = pd.read_csv(full_path, encoding='latin1', delimiter=',', on_bad_lines='skip')
    recipes_df = recipes_df[['name', 'ingredients', 'steps', 'minutes']]
    
    # Convert ingredient and step strings into lists
    recipes_df['ingredients'] = recipes_df['ingredients'].apply(eval)
    recipes_df['steps'] = recipes_df['steps'].apply(eval)

    return recipes_df

def match_recipes(user_ingredients, recipes_df, threshold=80, top_n=3):
    scored_recipes = []

    for _, row in recipes_df.iterrows():
        recipe_ingredients = row['ingredients']
        
        match_count = sum(
            any(fuzz.ratio(ui.lower(), ri.lower()) >= threshold for ui in user_ingredients)
            for ri in recipe_ingredients
        )
        
        match_ratio = match_count / len(recipe_ingredients)

        # Only include recipes with 60% or higher ingredient match
        if match_ratio >= 0.6:
            scored_recipes.append({
                'name': row['name'],
                'ingredients': recipe_ingredients,
                'steps': row['steps'],
                'minutes': row['minutes'],
                'score': match_ratio
            })

    # Sort matches by best score and return top results
    top_matches = sorted(scored_recipes, key=lambda r: r['score'], reverse=True)[:top_n]
    return top_matches
