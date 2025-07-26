#!/usr/bin/env python3
"""
Recipe Data Preprocessing CLI
Quick interface for processing recipe data and generating training datasets.
"""

import argparse
import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.preprocessing.data_preprocessor import RecipeDataPreprocessor

def main():
    parser = argparse.ArgumentParser(
        description="Process recipe data for machine learning training",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python preprocess_cli.py --input recipes.csv --output training_data
    python preprocess_cli.py --input recipes.csv --format huggingface
    python preprocess_cli.py --stats-only recipes.csv
        """
    )

    parser.add_argument(
        "--input", "-i",
        default="recipes.csv",
        help="Input CSV file with recipes (default: recipes.csv)"
    )

    parser.add_argument(
        "--output", "-o",
        default="processed_data",
        help="Output directory for processed files (default: processed_data)"
    )

    parser.add_argument(
        "--format",
        choices=["standard", "huggingface", "openai"],
        default="standard",
        help="Output format for training data (default: standard)"
    )

    parser.add_argument(
        "--stats-only",
        action="store_true",
        help="Only show statistics without processing"
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )

    args = parser.parse_args()

    # Check if input file exists
    if not os.path.exists(args.input):
        print(f"❌ Error: Input file '{args.input}' not found.")
        print("💡 Tip: Run the recipe collection app first to generate recipe data.")
        sys.exit(1)

    print("🍛 Recipe Data Preprocessor")
    print("=" * 50)

    # Initialize preprocessor
    preprocessor = RecipeDataPreprocessor(args.input)

    if args.stats_only:
        # Just show statistics
        df = preprocessor.load_recipes()
        if not df.empty:
            print(f"📊 Dataset Overview:")
            print(f"   Total records: {len(df)}")
            print(f"   Date range: {df['Timestamp'].min()} to {df['Timestamp'].max()}")

            # Language distribution
            lang_dist = df['Original Language'].value_counts()
            print(f"   Language distribution:")
            for lang, count in lang_dist.items():
                print(f"     {lang}: {count}")
        else:
            print("❌ No data found in the CSV file.")
        return

    # Process recipes
    print(f"📁 Input: {args.input}")
    print(f"📁 Output: {args.output}")
    print(f"🎯 Format: {args.format}")
    print()

    try:
        recipes, qa_pairs = preprocessor.process_all_recipes()

        if recipes and qa_pairs:
            # Save data based on format
            if args.format == "huggingface":
                output_files = save_huggingface_format(preprocessor, args.output)
            elif args.format == "openai":
                output_files = save_openai_format(preprocessor, args.output)
            else:
                output_files = preprocessor.save_to_json(args.output)

            print(f"\n✅ SUCCESS: Processed {len(recipes)} recipes into {len(qa_pairs)} Q&A pairs")
            print(f"📂 Files saved in: {args.output}")

            if args.verbose:
                print("\n📋 Generated files:")
                for file_type, filepath in output_files.items():
                    size = Path(filepath).stat().st_size / 1024  # KB
                    print(f"   {file_type}: {filepath} ({size:.1f} KB)")
        else:
            print("❌ No valid recipes found to process.")

    except Exception as e:
        print(f"❌ Error during processing: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

def save_huggingface_format(preprocessor, output_dir):
    """Save in HuggingFace datasets format"""
    import json
    from datetime import datetime

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Convert to HuggingFace format
    hf_data = []
    for pair in preprocessor.chat_pairs:
        hf_data.append({
            "input": pair["question"],
            "output": pair["answer"],
            "instruction": "Answer the cooking question in Telugu",
            "category": pair["category"],
            "difficulty": pair["difficulty"],
            "language": pair["language"]
        })

    # Save as JSONL for easy loading
    hf_file = os.path.join(output_dir, f"recipe_dataset_hf_{timestamp}.jsonl")
    with open(hf_file, 'w', encoding='utf-8') as f:
        for item in hf_data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')

    return {"huggingface_dataset": hf_file}

def save_openai_format(preprocessor, output_dir):
    """Save in OpenAI fine-tuning format"""
    import json
    from datetime import datetime

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Convert to OpenAI format
    openai_data = []
    for pair in preprocessor.chat_pairs:
        openai_data.append({
            "messages": [
                {"role": "user", "content": pair["question"]},
                {"role": "assistant", "content": pair["answer"]}
            ]
        })

    # Save as JSONL
    openai_file = os.path.join(output_dir, f"recipe_dataset_openai_{timestamp}.jsonl")
    with open(openai_file, 'w', encoding='utf-8') as f:
        for item in openai_data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')

    return {"openai_dataset": openai_file}

if __name__ == "__main__":
    main()
