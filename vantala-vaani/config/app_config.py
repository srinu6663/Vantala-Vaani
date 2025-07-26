# Configuration file for Recipe Collection App

# Application Settings
APP_TITLE = "వంటల వాణి - Recipe Collection"
APP_ICON = "🍛"
CSV_FILENAME = "recipes.csv"

# UI Settings
FORM_BACKGROUND_COLOR = "#f0f2f6"
SUCCESS_COLOR = "#d4edda"
SUCCESS_TEXT_COLOR = "#155724"

# Language Settings
SUPPORTED_LANGUAGES = ["English", "తెలుగు (Telugu)"]
DEFAULT_LANGUAGE = "English"

# Telugu Unicode Range
TELUGU_UNICODE_START = 0x0C00
TELUGU_UNICODE_END = 0x0C7F

# Translation Settings
TRANSLATION_SOURCE = "en"
TRANSLATION_TARGET = "te"

# CSV Headers
CSV_HEADERS = [
    'Timestamp',
    'Recipe Name (Telugu)',
    'Ingredients (Telugu)',
    'Steps (Telugu)',
    'Original Language',
    'Original Recipe Name',
    'Original Ingredients',
    'Original Steps'
]

# Sample placeholders
TELUGU_PLACEHOLDERS = {
    'recipe_name': "ఉదా: కోడి కర్రీ, పులిహోర, దోసె...",
    'ingredients': "ఉదా: అన్నం - 2 కప్పులు\nఉల్లిపాయలు - 2\nమిరపకాయలు - 3...",
    'steps': "దశలవారీగా వంట విధానాన్ని రాయండి..."
}

ENGLISH_PLACEHOLDERS = {
    'recipe_name': "e.g: Chicken Curry, Pulihora, Dosa...",
    'ingredients': "e.g: Rice - 2 cups\nOnions - 2\nGreen chilies - 3...",
    'steps': "Write step-by-step cooking instructions..."
}
