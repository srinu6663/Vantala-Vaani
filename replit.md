# Food Recipe Collection App

## Overview

This is a Streamlit-based web application designed to collect traditional food recipes in multiple formats (text, audio, and video) for building an Indic language corpus. The app serves as a data collection frontend that integrates with the CorpusApp backend API to store and manage recipe submissions. Users can submit recipes with metadata like cuisine type, cooking time, and difficulty level, while the system handles authentication, file validation, and submission tracking.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit-based single-page application with form-based user interface
- **User Interface**: Radio button format selection (Text/Audio/Video) with conditional input fields
- **File Handling**: Drag-and-drop file uploads with client-side validation for file types and sizes
- **Form Management**: Single form submission pattern with real-time validation feedback

### Backend Integration
- **API Client Architecture**: Service-oriented design with separate concerns for authentication and record management
- **Authentication Service**: Bearer token-based authentication with environment variable configuration
- **Record Service**: RESTful API client for submitting recipes to CorpusApp backend
- **File Upload Strategy**: Multipart form data handling for audio/video files, JSON payload for text content

### Data Storage Strategy
- **Primary Storage**: External CorpusApp API serving as the main data repository
- **Local Logging**: JSON-based submission tracking for monitoring and debugging purposes
- **Metadata Handling**: Structured metadata collection including recipe name, cuisine type, cooking time, and difficulty level

### File Management
- **Validation Layer**: Client-side file type and size validation before submission
- **Supported Formats**: Audio (mp3, wav, m4a) up to 50MB, Video (mp4, mov, avi) up to 100MB
- **Processing**: Direct file streaming to API without local storage persistence

### Configuration Management
- **Environment Variables**: Centralized configuration using .env files for API credentials and endpoints
- **Service Configuration**: Modular configuration with separate concerns for different service components

### Error Handling and Logging
- **Submission Tracking**: Local JSON-based logging system for successful and failed submissions
- **User Feedback**: Real-time error messages and success notifications through Streamlit interface
- **Authentication Validation**: Startup authentication check with graceful failure handling

## External Dependencies

### Core Application Stack
- **Streamlit**: Web application framework for the user interface
- **Requests**: HTTP client library for API communication
- **Python-dotenv**: Environment variable management

### External APIs
- **CorpusApp API**: Primary backend service for recipe data storage and management
  - Authentication via Bearer tokens
  - RESTful endpoints for record creation and retrieval
  - Category-based data organization (Food category: 833299f6-ff1c-4fde-804f-6d3b3877c76e)

### Development and Deployment
- **Python 3.8+**: Runtime environment requirement
- **Environment Configuration**: Requires ACCESS_TOKEN, CATEGORY_ID, and API_BASE configuration

### Data Format Dependencies
- **Audio Codecs**: Support for MP3, WAV, and M4A audio formats
- **Video Codecs**: Support for MP4, MOV, and AVI video formats
- **Text Encoding**: Unicode support for Indic language text input