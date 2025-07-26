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

        # Basic cooking terms dictionary for fallback translation
        self.basic_translations = {
            'rice': 'అన్నం', 'oil': 'నూనె', 'salt': 'ఉప్పు', 'water': 'నీరు',
            'onion': 'ఉల్లిపాయ', 'garlic': 'వెల్లుల్లి', 'ginger': 'అల్లం',
            'tomato': 'టొమాటో', 'green chili': 'పచ్చిమిరపకాయ', 'red chili': 'ఎర్రమిరపకాయ',
            'turmeric': 'పసుపు', 'coriander': 'ధనియాలు', 'cumin': 'జీలకర్ర',
            'mustard seeds': 'ఆవాలు', 'curry leaves': 'కరివేపాకు', 'coconut': 'కొబ్బరి',
            'dal': 'పప్పు', 'lentils': 'పప్పు', 'chicken': 'కోడిమాంసం', 'fish': 'చేప',
            'mutton': 'మటన్', 'vegetables': 'కూరగాయలు', 'potato': 'బంగాళాదుంప',
            'carrot': 'కేరట్', 'beans': 'బీన్స్', 'cabbage': 'కాబేజీ'
        }

    def detect_language(self, text):
        """Detect if text contains Telugu characters"""
        return 'telugu' if self.telugu_pattern.search(text) else 'english'

    def basic_translate(self, text):
        """Basic fallback translation using dictionary"""
        if not text:
            return text

        translated_text = text.lower()
        for english_word, telugu_word in self.basic_translations.items():
            translated_text = translated_text.replace(english_word, telugu_word)

        # If we made some translations, show a notice
        if translated_text != text.lower():
            st.info("🔄 Using basic translation for common cooking terms.")
            return translated_text
        return text

    def translate_to_telugu(self, text):
        """Translate English text to Telugu"""
        if not text or not text.strip():
            return text

        # If input is already Telugu, return as-is
        if self.detect_language(text) == 'telugu':
            return text

        # Try Google Translate first if available
        if self.translation_available and self.translator:
            try:
                result = self.translator.translate(text, src='en', dest='te')
                if result and result.text:
                    return result.text
            except Exception as e:
                # Only show translation error once per session
                if not hasattr(st.session_state, 'translation_error_shown'):
                    st.warning(f"⚠️ Google Translate temporarily unavailable. Using basic translation.")
                    st.session_state.translation_error_shown = True

        # Fallback to basic translation
        if self.detect_language(text) == 'english':
            return self.basic_translate(text)

        # If nothing else worked, show warning only once
        if not hasattr(st.session_state, 'translation_warning_shown'):
            st.info("💡 For best results, enter your recipe directly in Telugu.")
            st.session_state.translation_warning_shown = True

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
