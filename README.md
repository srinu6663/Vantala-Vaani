# వంటల వాణి (Vantala Vaani) - Recipe Collection System

A bilingual Telugu-English recipe collection and machine learning preprocessing system.

## 🚀 Quick Start

1. **Setup** (Windows):

   ```bash
   scripts\setup.bat
   ```

2. **Run Application**:
   ```bash
   python main.py
   ```

## 📁 Project Structure

```
vantala-vaani/
├── main.py                    # 🎯 Main application launcher
├── src/                       # 📦 Source code
│   ├── core/                  # 🔧 Core application modules
│   │   ├── __init__.py
│   │   ├── recipe_collection.py  # Streamlit web interface
│   │   └── utils.py              # Shared utilities
│   ├── preprocessing/         # 🔄 Data processing pipeline
│   │   ├── __init__.py
│   │   ├── data_preprocessor.py  # Main preprocessing logic
│   │   └── preprocess_cli.py     # CLI interface
│   └── __init__.py
├── config/                    # ⚙️ Configuration files
│   ├── project_config.py     # Project-wide settings
│   ├── app_config.py         # Application configuration
│   └── preprocessing_config.py # Preprocessing settings
├── data/                      # 📊 Data files
│   ├── recipes.csv           # Main recipe database
│   ├── processed/            # Processed datasets
│   └── raw/                  # Raw data files
├── scripts/                   # 🛠️ Setup and utility scripts
│   └── setup.bat            # Windows setup script
├── tests/                     # 🧪 Test files
│   └── test_setup.py        # Setup validation tests
├── docs/                      # 📚 Documentation
│   └── DATA_PREPROCESSING_GUIDE.md
└── requirements.txt          # 📋 Python dependencies
```

│ ├── preprocessing_config.yaml # Processing settings
│ └── requirements.txt # Python dependencies
├── data/ # 📊 Data storage
│ ├── raw/ # Original recipe submissions
│ └── processed/ # ML-ready training data
├── tests/ # 🧪 Test files
├── scripts/ # 🔨 Utility scripts
└── docs/ # 📚 Documentation

````

## 🛠️ Features

### Recipe Collection
- 📝 Bilingual Telugu-English web interface
- 🔄 Automatic translation (English → Telugu)
- 💾 CSV storage for submissions
- 🎨 Beautiful Streamlit UI

### Data Preprocessing
- 🔍 Intelligent deduplication
- 🌐 Language detection and translation
- 🤖 Q&A pair generation for ML training
- 📈 Multiple export formats (JSON, HuggingFace, OpenAI)

### ML Training Ready
- 🎯 Question-Answer pairs in Telugu
- 📊 Categorized recipes (వంటకం రకం)
- ⏱️ Difficulty and time estimates
- 📄 Multiple formats for different training frameworks

## 📱 Usage

### Interactive Menu
```bash
python main.py
````

Options:

1. **Recipe Collection** - Start Streamlit web interface
2. **Data Preprocessing** - Process raw recipes into ML format
3. **Dataset Statistics** - View collection statistics
4. **System Tests** - Verify installation

### Direct Commands

```bash
# Web interface only
streamlit run src/core/recipe_collection.py

# CLI preprocessing
python src/preprocessing/preprocess_cli.py --input data/raw/recipes.csv
```

```
vantala-vaani/
├── recipe_collection.py    # Main Streamlit application
├── requirements.txt        # Python dependencies
├── recipes.csv            # Generated CSV file with saved recipes
└── README.md              # This file
```

## CSV Output Format

The generated `recipes.csv` contains the following columns:

- Timestamp
- Recipe Name (Telugu)
- Ingredients (Telugu)
- Steps (Telugu)
- Original Language
- Original Recipe Name
- Original Ingredients
- Original Steps

## Technical Features

- **Language Detection**: Uses regex pattern matching for Telugu script
- **Translation**: Google Translate API for English to Telugu translation
- **Unicode Support**: Full support for Telugu Unicode characters
- **Error Handling**: Graceful handling of translation errors
- **Data Persistence**: CSV format for easy data export and analysis

## Troubleshooting

### Translation Issues

- Ensure internet connection for Google Translate API
- Check if `googletrans` package is properly installed

### Telugu Font Issues

- The app includes CSS for Telugu font support
- Ensure your browser supports Unicode Telugu fonts

### CSV File Issues

- Check file permissions in the application directory
- Ensure write access to create `recipes.csv`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is open source and available under the MIT License.
