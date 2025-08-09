# Vantala Vaani (Food) — Recipe Uploader to Swecha CorpusApp

A minimal, simple Streamlit application for uploading food recipes to Swecha CorpusApp via audio files or text input.

## Features

- **Text Recipe Upload**: Submit recipes with title, ingredients, cooking steps, and submitter name
- **Audio Recipe Upload**: Upload audio recordings with title and optional description
- **Smart Ingredients Parser**: Automatically parses ingredients from text format
- **File Validation**: Validates audio file types and sizes before upload
- **Clean UI**: Simple, intuitive interface with real-time previews
- **Error Handling**: Comprehensive error messages and validation
- **Endpoint Discovery**: Automatically discovers available API endpoints
- **Multi-endpoint Support**: Tries multiple common API patterns for robust connectivity

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Copy the example environment file and fill in your Swecha CorpusApp details:

```bash
copy .env.example .env
```

Edit `.env` with your actual values:

```env
CORPUSAPP_BASE_URL=https://api.corpus.swecha.org/api/v1
CORPUSAPP_TOKEN=your_swecha_api_token_here
CATEGORY_ID_FOOD=833299f6-ff1c-4fde-804f-6d3b3877c76e
ALLOWED_AUDIO_TYPES=mp3,wav,m4a,aac,ogg,flac
MAX_UPLOAD_MB=50
```

### 3. Run the Application

```bash
streamlit run app.py
```

The app will be available at `http://localhost:8501`

## 🎯 **Integration Status: Ready for Swecha CorpusApp!**

✅ **Configured for Official Swecha API**

- **Base URL**: `https://api.corpus.swecha.org/api/v1` ✅
- **Documentation**: Available at https://api.corpus.swecha.org/docs
- **Food Category ID**: `833299f6-ff1c-4fde-804f-6d3b3877c76e` ✅ Confirmed

**🔑 Only Missing: Your API Token**

1. **Create account** at https://corpus.swecha.org/
2. **Generate API token** from your account settings
3. **Update .env**: `CORPUSAPP_TOKEN=your_actual_token_here`
4. **Start uploading recipes!** 🍽️

**✨ Ready Features:**

- Smart endpoint discovery
- Automatic audio/text recipe upload
- Telugu content support with ingredients parsing
- Robust error handling and validation

## Usage

### Text Recipe Submission

1. Go to the "📝 Text Recipe" tab
2. Enter a recipe title (required)
3. Optionally add ingredients (one per line, format: "ingredient — quantity")
4. Optionally add cooking steps
5. Optionally add your name
6. Click "Submit Text Recipe"

**Ingredients Format Example:**

```
Chicken — 500g
Basmati Rice — 2 cups
Onions — 2 large
Salt — to taste
```

### Audio Recipe Submission

1. Go to the "🎤 Audio Recipe" tab
2. Enter a recipe title (required)
3. Upload an audio file (required)
4. Optionally add a description
5. Optionally add your name
6. Preview the audio to ensure it uploaded correctly
7. Click "Submit Audio Recipe"

**Supported Audio Formats:** MP3, WAV, M4A, AAC, OGG, FLAC

## Project Structure

```
Food/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .streamlit/
│   └── config.toml       # Streamlit configuration
├── config/
│   └── settings.py       # Application settings
├── services/
│   ├── corpus_client.py  # CorpusApp API client
│   └── parsers.py        # Data parsing utilities
└── tests/                # Test files (optional)
    ├── test_parsers.py
    └── test_corpus_client.py
```

## API Integration

The app supports two CorpusApp upload patterns:

1. **Direct Upload**: Direct file upload to `/v1/media` endpoint
2. **Presigned Upload**: Two-step process with presigned URLs

The client automatically detects and uses the appropriate method.

## Configuration

### Streamlit Settings

- **Upload Limit**: 400MB (configurable in `.streamlit/config.toml`)
- **Theme**: Custom color scheme optimized for food content

### Environment Variables

| Variable              | Description                      | Default                                |
| --------------------- | -------------------------------- | -------------------------------------- |
| `CORPUSAPP_BASE_URL`  | CorpusApp API base URL           | Required                               |
| `CORPUSAPP_TOKEN`     | API authentication token         | Required                               |
| `CATEGORY_ID_FOOD`    | Food category ID in CorpusApp    | `833299f6-ff1c-4fde-804f-6d3b3877c76e` |
| `ALLOWED_AUDIO_TYPES` | Comma-separated audio file types | `mp3,wav,m4a,aac,ogg,flac`             |
| `MAX_UPLOAD_MB`       | Maximum file size in MB          | `50`                                   |

## Testing

Run the tests (if implemented):

```bash
pytest tests/
```

## Error Handling

The application provides clear error messages for:

- Missing or invalid configuration
- Network connectivity issues
- Authentication failures
- File validation errors
- API rate limits and server errors

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the MIT License.
