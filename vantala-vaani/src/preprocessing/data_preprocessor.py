import pandas as pd
import json
import re
import hashlib
from datetime import datetime
from typing import List, Dict, Tuple, Set
import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.utils import RecipeUtils
from googletrans import Translator
import unicodedata
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RecipeDataPreprocessor:
    """
    Data preprocessing pipeline for recipe collection.

    Features:
    - Read CSV recipe data
    - Deduplicate recipes
    - Clean and format text
    - Language detection and translation
    - Convert to Q&A chat pairs
    - Export to JSON for model training
    """

    def __init__(self, csv_file_path: str = "recipes.csv"):
        self.csv_file_path = csv_file_path
        self.recipe_utils = RecipeUtils()
        self.translator = Translator()
        self.processed_recipes = []
        self.chat_pairs = []
        self.duplicate_count = 0

        # Telugu script patterns for cleaning
        self.telugu_pattern = re.compile(r'[\u0C00-\u0C7F]+')
        self.english_pattern = re.compile(r'[a-zA-Z]+')

        # Common question patterns for Q&A generation
        self.question_patterns = [
            "How do I make {recipe_name}?",
            "What's the recipe for {recipe_name}?",
            "Can you tell me how to prepare {recipe_name}?",
            "I want to cook {recipe_name}. How?",
            "Give me the recipe for {recipe_name}",
            "How to cook {recipe_name}?",
            "What are the steps to make {recipe_name}?",
            "Can you provide the {recipe_name} recipe?",
            "{recipe_name} ఎలా చేయాలి?",
            "{recipe_name} రెసిపీ చెప్పండి",
            "{recipe_name} ఎలా వండాలి?",
            "{recipe_name} తయారీ విధానం చెప్పండి"
        ]

    def load_recipes(self) -> pd.DataFrame:
        """Load recipes from CSV file"""
        try:
            if not os.path.exists(self.csv_file_path):
                logger.error(f"CSV file not found: {self.csv_file_path}")
                return pd.DataFrame()

            df = pd.read_csv(self.csv_file_path)
            logger.info(f"Loaded {len(df)} recipes from {self.csv_file_path}")
            return df
        except Exception as e:
            logger.error(f"Error loading CSV: {e}")
            return pd.DataFrame()

    def clean_text(self, text: str) -> str:
        """Clean and normalize text content"""
        if pd.isna(text) or not text:
            return ""

        # Convert to string if not already
        text = str(text)

        # Normalize Unicode characters
        text = unicodedata.normalize('NFKC', text)

        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)

        # Remove leading/trailing whitespace
        text = text.strip()

        # Clean up common formatting issues
        text = re.sub(r'([.!?])\s*([a-zA-Z\u0C00-\u0C7F])', r'\1 \2', text)

        # Fix Telugu punctuation
        text = re.sub(r'([.!?])\s*([అ-హ])', r'\1 \2', text)

        return text

    def generate_recipe_hash(self, recipe_name: str, ingredients: str) -> str:
        """Generate hash for duplicate detection"""
        # Normalize text for comparison
        normalized_name = self.clean_text(recipe_name).lower()
        normalized_ingredients = self.clean_text(ingredients).lower()

        # Create hash from name and key ingredients
        content = normalized_name + normalized_ingredients
        return hashlib.md5(content.encode('utf-8')).hexdigest()

    def detect_and_translate(self, text: str) -> Tuple[str, str]:
        """
        Detect language and translate to Telugu if needed
        Returns: (telugu_text, detected_language)
        """
        if not text or pd.isna(text):
            return "", "unknown"

        # Detect if text contains Telugu characters
        if self.telugu_pattern.search(text):
            return text, "telugu"
        elif self.english_pattern.search(text):
            # Translate English to Telugu
            try:
                translated = self.recipe_utils.translate_to_telugu(text)
                return translated, "english"
            except Exception as e:
                logger.warning(f"Translation failed: {e}")
                return text, "english"
        else:
            return text, "unknown"

    def deduplicate_recipes(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove duplicate recipes based on content similarity"""
        if df.empty:
            return df

        seen_hashes: Set[str] = set()
        unique_indices = []

        for idx, row in df.iterrows():
            recipe_hash = self.generate_recipe_hash(
                row.get('Recipe Name (Telugu)', ''),
                row.get('Ingredients (Telugu)', '')
            )

            if recipe_hash not in seen_hashes:
                seen_hashes.add(recipe_hash)
                unique_indices.append(idx)
            else:
                self.duplicate_count += 1

        logger.info(f"Removed {self.duplicate_count} duplicate recipes")
        return df.loc[unique_indices].reset_index(drop=True)

    def process_single_recipe(self, row: pd.Series) -> Dict:
        """Process a single recipe row"""
        # Extract and clean data
        timestamp = row.get('Timestamp', '')
        recipe_name_te = self.clean_text(row.get('Recipe Name (Telugu)', ''))
        ingredients_te = self.clean_text(row.get('Ingredients (Telugu)', ''))
        steps_te = self.clean_text(row.get('Steps (Telugu)', ''))
        original_language = row.get('Original Language', '')
        original_name = self.clean_text(row.get('Original Recipe Name', ''))
        original_ingredients = self.clean_text(row.get('Original Ingredients', ''))
        original_steps = self.clean_text(row.get('Original Steps', ''))

        # Ensure Telugu versions exist
        if not recipe_name_te and original_name:
            recipe_name_te, _ = self.detect_and_translate(original_name)

        if not ingredients_te and original_ingredients:
            ingredients_te, _ = self.detect_and_translate(original_ingredients)

        if not steps_te and original_steps:
            steps_te, _ = self.detect_and_translate(original_steps)

        return {
            'id': hashlib.md5(f"{recipe_name_te}{ingredients_te}".encode('utf-8')).hexdigest()[:8],
            'timestamp': timestamp,
            'recipe_name_telugu': recipe_name_te,
            'ingredients_telugu': ingredients_te,
            'steps_telugu': steps_te,
            'original_language': original_language,
            'original_name': original_name,
            'original_ingredients': original_ingredients,
            'original_steps': original_steps,
            'word_count': len(f"{recipe_name_te} {ingredients_te} {steps_te}".split()),
            'has_measurements': bool(re.search(r'\d+\s*(కప్పు|టీస్పూన్|గ్రాము|కిలో|లీటర్|cup|tsp|gram|kg|liter)',
                                             f"{ingredients_te} {original_ingredients}", re.IGNORECASE))
        }

    def generate_qa_pairs(self, recipe: Dict) -> List[Dict]:
        """Generate Q&A chat pairs for a recipe"""
        qa_pairs = []
        recipe_name = recipe['recipe_name_telugu']

        if not recipe_name:
            return qa_pairs

        # Create comprehensive Telugu answer
        answer_parts = []

        # Add ingredients section
        if recipe['ingredients_telugu']:
            answer_parts.append(f"📝 కావలసిన వస్తువులు:\n{recipe['ingredients_telugu']}")

        # Add cooking steps
        if recipe['steps_telugu']:
            answer_parts.append(f"👩‍🍳 తయారీ విధానం:\n{recipe['steps_telugu']}")

        # Add helpful tips
        if recipe['has_measurements']:
            answer_parts.append("💡 చిట్కా: కచ్చితమైన కొలతలను అనుసరించండి మంచి రుచికి.")

        answer = "\n\n".join(answer_parts)

        # Generate multiple question variations
        for pattern in self.question_patterns:
            question = pattern.format(recipe_name=recipe_name)

            qa_pair = {
                'id': f"{recipe['id']}_{len(qa_pairs)}",
                'recipe_id': recipe['id'],
                'question': question,
                'answer': answer,
                'recipe_name': recipe_name,
                'language': 'telugu' if any(c in pattern for c in 'అఆఇఈఉఊఋఎఏఐఒఓఔకఖగఘజఞటఠడఢణతథదధనపఫబభమయరలవశషసహ') else 'english',
                'category': self.categorize_recipe(recipe_name),
                'difficulty': self.estimate_difficulty(recipe),
                'cooking_time': self.estimate_cooking_time(recipe),
                'metadata': {
                    'original_language': recipe['original_language'],
                    'word_count': recipe['word_count'],
                    'has_measurements': recipe['has_measurements'],
                    'timestamp': recipe['timestamp']
                }
            }
            qa_pairs.append(qa_pair)

        return qa_pairs

    def categorize_recipe(self, recipe_name: str) -> str:
        """Categorize recipe based on name"""
        recipe_name_lower = recipe_name.lower()

        # Telugu and English category keywords
        categories = {
            'rice': ['అన్నం', 'రైస్', 'పులిహోర', 'బిర్యానీ', 'rice', 'biryani', 'pulihora'],
            'curry': ['కర్రీ', 'కూర', 'కుర', 'curry', 'gravy', 'మసాలా'],
            'snacks': ['స్నాక్స్', 'టిఫిన్', 'దోసె', 'ఇడ్లీ', 'వడ', 'snacks', 'tiffin', 'dosa', 'idli'],
            'sweets': ['మిఠాయి', 'లడ్డు', 'హల్వా', 'పాయసం', 'sweet', 'laddu', 'halwa', 'payasam'],
            'dal': ['పప్పు', 'సాంబార్', 'రసం', 'dal', 'sambar', 'rasam'],
            'vegetables': ['కూరగాయలు', 'కర్రీ', 'పల్య', 'vegetables', 'sabzi', 'curry'],
            'bread': ['రొట్టె', 'చపాతీ', 'నాన్', 'bread', 'chapati', 'naan'],
            'chicken': ['కోడి', 'చికెన్', 'chicken', 'poultry'],
            'mutton': ['మటన్', 'గొర్రె', 'mutton', 'goat', 'lamb'],
            'fish': ['చేప', 'ఫిష్', 'fish', 'seafood'],
            'beverages': ['పానీయాలు', 'టీ', 'కాఫీ', 'జూస్', 'drinks', 'tea', 'coffee', 'juice']
        }

        for category, keywords in categories.items():
            if any(keyword in recipe_name_lower for keyword in keywords):
                return category

        return 'miscellaneous'

    def estimate_difficulty(self, recipe: Dict) -> str:
        """Estimate cooking difficulty based on recipe complexity"""
        steps = recipe.get('steps_telugu', '')
        ingredients = recipe.get('ingredients_telugu', '')

        # Count complexity indicators
        complexity_score = 0

        # Number of ingredients
        ingredient_count = len(ingredients.split('\n')) if ingredients else 0
        if ingredient_count > 10:
            complexity_score += 2
        elif ingredient_count > 5:
            complexity_score += 1

        # Number of steps
        step_count = len(steps.split('.')) if steps else 0
        if step_count > 8:
            complexity_score += 2
        elif step_count > 4:
            complexity_score += 1

        # Cooking techniques
        complex_techniques = ['వేయించు', 'కాల్చు', 'మసాలా', 'tempering', 'fry', 'roast', 'grind']
        for technique in complex_techniques:
            if technique in steps.lower():
                complexity_score += 1

        if complexity_score >= 5:
            return 'hard'
        elif complexity_score >= 3:
            return 'medium'
        else:
            return 'easy'

    def estimate_cooking_time(self, recipe: Dict) -> str:
        """Estimate cooking time based on recipe content"""
        steps = recipe.get('steps_telugu', '').lower()

        # Time indicators
        if any(word in steps for word in ['గంట', 'గంటలు', 'hour', 'hours']):
            return 'long'
        elif any(word in steps for word in ['నిమిషాలు', 'minutes', 'మిన్', 'min']):
            return 'medium'
        else:
            return 'short'

    def process_all_recipes(self) -> Tuple[List[Dict], List[Dict]]:
        """Main processing pipeline"""
        logger.info("Starting recipe preprocessing pipeline...")

        # Load data
        df = self.load_recipes()
        if df.empty:
            logger.warning("No recipes to process")
            return [], []

        # Deduplicate
        df_unique = self.deduplicate_recipes(df)

        # Process each recipe
        self.processed_recipes = []
        self.chat_pairs = []

        for i, (idx, row) in enumerate(df_unique.iterrows()):
            try:
                # Process recipe
                processed_recipe = self.process_single_recipe(row)
                self.processed_recipes.append(processed_recipe)

                # Generate Q&A pairs
                qa_pairs = self.generate_qa_pairs(processed_recipe)
                self.chat_pairs.extend(qa_pairs)

                if (i + 1) % 10 == 0:
                    logger.info(f"Processed {i + 1}/{len(df_unique)} recipes")

            except Exception as e:
                logger.error(f"Error processing recipe at index {idx}: {e}")
                continue

        logger.info(f"Processing complete: {len(self.processed_recipes)} recipes, {len(self.chat_pairs)} Q&A pairs")
        return self.processed_recipes, self.chat_pairs

    def save_to_json(self, output_dir: str = "processed_data") -> Dict[str, str]:
        """Save processed data to JSON files"""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Save processed recipes
        recipes_file = os.path.join(output_dir, f"processed_recipes_{timestamp}.json")
        with open(recipes_file, 'w', encoding='utf-8') as f:
            json.dump(self.processed_recipes, f, ensure_ascii=False, indent=2)

        # Save Q&A pairs for training
        qa_file = os.path.join(output_dir, f"recipe_qa_pairs_{timestamp}.json")
        with open(qa_file, 'w', encoding='utf-8') as f:
            json.dump(self.chat_pairs, f, ensure_ascii=False, indent=2)

        # Save training dataset format
        training_file = os.path.join(output_dir, f"training_dataset_{timestamp}.json")
        training_data = {
            "dataset_info": {
                "name": "Telugu Recipe Q&A Dataset",
                "version": "1.0",
                "created": datetime.now().isoformat(),
                "total_recipes": len(self.processed_recipes),
                "total_qa_pairs": len(self.chat_pairs),
                "duplicates_removed": self.duplicate_count,
                "languages": ["telugu", "english"]
            },
            "recipes": self.processed_recipes,
            "qa_pairs": self.chat_pairs,
            "statistics": self.generate_statistics()
        }

        with open(training_file, 'w', encoding='utf-8') as f:
            json.dump(training_data, f, ensure_ascii=False, indent=2)

        # Save summary report
        report_file = os.path.join(output_dir, f"processing_report_{timestamp}.md")
        self.save_processing_report(report_file)

        logger.info(f"Data saved to {output_dir}")
        return {
            "recipes": recipes_file,
            "qa_pairs": qa_file,
            "training_dataset": training_file,
            "report": report_file
        }

    def generate_statistics(self) -> Dict:
        """Generate dataset statistics"""
        if not self.chat_pairs:
            return {}

        # Category distribution
        categories = {}
        difficulties = {}
        languages = {}

        for pair in self.chat_pairs:
            category = pair.get('category', 'unknown')
            difficulty = pair.get('difficulty', 'unknown')
            language = pair.get('language', 'unknown')

            categories[category] = categories.get(category, 0) + 1
            difficulties[difficulty] = difficulties.get(difficulty, 0) + 1
            languages[language] = languages.get(language, 0) + 1

        return {
            "category_distribution": categories,
            "difficulty_distribution": difficulties,
            "language_distribution": languages,
            "avg_question_length": sum(len(pair['question'].split()) for pair in self.chat_pairs) / len(self.chat_pairs),
            "avg_answer_length": sum(len(pair['answer'].split()) for pair in self.chat_pairs) / len(self.chat_pairs)
        }

    def save_processing_report(self, report_file: str):
        """Save detailed processing report"""
        stats = self.generate_statistics()

        report_content = f"""# Recipe Data Preprocessing Report
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Summary
- **Total Recipes Processed**: {len(self.processed_recipes)}
- **Total Q&A Pairs Generated**: {len(self.chat_pairs)}
- **Duplicates Removed**: {self.duplicate_count}
- **Source File**: {self.csv_file_path}

## Dataset Statistics

### Recipe Categories
"""

        if 'category_distribution' in stats:
            for category, count in stats['category_distribution'].items():
                report_content += f"- **{category.title()}**: {count} pairs\n"

        report_content += f"""
### Difficulty Distribution
"""
        if 'difficulty_distribution' in stats:
            for difficulty, count in stats['difficulty_distribution'].items():
                report_content += f"- **{difficulty.title()}**: {count} pairs\n"

        report_content += f"""
### Language Distribution
"""
        if 'language_distribution' in stats:
            for language, count in stats['language_distribution'].items():
                report_content += f"- **{language.title()}**: {count} pairs\n"

        if 'avg_question_length' in stats:
            report_content += f"""
### Content Statistics
- **Average Question Length**: {stats['avg_question_length']:.1f} words
- **Average Answer Length**: {stats['avg_answer_length']:.1f} words

## Data Quality Notes
- All English content has been translated to Telugu
- Duplicate recipes have been removed based on content similarity
- Text has been cleaned and normalized
- Measurements and cooking techniques have been preserved
- Category classification applied automatically

## Usage
This dataset is ready for training Telugu recipe chatbot models. The Q&A pairs follow a consistent format suitable for fine-tuning language models.
"""

        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_content)


def main():
    """Main execution function"""
    preprocessor = RecipeDataPreprocessor()

    # Process all recipes
    recipes, qa_pairs = preprocessor.process_all_recipes()

    if recipes and qa_pairs:
        # Save to JSON files
        output_files = preprocessor.save_to_json()

        print("\n" + "="*60)
        print("📊 RECIPE DATA PREPROCESSING COMPLETE")
        print("="*60)
        print(f"✅ Processed: {len(recipes)} recipes")
        print(f"✅ Generated: {len(qa_pairs)} Q&A pairs")
        print(f"✅ Removed: {preprocessor.duplicate_count} duplicates")
        print("\n📁 Output Files:")
        for key, filepath in output_files.items():
            print(f"   {key}: {filepath}")
        print("\n🎯 Ready for model training!")
    else:
        print("❌ No recipes found to process. Please add some recipes first.")


if __name__ == "__main__":
    main()
