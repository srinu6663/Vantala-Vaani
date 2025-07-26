#!/usr/bin/env python3
"""
వంటల వాణి (Vantala Vaani) - Recipe Collection System
Main application launcher with interactive menu system.
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Main interactive menu for the application"""
    print("🍛 వంటల వాణి (Vantala Vaani) - Recipe Collection System")
    print("=" * 60)

    while True:
        print("\nAvailable operations:")
        print("1. 📝 Recipe Collection Interface (Streamlit App)")
        print("2. 🔄 Data Preprocessing Pipeline")
        print("3. 📊 Dataset Statistics")
        print("4. 🧪 System Tests")
        print("5. ❌ Exit")

        try:
            choice = input("\nSelect an option (1-5): ").strip()

            if choice == "1":
                print("\n📝 Starting Recipe Collection Interface...")
                launch_recipe_collection()
                break

            elif choice == "2":
                print("\n🔄 Starting Data Preprocessing...")
                launch_preprocessing()
                break

            elif choice == "3":
                print("\n📊 Showing Dataset Statistics...")
                show_statistics()
                break

            elif choice == "4":
                print("\n🧪 Running System Tests...")
                run_tests()
                break

            elif choice == "5":
                print("\n👋 Goodbye!")
                sys.exit(0)

            else:
                print("❌ Invalid choice. Please select 1-5.")

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ Error: {e}")

def launch_recipe_collection():
    """Launch the Streamlit recipe collection interface"""
    try:
        import subprocess
        # Change to project root
        os.chdir(Path(__file__).parent)
        # Launch Streamlit with the recipe collection app
        subprocess.run([sys.executable, "-m", "streamlit", "run", "src/core/recipe_collection.py"])
    except Exception as e:
        print(f"❌ Error launching recipe collection: {e}")

def launch_preprocessing():
    """Launch the data preprocessing pipeline"""
    try:
        # Change to project root for data access
        os.chdir(Path(__file__).parent)

        # Import and run preprocessing
        sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
        from src.preprocessing.data_preprocessor import RecipeDataPreprocessor

        input_file = "data/recipes.csv"
        if os.path.exists(input_file):
            processor = RecipeDataPreprocessor(input_file)
            processed_recipes, qa_pairs = processor.process_all_recipes()

            if processed_recipes:
                output_files = processor.save_to_json("data/processed")
                print(f"\n✅ Processing completed!")
                print(f"📁 Output files created:")
                for format_name, file_path in output_files.items():
                    print(f"  {format_name}: {file_path}")
            else:
                print("No recipes to process.")
        else:
            print(f"No data file found at {input_file}")
            print("Please collect some recipes first using option 1")
    except Exception as e:
        print(f"❌ Error in preprocessing: {e}")

def show_statistics():
    """Show dataset statistics"""
    try:
        # Import the preprocessor directly
        sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
        from src.preprocessing.data_preprocessor import RecipeDataPreprocessor

        input_file = "data/recipes.csv"
        if os.path.exists(input_file):
            processor = RecipeDataPreprocessor(input_file)
            df = processor.load_recipes()

            if len(df) > 0:
                # Process recipes to generate statistics
                processor.process_all_recipes()
                stats = processor.generate_statistics()

                print(f"\n📊 Dataset Statistics:")
                print(f"Total Recipes: {stats.get('total_recipes', 0)}")
                print(f"Processed Recipes: {stats.get('processed_recipes', 0)}")
                print(f"Generated Q&A Pairs: {stats.get('total_qa_pairs', 0)}")
                print(f"Duplicates Removed: {stats.get('duplicates_removed', 0)}")

                if 'categories' in stats:
                    print(f"\nRecipe Categories:")
                    for category, count in stats['categories'].items():
                        print(f"  {category}: {count}")

                if 'languages' in stats:
                    print(f"\nLanguage Distribution:")
                    for lang, count in stats['languages'].items():
                        print(f"  {lang}: {count}")
            else:
                print("No recipes found in the dataset.")
        else:
            print(f"No data file found at {input_file}")
            print("Please collect some recipes first using option 1")
    except Exception as e:
        print(f"❌ Error showing statistics: {e}")

def run_tests():
    """Run system tests"""
    try:
        import subprocess
        os.chdir(Path(__file__).parent)
        subprocess.run([sys.executable, "tests/test_setup.py"])
    except Exception as e:
        print(f"❌ Error running tests: {e}")

if __name__ == "__main__":
    main()
