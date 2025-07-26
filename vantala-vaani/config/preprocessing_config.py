# Data Preprocessing Configuration

# File paths
CSV_INPUT_FILE = "recipes.csv"
OUTPUT_DIRECTORY = "processed_data"

# Processing options
REMOVE_DUPLICATES = True
CLEAN_TEXT = True
TRANSLATE_TO_TELUGU = True
GENERATE_QA_PAIRS = True

# Quality filters
MIN_RECIPE_NAME_LENGTH = 3
MIN_INGREDIENTS_LENGTH = 10
MIN_STEPS_LENGTH = 20
MAX_RECIPE_LENGTH = 5000  # characters

# Q&A generation settings
QUESTIONS_PER_RECIPE = 12  # Number of question variations per recipe
INCLUDE_ENGLISH_QUESTIONS = True
INCLUDE_TELUGU_QUESTIONS = True

# Translation settings
TRANSLATION_BATCH_SIZE = 10
TRANSLATION_TIMEOUT = 30  # seconds
FALLBACK_ON_TRANSLATION_FAILURE = True

# Output formats
SAVE_PROCESSED_RECIPES = True
SAVE_QA_PAIRS = True
SAVE_TRAINING_DATASET = True
SAVE_STATISTICS = True
SAVE_PROCESSING_REPORT = True

# Question templates for Q&A generation
ENGLISH_QUESTION_TEMPLATES = [
    "How do I make {recipe_name}?",
    "What's the recipe for {recipe_name}?",
    "Can you tell me how to prepare {recipe_name}?",
    "I want to cook {recipe_name}. How?",
    "Give me the recipe for {recipe_name}",
    "How to cook {recipe_name}?",
    "What are the steps to make {recipe_name}?",
    "Can you provide the {recipe_name} recipe?",
    "Show me how to make {recipe_name}",
    "I need the {recipe_name} recipe"
]

TELUGU_QUESTION_TEMPLATES = [
    "{recipe_name} ఎలా చేయాలి?",
    "{recipe_name} రెసిపీ చెప్పండి",
    "{recipe_name} ఎలా వండాలి?",
    "{recipe_name} తయారీ విధానం చెప్పండి",
    "{recipe_name} ఎలా తయారు చేస్తారు?",
    "{recipe_name} వంట విధానం ఏమిటి?",
    "{recipe_name} చేయడానికి ఏమి కావాలి?",
    "{recipe_name} వండే విధానం చెప్పండి"
]

# Category keywords for automatic classification
RECIPE_CATEGORIES = {
    'rice': {
        'telugu': ['అన్నం', 'రైస్', 'పులిహోర', 'బిర్యానీ', 'చిత్రాన్నం'],
        'english': ['rice', 'biryani', 'pulihora', 'fried rice', 'pulao']
    },
    'curry': {
        'telugu': ['కర్రీ', 'కూర', 'కుర', 'గ్రేవీ', 'మసాలా'],
        'english': ['curry', 'gravy', 'masala', 'sauce']
    },
    'snacks': {
        'telugu': ['స్నాక్స్', 'టిఫిన్', 'దోసె', 'ఇడ్లీ', 'వడ', 'అప్పడం'],
        'english': ['snacks', 'tiffin', 'dosa', 'idli', 'vada', 'upma']
    },
    'sweets': {
        'telugu': ['మిఠాయి', 'లడ్డు', 'హల్వా', 'పాయసం', 'జీలేబీ', 'గుజియా'],
        'english': ['sweet', 'laddu', 'halwa', 'payasam', 'jalebi', 'dessert']
    },
    'dal': {
        'telugu': ['పప్పు', 'సాంబార్', 'రసం', 'దాల్'],
        'english': ['dal', 'sambar', 'rasam', 'lentil']
    },
    'vegetables': {
        'telugu': ['కూరగాయలు', 'కరీ', 'పల్య', 'వేపుడు'],
        'english': ['vegetables', 'sabzi', 'stir fry', 'poriyal']
    },
    'bread': {
        'telugu': ['రొట్టె', 'చపాతీ', 'నాన్', 'పూరీ', 'పరోటా'],
        'english': ['bread', 'chapati', 'naan', 'poori', 'paratha']
    },
    'non_veg': {
        'telugu': ['కోడి', 'చికెన్', 'మటన్', 'చేప', 'ఈగ', 'మాంసం'],
        'english': ['chicken', 'mutton', 'fish', 'egg', 'meat', 'non-veg']
    },
    'beverages': {
        'telugu': ['పానీయాలు', 'టీ', 'కాఫీ', 'జూస్', 'లస్సీ'],
        'english': ['drinks', 'tea', 'coffee', 'juice', 'lassi', 'beverage']
    }
}

# Difficulty estimation keywords
DIFFICULTY_KEYWORDS = {
    'easy': {
        'telugu': ['సులభం', 'తక్కువ సమయం', 'సింపుల్'],
        'english': ['easy', 'simple', 'quick', 'basic']
    },
    'medium': {
        'telugu': ['మధ్యస్థం', 'కొంచెం కష్టం'],
        'english': ['medium', 'moderate', 'intermediate']
    },
    'hard': {
        'telugu': ['కష్టం', 'చాలా సమయం', 'ఎక్కువ దశలు'],
        'english': ['hard', 'difficult', 'complex', 'advanced', 'time consuming']
    }
}

# Text cleaning patterns
CLEANING_PATTERNS = {
    'extra_whitespace': r'\s+',
    'leading_trailing_space': r'^\s+|\s+$',
    'punctuation_spacing': r'([.!?])\s*([a-zA-Z\u0C00-\u0C7F])',
    'telugu_punctuation': r'([.!?])\s*([అ-హ])',
    'measurement_normalization': r'(\d+)\s*(కప్పు|టీస్పూన్|గ్రాము|కిలో|లీటర్)',
    'english_measurement_normalization': r'(\d+)\s*(cup|tsp|tbsp|gram|kg|liter|ml)'
}

# Validation rules
VALIDATION_RULES = {
    'recipe_name': {
        'min_length': 3,
        'max_length': 100,
        'required': True
    },
    'ingredients': {
        'min_length': 10,
        'max_length': 2000,
        'required': True
    },
    'steps': {
        'min_length': 20,
        'max_length': 3000,
        'required': True
    }
}

# Output format settings
OUTPUT_FORMATS = {
    'standard': {
        'extension': 'json',
        'indent': 2,
        'ensure_ascii': False
    },
    'huggingface': {
        'extension': 'jsonl',
        'format': 'instruction_following'
    },
    'openai': {
        'extension': 'jsonl',
        'format': 'chat_completion'
    }
}

# Logging configuration
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = "preprocessing.log"
