# Recipe Data Preprocessing Pipeline

## 📋 Overview

This module provides a complete data preprocessing pipeline for the **వంటల వాణి (Recipe Collection)** project. It reads recipe submissions from CSV, cleans and deduplicates the data, detects languages, translates content to Telugu, and converts everything into Q&A chat pairs suitable for machine learning model training.

## 🚀 Features

### ✅ **Core Functionality**

- **CSV Reading**: Load recipe data from the collection interface
- **Deduplication**: Remove duplicate recipes based on content similarity
- **Text Cleaning**: Normalize Unicode, fix formatting, clean whitespace
- **Language Detection**: Automatically detect Telugu vs English content
- **Translation**: Translate English content to Telugu using Google Translate
- **Q&A Generation**: Convert recipes into question-answer chat pairs
- **Multiple Output Formats**: Standard JSON, HuggingFace, OpenAI formats

### ✅ **Data Quality Features**

- **Input Validation**: Verify recipe completeness and quality
- **Content Analysis**: Extract metadata like difficulty, cooking time, category
- **Statistics Generation**: Comprehensive dataset statistics
- **Error Handling**: Graceful handling of translation and processing errors
- **Progress Logging**: Detailed logging of processing steps

### ✅ **Advanced Processing**

- **Category Classification**: Automatic recipe categorization (curry, rice, snacks, etc.)
- **Difficulty Estimation**: Analyze complexity based on ingredients and steps
- **Time Estimation**: Estimate cooking time from recipe content
- **Measurement Detection**: Identify recipes with proper measurements
- **Multiple Question Variations**: Generate diverse question formats per recipe

## 📁 File Structure

```
vantala-vaani/
├── data_preprocessor.py      # Main preprocessing class
├── preprocess_cli.py         # Command-line interface
├── preprocessing_config.py   # Configuration settings
├── recipes.csv              # Input data (from collection app)
├── processed_data/          # Output directory
│   ├── processed_recipes_*.json      # Cleaned recipe data
│   ├── recipe_qa_pairs_*.json       # Q&A pairs for training
│   ├── training_dataset_*.json      # Complete training dataset
│   └── processing_report_*.md       # Processing statistics
└── hf_data/                 # HuggingFace format exports
    └── recipe_dataset_hf_*.jsonl    # HF-compatible format
```

## 🛠️ Usage

### Method 1: Direct Python Execution

```bash
# Run the main preprocessor
python data_preprocessor.py

# Output: Processes recipes.csv and creates training data
```

### Method 2: Command Line Interface

```bash
# Show dataset statistics only
python preprocess_cli.py --stats-only

# Process with standard format
python preprocess_cli.py --input recipes.csv --output training_data

# Generate HuggingFace compatible format
python preprocess_cli.py --format huggingface --output hf_data

# Generate OpenAI fine-tuning format
python preprocess_cli.py --format openai --output openai_data

# Verbose processing with detailed logs
python preprocess_cli.py --verbose
```

### Method 3: Import as Module

```python
from data_preprocessor import RecipeDataPreprocessor

# Initialize preprocessor
preprocessor = RecipeDataPreprocessor("recipes.csv")

# Process all recipes
recipes, qa_pairs = preprocessor.process_all_recipes()

# Save in different formats
output_files = preprocessor.save_to_json("output_directory")
```

## 📊 Output Formats

### 1. **Standard JSON Format**

```json
{
  "id": "1fe80f92_0",
  "recipe_id": "1fe80f92",
  "question": "How do I make కాశ్మీరీ స్టైల్ పన్నీర్ మసాలా రెసిపీ?",
  "answer": "📝 కావలసిన వస్తువులు:\n...\n👩‍🍳 తయారీ విధానం:\n...",
  "recipe_name": "కాశ్మీరీ స్టైల్ పన్నీర్ మసాలా రెసిపీ",
  "language": "english",
  "category": "curry",
  "difficulty": "medium",
  "cooking_time": "medium",
  "metadata": { ... }
}
```

### 2. **HuggingFace Format (JSONL)**

```json
{
  "input": "How do I make కాశ్మీరీ స్టైల్ పన్నీర్ మసాలా రెసిపీ?",
  "output": "📝 కావలసిన వస్తువులు:\n...",
  "instruction": "Answer the cooking question in Telugu",
  "category": "curry",
  "difficulty": "medium",
  "language": "english"
}
```

### 3. **OpenAI Format (JSONL)**

