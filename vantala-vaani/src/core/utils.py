import re
import csv
import os
from datetime import datetime
import streamlit as st
from pathlib import Path

# Try to import googletrans, fallback if not available
try:
    from googletrans import Translator as GoogleTranslator
    TRANSLATION_AVAILABLE = True
except ImportError:
    GoogleTranslator = None
    TRANSLATION_AVAILABLE = False

class RecipeUtils:
    """Utility class for recipe collection functionality"""

    def __init__(self):
        self.translation_available = TRANSLATION_AVAILABLE
        if self.translation_available and GoogleTranslator:
            try:
                self.translator = GoogleTranslator()
            except Exception:
                self.translator = None
                self.translation_available = False
        else:
            self.translator = None

        self.telugu_pattern = re.compile(r'[\u0C00-\u0C7F]')
        # Set paths relative to project root
        self.project_root = Path(__file__).parent.parent.parent
        self.data_dir = self.project_root / "data"
        self.data_dir.mkdir(exist_ok=True)

    def detect_language(self, text):
        """Detect if text contains Telugu characters"""
        return 'telugu' if self.telugu_pattern.search(text) else 'english'

    def translate_to_telugu(self, text):
        """Translate English text to Telugu"""
        if not self.translation_available or not self.translator:
            st.warning("⚠️ Translation service not available. Please enter text in Telugu directly.")
            return text

        try:
            if self.detect_language(text) == 'english' and text.strip():
                result = self.translator.translate(text, src='en', dest='te')
                return result.text
            return text
        except Exception as e:
            st.warning(f"Translation warning: Could not translate '{text[:50]}...' - {e}")
            return text

    def save_recipe_to_csv(self, recipe_data, filename='recipes.csv'):
        """Save recipe data to CSV file"""
        file_path = self.data_dir / filename
        file_exists = file_path.exists()

        headers = [
            'Timestamp', 'Recipe Name (Telugu)', 'Ingredients (Telugu)', 'Steps (Telugu)',
            'Original Language', 'Original Recipe Name', 'Original Ingredients', 'Original Steps'
        ]

        try:
            with open(file_path, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)

                if not file_exists:
                    writer.writerow(headers)

                writer.writerow(recipe_data)

            return file_path
        except Exception as e:
            st.error(f"Error saving to CSV: {e}")
            return None

    def validate_recipe_input(self, recipe_name, ingredients, steps):
        """Validate recipe input fields"""
        errors = []

        if not recipe_name.strip():
            errors.append("Recipe name is required")

        if not ingredients.strip():
            errors.append("Ingredients are required")

        if not steps.strip():
            errors.append("Cooking steps are required")

        # Check minimum length
        if len(recipe_name.strip()) < 2:
            errors.append("Recipe name should be at least 2 characters")

        if len(ingredients.strip()) < 10:
            errors.append("Ingredients description should be more detailed")

        if len(steps.strip()) < 20:
            errors.append("Cooking steps should be more detailed")

        return errors

    def format_recipe_preview(self, recipe_name, ingredients, steps, max_length=100):
        """Format recipe data for preview"""
        preview_data = {}

        if recipe_name:
            preview_data['name'] = recipe_name

        if ingredients:
            preview_data['ingredients'] = (
                ingredients[:max_length] + "..." if len(ingredients) > max_length
                else ingredients
            )

        if steps:
            preview_data['steps'] = (
                steps[:max_length] + "..." if len(steps) > max_length
                else steps
            )

        return preview_data

    def get_recipe_statistics(self, csv_file='recipes.csv'):
        """Get statistics about saved recipes"""
        file_path = self.data_dir / csv_file
        if not file_path.exists():
            return None

        try:
            import pandas as pd
            df = pd.read_csv(file_path)

            stats = {
                'total_recipes': len(df),
                'telugu_recipes': len(df[df['Original Language'] == 'తెలుగు (Telugu)']),
                'english_recipes': len(df[df['Original Language'] == 'English']),
                'latest_recipe': df['Timestamp'].max() if not df.empty else None
            }

            return stats
        except Exception as e:
            st.error(f"Error reading recipe statistics: {e}")
            return None

    def search_recipes(self, search_term, csv_file='recipes.csv'):
        """Search recipes by name or ingredients"""
        file_path = self.data_dir / csv_file
        if not file_path.exists():
            return []

        try:
            import pandas as pd
            df = pd.read_csv(file_path)

            # Search in recipe names and ingredients
            mask = (
                df['Recipe Name (Telugu)'].str.contains(search_term, case=False, na=False) |
                df['Original Recipe Name'].str.contains(search_term, case=False, na=False) |
                df['Ingredients (Telugu)'].str.contains(search_term, case=False, na=False) |
                df['Original Ingredients'].str.contains(search_term, case=False, na=False)
            )

            return df[mask].to_dict('records')
        except Exception as e:
            st.error(f"Error searching recipes: {e}")
            return []
