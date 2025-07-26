import streamlit as st
import pandas as pd
from datetime import datetime
import os
import sys
import csv
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.utils import RecipeUtils
from config.app_config import *

# Initialize recipe utilities
recipe_utils = RecipeUtils()

def main():
    st.set_page_config(
        page_title="వంటల వాణి - Recipe Collection",
        page_icon="🍛",
        layout="wide"
    )

    # Initialize session state for recipes if not exists
    if 'saved_recipes' not in st.session_state:
        st.session_state.saved_recipes = []

    # Custom CSS for Telugu font support
    st.markdown("""
    <style>
    .telugu-text {
        font-family: 'Noto Sans Telugu', 'Gautami', 'Akshar Unicode', sans-serif;
        font-size: 16px;
    }
    .recipe-form {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
    }
    </style>
    """, unsafe_allow_html=True)

    # Title in both languages
    st.title("🍛 వంటల వాణి - Recipe Collection")
    st.title("🍛 Family Recipe Collection")

    st.markdown("---")

    # Language selection
    st.subheader("భాష ఎంపిక / Language Selection")
    input_language = st.radio(
        "Choose your input language / మీ భాషను ఎంచుకోండి:",
        ("English", "తెలుగు (Telugu)"),
        horizontal=True
    )

    st.markdown("---")

    # Recipe form
    with st.container():
        st.subheader("రెసిపీ వివరాలు / Recipe Details")

        col1, col2 = st.columns([1, 1])

        with col1:
            if input_language == "తెలుగు (Telugu)":
                st.markdown("### తెలుగులో రెసిపీ నమోదు")
                recipe_name = st.text_input(
                    "వంటకం పేరు:",
                    placeholder="ఉదా: కోడి కర్రీ, పులిహోర, దోసె..."
                )

                ingredients = st.text_area(
                    "కావలసిన వస్తువులు:",
                    placeholder="ఉదా: అన్నం - 2 కప్పులు\nఉల్లిపాయలు - 2\nమిరపకాయలు - 3...",
                    height=150
                )

                steps = st.text_area(
                    "తయారీ విధానం:",
                    placeholder="దశలవారీగా వంట విధానాన్ని రాయండి...",
                    height=200
                )
            else:
                st.markdown("### Recipe Entry in English")
                recipe_name = st.text_input(
                    "Recipe Name:",
                    placeholder="e.g: Chicken Curry, Pulihora, Dosa..."
                )

                ingredients = st.text_area(
                    "Ingredients:",
                    placeholder="e.g: Rice - 2 cups\nOnions - 2\nGreen chilies - 3...",
                    height=150
                )

                steps = st.text_area(
                    "Cooking Steps:",
                    placeholder="Write step-by-step cooking instructions...",
                    height=200
                )

        # with col2:
        #     # st.markdown("### Preview / మునుజూపు")

        #     if recipe_name or ingredients or steps:
        #         if input_language == "English":
        #             st.info("📝 Auto-translation to Telugu will be applied when saving")

        #             # Show preview
        #             st.markdown("**Current Input:**")
        #             if recipe_name:
        #                 st.write(f"**Recipe:** {recipe_name}")
        #             if ingredients:
        #                 st.write(f"**Ingredients:** {ingredients[:100]}...")
        #             if steps:
        #                 st.write(f"**Steps:** {steps[:100]}...")
        #         else:
        #             st.success("✅ Telugu input detected")
        #             if recipe_name:
        #                 st.write(f"**వంటకం:** {recipe_name}")
        #             if ingredients:
        #                 st.write(f"**వస్తువులు:** {ingredients[:100]}...")
        #             if steps:
        #                 st.write(f"**విధానం:** {steps[:100]}...")

    st.markdown("---")

    # Submit button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🍛 రెసిపీ సేవ్ చేయండి / Save Recipe", type="primary", use_container_width=True):
            # Validate input
            validation_errors = recipe_utils.validate_recipe_input(recipe_name, ingredients, steps)

            if validation_errors:
                for error in validation_errors:
                    st.error(f"❌ {error}")
            else:
                with st.spinner("Saving recipe... / రెసిపీ సేవ్ చేస్తున్నాము..."):
                    try:
                        # Detect original language
                        original_language = input_language

                        # Store original text
                        original_recipe = recipe_name
                        original_ingredients = ingredients
                        original_steps = steps

                        # Translate to Telugu if input is English
                        if input_language == "English":
                            telugu_recipe_name = recipe_utils.translate_to_telugu(recipe_name)
                            telugu_ingredients = recipe_utils.translate_to_telugu(ingredients)
                            telugu_steps = recipe_utils.translate_to_telugu(steps)
                        else:
                            telugu_recipe_name = recipe_name
                            telugu_ingredients = ingredients
                            telugu_steps = steps

                        # Prepare data for CSV
                        recipe_data = [
                            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            telugu_recipe_name,
                            telugu_ingredients,
                            telugu_steps,
                            original_language,
                            original_recipe,
                            original_ingredients,
                            original_steps
                        ]

                        # Save to CSV
                        file_path = recipe_utils.save_recipe_to_csv(recipe_data)

                        # Also save to session state for immediate display
                        recipe_dict = {
                            'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            'Recipe Name (Telugu)': telugu_recipe_name,
                            'Ingredients (Telugu)': telugu_ingredients,
                            'Steps (Telugu)': telugu_steps,
                            'Original Language': original_language,
                            'Original Recipe Name': original_recipe,
                            'Original Ingredients': original_ingredients,
                            'Original Steps': original_steps
                        }
                        st.session_state.saved_recipes.append(recipe_dict)

                        # Success message
                        st.success("✅ రెసిపీ విజయవంతంగా సేవ్ అయ్యింది! / Recipe saved successfully!")
                        st.info(f"📊 Total recipes in this session: {len(st.session_state.saved_recipes)}")

                    except Exception as e:
                        st.error(f"❌ Error saving recipe: {e}")

    st.markdown("---")

    # View saved recipes
    if st.checkbox("📋 Saved Recipes చూడండి / View Saved Recipes"):
        # First check session state recipes
        if st.session_state.saved_recipes:
            st.subheader(f"📊 Total Recipes in Current Session: {len(st.session_state.saved_recipes)}")
            
            # Add download button for CSV
            if st.session_state.saved_recipes:
                # Create CSV data for download
                import io
                output = io.StringIO()
                headers = ['Timestamp', 'Recipe Name (Telugu)', 'Ingredients (Telugu)', 'Steps (Telugu)',
                          'Original Language', 'Original Recipe Name', 'Original Ingredients', 'Original Steps']
                
                writer = csv.writer(output)
                writer.writerow(headers)
                for recipe in st.session_state.saved_recipes:
                    writer.writerow([recipe[header] for header in headers])
                
                csv_data = output.getvalue()
                st.download_button(
                    label="📥 Download Recipes as CSV",
                    data=csv_data,
                    file_name=f"vantala_vaani_recipes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )

            # Display recipes from session state
            for idx, recipe in enumerate(st.session_state.saved_recipes):
                with st.expander(f"🍛 {recipe['Recipe Name (Telugu)']} ({recipe['Timestamp']})"):
                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown("**తెలుగు వెర్షన్ / Telugu Version:**")
                        st.write(f"**వంటకం:** {recipe['Recipe Name (Telugu)']}")
                        st.write(f"**వస్తువులు:** {recipe['Ingredients (Telugu)']}")
                        st.write(f"**విధానం:** {recipe['Steps (Telugu)']}")

                    with col2:
                        if recipe['Original Language'] == 'English':
                            st.markdown("**Original English Version:**")
                            st.write(f"**Recipe:** {recipe['Original Recipe Name']}")
                            st.write(f"**Ingredients:** {recipe['Original Ingredients']}")
                            st.write(f"**Steps:** {recipe['Original Steps']}")
                        else:
                            st.info("Originally submitted in Telugu")
        else:
            # Also check if there's a CSV file (for backward compatibility)
            data_dir = project_root / "data"
            csv_path = data_dir / "recipes.csv"
            if csv_path.exists():
                try:
                    df = pd.read_csv(csv_path)
                    if not df.empty:
                        st.subheader(f"📊 Previously Saved Recipes: {len(df)}")
                        st.info("ℹ️ Note: These are from previous sessions. New recipes will appear above.")

                        # Display CSV recipes
                        for idx, row in df.iterrows():
                            with st.expander(f"🍛 {row['Recipe Name (Telugu)']} ({row['Timestamp']})"):
                                col1, col2 = st.columns(2)

                                with col1:
                                    st.markdown("**తెలుగు వెర్షన్ / Telugu Version:**")
                                    st.write(f"**వంటకం:** {row['Recipe Name (Telugu)']}")
                                    st.write(f"**వస్తువులు:** {row['Ingredients (Telugu)']}")
                                    st.write(f"**విధానం:** {row['Steps (Telugu)']}")

                                with col2:
                                    if row['Original Language'] == 'English':
                                        st.markdown("**Original English Version:**")
                                        st.write(f"**Recipe:** {row['Original Recipe Name']}")
                                        st.write(f"**Ingredients:** {row['Original Ingredients']}")
                                        st.write(f"**Steps:** {row['Original Steps']}")
                                    else:
                                        st.info("Originally submitted in Telugu")
                    else:
                        st.info("📝 No recipes saved yet. Add your first recipe above!")
                except Exception as e:
                    st.warning(f"Could not read previous recipes: {e}")
                    st.info("📝 No recipes saved yet. Add your first recipe above!")
            else:
                st.info("📝 No recipes saved yet. Add your first recipe above!")
                
        # Clear session recipes button
        if st.session_state.saved_recipes:
            if st.button("🗑️ Clear Session Recipes"):
                st.session_state.saved_recipes = []
                st.success("Session recipes cleared!")
                st.experimental_rerun()

if __name__ == "__main__":
    main()