```json
{
  "messages": [
    {
      "role": "user",
      "content": "How do I make కాశ్మీరీ స్టైల్ పన్నీర్ మసాలా రెసిపీ?"
    },
    { "role": "assistant", "content": "📝 కావలసిన వస్తువులు:\n..." }
  ]
}
```

## 🔧 Processing Pipeline

### Step 1: **Data Loading**

- Read CSV file with recipe submissions
- Validate file structure and content
- Log loading statistics

### Step 2: **Deduplication**

- Generate content hashes for each recipe
- Compare recipe names and ingredients
- Remove exact and near-duplicate entries

### Step 3: **Text Cleaning**

- Normalize Unicode characters (NFKC)
- Fix punctuation spacing
- Clean extra whitespace
- Standardize measurement formats

### Step 4: **Language Processing**

- Detect Telugu vs English content using Unicode ranges
- Translate English content to Telugu
- Preserve original text alongside translations
- Handle translation errors gracefully

### Step 5: **Content Analysis**

- **Category Classification**: Based on recipe name keywords

  - Rice dishes (అన్నం, rice, biryani)
  - Curries (కర్రీ, curry, gravy)
  - Snacks (స్నాక్స్, tiffin, dosa)
  - Sweets (మిఠాయి, laddu, halwa)
  - And more...

- **Difficulty Estimation**: Based on complexity factors

  - Ingredient count
  - Number of cooking steps
  - Advanced techniques (frying, grinding, etc.)

- **Time Estimation**: From recipe content
  - Short: Quick preparations
  - Medium: Standard cooking time
  - Long: Extended cooking processes

### Step 6: **Q&A Generation**

- Generate multiple question variations per recipe
- Create comprehensive Telugu answers
- Include ingredients, steps, and cooking tips
- Add emoji formatting for better readability

### Step 7: **Output Generation**

- Save processed recipes as structured JSON
- Generate training-ready Q&A pairs
- Create comprehensive training dataset
- Generate processing statistics and reports

## 📈 Quality Metrics

### Data Quality Checks

- **Completeness**: All required fields present
- **Length Validation**: Minimum content thresholds
- **Language Consistency**: Proper Telugu translations
- **Measurement Detection**: Recipes include proper quantities
- **Duplicate Detection**: Content similarity analysis

### Output Statistics

- Total recipes processed
- Q&A pairs generated
- Category distribution
- Language distribution
- Average content lengths
- Processing time metrics

## 🎯 Example Results

From 1 recipe input, the system generates:

- ✅ **12 Q&A pairs** (8 English questions, 4 Telugu questions)
- ✅ **1 cleaned recipe** with metadata
- ✅ **Auto-categorization** (curry category detected)
- ✅ **Difficulty assessment** (medium difficulty)
- ✅ **Multiple output formats** for different ML frameworks

## 🔍 Configuration Options

The system supports extensive customization through `preprocessing_config.py`:

- **Question Templates**: Customize Q&A generation patterns
- **Category Keywords**: Define recipe classification rules
- **Quality Thresholds**: Set minimum content requirements
- **Translation Settings**: Configure translation behavior
- **Output Formats**: Specify export options

## 🚀 Integration with ML Training

The generated datasets are ready for:

### 1. **Fine-tuning Language Models**

- Use HuggingFace format for transformer models
- OpenAI format for GPT fine-tuning
- Standard format for custom training pipelines

### 2. **Chatbot Development**

- Q&A pairs for conversational AI
- Recipe-specific intent classification
- Multi-language support (Telugu + English)

### 3. **Search and Recommendation**

- Recipe embeddings generation
- Similarity-based recipe suggestions
- Category-based filtering

## 📊 Sample Processing Report

```
Recipe Data Preprocessing Report
Generated: 2025-07-26 20:10:00

Summary:
- Total Recipes Processed: 1
- Total Q&A Pairs Generated: 12
- Duplicates Removed: 0

Dataset Statistics:
Recipe Categories:
- Curry: 12 pairs

Difficulty Distribution:
- Medium: 12 pairs

Language Distribution:
- English: 8 pairs
- Telugu: 4 pairs

Content Statistics:
- Average Question Length: 9.0 words
- Average Answer Length: 307.0 words
```

## 🎯 Next Steps

This preprocessing pipeline sets the foundation for:

1. **Model Training**: Use generated Q&A pairs to train Telugu recipe chatbots
2. **Data Augmentation**: Add more recipes to increase dataset size
3. **Quality Improvement**: Refine translation and categorization
4. **Advanced Features**: Add image processing, nutrition analysis, etc.

The system is designed to scale with more recipe data and can be easily extended with additional processing features.
