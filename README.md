# 🍽️ Food Recipe Collection App

A Streamlit-based application for collecting traditional food recipes in text, audio, and video formats to build an Indic language corpus.

## 🎯 Purpose

This application helps collect traditional recipes and culinary knowledge for Indic languages by providing an easy-to-use interface for submitting recipes in multiple formats. All submissions are stored in the CorpusApp backend under the Food category.

## ✨ Features

- **Multi-format Recipe Submission**: Text, audio (.mp3, .wav, .m4a), and video (.mp4, .mov, .avi)
- **CorpusApp Integration**: Direct submission to CorpusApp API with authentication
- **Metadata Collection**: Recipe name, cuisine type, cooking time, and difficulty level
- **File Validation**: Automatic validation of file types and sizes
- **Submission Logging**: Track successful and failed submissions
- **Indic Language Support**: Full support for Indic language text input
- **User-friendly Interface**: Simple radio button selection and drag-drop file uploads

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Access to CorpusApp API with valid bearer token

### Installation

1. **Clone or download the application files**

2. **Install dependencies**:
   ```bash
   pip install streamlit requests python-dotenv
   ```

3. **Set up environment variables**:
   
   Create a `.env` file in the project root:
   ```env
   ACCESS_TOKEN=your_bearer_token_here
   CATEGORY_ID=833299f6-ff1c-4fde-804f-6d3b3877c76e
   API_BASE=https://your-corpus-app-domain.com
   ```

4. **Run the application**:
   ```bash
   streamlit run app.py
   ```

5. **Access the app**:
   Open your browser and navigate to `http://localhost:5000`

## 📁 Project Structure

