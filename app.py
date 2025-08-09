import streamlit as st
import time
from typing import Optional
from config.settings import settings
from services.corpus_client import CorpusClient, CorpusAppError
from services.parsers import parse_ingredients, validate_audio_file, format_file_size

# Page configuration
st.set_page_config(
    page_title="Vantala Vaani - Food Recipe Uploader",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0 2rem 0;
        border-bottom: 2px solid #FF6B35;
        margin-bottom: 2rem;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        margin: 1rem 0;
    }
    .error-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def init_session_state():
    """Initialize session state variables"""
    if 'text_form_submitted' not in st.session_state:
        st.session_state.text_form_submitted = False
    if 'audio_form_submitted' not in st.session_state:
        st.session_state.audio_form_submitted = False
    if 'last_success_id' not in st.session_state:
        st.session_state.last_success_id = None

def clear_text_form():
    """Clear text form fields"""
    for key in ['text_title', 'text_ingredients', 'text_steps', 'text_user_name']:
        if key in st.session_state:
            del st.session_state[key]
    st.session_state.text_form_submitted = False

def clear_audio_form():
    """Clear audio form fields"""
    for key in ['audio_title', 'audio_description', 'audio_user_name']:
        if key in st.session_state:
            del st.session_state[key]
    st.session_state.audio_form_submitted = False

def check_configuration():
    """Check if the app is properly configured"""
    if not settings.validate():
        missing_vars = settings.get_missing_vars()
        st.error(f"""
        **Configuration Error**: Missing required environment variables: {', '.join(missing_vars)}

        Please create a `.env` file with the following variables:
        ```
        CORPUSAPP_BASE_URL=https://your-corpusapp-domain.com/api
        CORPUSAPP_TOKEN=your_api_token_here
        ```

        You can copy `.env.example` as a starting point.
        """)
        return False
    return True

def submit_text_recipe(title: str, ingredients: str, steps: str, user_name: str):
    """Submit text recipe to CorpusApp"""
    try:
        # Parse ingredients
        parsed_ingredients = parse_ingredients(ingredients) if ingredients.strip() else []

        # Build content text
        content_parts = []
        if steps.strip():
            content_parts.append(f"Instructions:\n{steps.strip()}")

        if parsed_ingredients:
            content_parts.append(f"Ingredients:\n" + "\n".join([f"• {ing}" for ing in parsed_ingredients]))

        if user_name.strip():
            content_parts.append(f"Submitted by: {user_name.strip()}")

        content_text = "\n\n".join(content_parts)

        # Build payload in the correct format for Swecha CorpusApp
        payload = {
            "title": title.strip(),
            "content": content_text,
            "category_id": settings.CATEGORY_ID_FOOD,
            "media_type": "text"
        }

        # Submit to CorpusApp
        client = CorpusClient()

        with st.spinner("Submitting recipe to CorpusApp..."):
            result = client.create_content(payload)

        # Success
        content_id = result.get('id', 'Unknown')
        st.session_state.last_success_id = content_id

        st.markdown(f"""
        <div class="success-box">
            <h4>✅ Recipe Submitted Successfully!</h4>
            <p><strong>Content ID:</strong> {content_id}</p>
            <p>Your text recipe has been uploaded to CorpusApp.</p>
        </div>
        """, unsafe_allow_html=True)

        # Clear form
        clear_text_form()
        st.rerun()

    except CorpusAppError as e:
        st.markdown(f"""
        <div class="error-box">
            <h4>❌ Submission Failed</h4>
            <p>{str(e)}</p>
        </div>
        """, unsafe_allow_html=True)
    except Exception as e:
        st.markdown(f"""
        <div class="error-box">
            <h4>❌ Unexpected Error</h4>
            <p>An unexpected error occurred: {str(e)}</p>
        </div>
        """, unsafe_allow_html=True)

def submit_audio_recipe(title: str, audio_file, description: str, user_name: str):
    """Submit audio recipe to CorpusApp"""
    try:
        # Validate audio file
        file_bytes = audio_file.getvalue()
        is_valid, error_msg = validate_audio_file(
            file_bytes,
            audio_file.name,
            settings.ALLOWED_AUDIO_TYPES,
            settings.MAX_UPLOAD_MB
        )

        if not is_valid:
            st.markdown(f"""
            <div class="error-box">
                <h4>❌ Invalid Audio File</h4>
                <p>{error_msg}</p>
            </div>
            """, unsafe_allow_html=True)
            return

        client = CorpusClient()

        # Upload audio file
        with st.spinner("Uploading audio file..."):
            media_result = client.upload_media(
                file_bytes,
                audio_file.name,
                audio_file.type
            )

        # Build content text
        content_parts = [f"Audio Recipe: {title.strip()}"]

        if description.strip():
            content_parts.append(f"Description: {description.strip()}")

        if user_name.strip():
            content_parts.append(f"Submitted by: {user_name.strip()}")

        content_text = "\n\n".join(content_parts)

        # Build content payload in correct format
        payload = {
            "title": title.strip(),
            "content": content_text,
            "category_id": settings.CATEGORY_ID_FOOD,
            "media_type": "audio",
            "media_url": media_result.get('url') or media_result.get('id')
        }

        # Submit content
        with st.spinner("Creating content in CorpusApp..."):
            result = client.create_content(payload)

        # Success
        content_id = result.get('id', 'Unknown')
        st.session_state.last_success_id = content_id

        st.markdown(f"""
        <div class="success-box">
            <h4>✅ Audio Recipe Submitted Successfully!</h4>
            <p><strong>Content ID:</strong> {content_id}</p>
            <p>Your audio recipe has been uploaded to CorpusApp.</p>
        </div>
        """, unsafe_allow_html=True)

        # Clear form
        clear_audio_form()
        st.rerun()

    except CorpusAppError as e:
        st.markdown(f"""
        <div class="error-box">
            <h4>❌ Submission Failed</h4>
            <p>{str(e)}</p>
        </div>
        """, unsafe_allow_html=True)
    except Exception as e:
        st.markdown(f"""
        <div class="error-box">
            <h4>❌ Unexpected Error</h4>
            <p>An unexpected error occurred: {str(e)}</p>
        </div>
        """, unsafe_allow_html=True)

def main():
    """Main application"""
    init_session_state()

    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🍽️ Vantala Vaani</h1>
        <p style="font-size: 1.2em; color: #666;">Minimal Food Recipe Uploader to CorpusApp</p>
    </div>
    """, unsafe_allow_html=True)

    # Check configuration
    if not check_configuration():
        return

    # Test connection (optional, in sidebar)
    with st.sidebar:
        st.header("🔧 Configuration")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Test Connection"):
                client = CorpusClient()
                with st.spinner("Testing connection..."):
                    if client.test_connection():
                        st.success("✅ Connection successful!")
                    else:
                        st.error("❌ Connection failed. Check your settings.")

        with col2:
            if st.button("Discover Endpoints"):
                client = CorpusClient()
                with st.spinner("Discovering endpoints..."):
                    endpoints = client.discover_endpoints()
                    if endpoints["working_endpoints"]:
                        st.success("✅ Found endpoints!")
                        for endpoint_type, url in endpoints["working_endpoints"].items():
                            st.write(f"**{endpoint_type}**: `{url}`")
                    else:
                        st.warning("⚠️ No endpoints discovered. Check your base URL.")

        st.markdown("---")
        st.markdown(f"""
        **Current Settings:**
        - **Base URL:** `{settings.CORPUSAPP_BASE_URL}`
        - **Max Upload:** {settings.MAX_UPLOAD_MB}MB
        - **Allowed Types:** {', '.join(settings.ALLOWED_AUDIO_TYPES)}
        - **Category ID:** `{settings.CATEGORY_ID_FOOD[:8]}...`
        """)

        if settings.CORPUSAPP_TOKEN and len(settings.CORPUSAPP_TOKEN) > 10:
            st.write(f"**Token:** `{settings.CORPUSAPP_TOKEN[:8]}...`")
        else:
            st.warning("⚠️ API Token not configured")    # Main tabs
    tab1, tab2 = st.tabs(["📝 Text Recipe", "🎤 Audio Recipe"])

    with tab1:
        st.header("Submit Text Recipe")

        with st.form("text_recipe_form", clear_on_submit=False):
            col1, col2 = st.columns([2, 1])

            with col1:
                title = st.text_input(
                    "Recipe Title *",
                    key="text_title",
                    placeholder="e.g., Spicy Chicken Biryani"
                )

                ingredients = st.text_area(
                    "Ingredients (optional)",
                    key="text_ingredients",
                    placeholder="One ingredient per line:\nChicken — 500g\nBasmati Rice — 2 cups\nOnions — 2 large",
                    height=100
                )

                steps = st.text_area(
                    "Cooking Steps (optional)",
                    key="text_steps",
                    placeholder="Describe the cooking process...",
                    height=150
                )

            with col2:
                user_name = st.text_input(
                    "Your Name (optional)",
                    key="text_user_name",
                    placeholder="Recipe submitter"
                )

                st.markdown("### Preview")
                if ingredients:
                    parsed = parse_ingredients(ingredients)
                    if parsed:
                        st.write("**Parsed Ingredients:**")
                        for ing in parsed[:3]:  # Show first 3
                            st.write(f"• {ing['name_te']}" + (f" — {ing['qty']}" if ing['qty'] else ""))
                        if len(parsed) > 3:
                            st.write(f"... and {len(parsed) - 3} more")

            submitted = st.form_submit_button("Submit Text Recipe", type="primary", use_container_width=True)

            if submitted:
                if not title.strip():
                    st.error("Please enter a recipe title.")
                else:
                    submit_text_recipe(title, ingredients, steps, user_name)

    with tab2:
        st.header("Submit Audio Recipe")

        with st.form("audio_recipe_form", clear_on_submit=False):
            col1, col2 = st.columns([2, 1])

            with col1:
                title = st.text_input(
                    "Recipe Title *",
                    key="audio_title",
                    placeholder="e.g., Grandma's Secret Curry Recipe"
                )

                audio_file = st.file_uploader(
                    "Upload Audio File *",
                    type=settings.ALLOWED_AUDIO_TYPES,
                    help=f"Supported formats: {', '.join(settings.ALLOWED_AUDIO_TYPES)}. Max size: {settings.MAX_UPLOAD_MB}MB"
                )

                if audio_file:
                    # Show file info
                    file_size = len(audio_file.getvalue())
                    st.info(f"**File:** {audio_file.name} ({format_file_size(file_size)})")

                    # Audio preview
                    st.audio(audio_file.getvalue())

                description = st.text_area(
                    "Description (optional)",
                    key="audio_description",
                    placeholder="Brief description of the recipe or any notes...",
                    height=100
                )

            with col2:
                user_name = st.text_input(
                    "Your Name (optional)",
                    key="audio_user_name",
                    placeholder="Recipe submitter"
                )

                if audio_file:
                    st.markdown("### File Details")
                    file_bytes = audio_file.getvalue()
                    is_valid, error_msg = validate_audio_file(
                        file_bytes,
                        audio_file.name,
                        settings.ALLOWED_AUDIO_TYPES,
                        settings.MAX_UPLOAD_MB
                    )

                    if is_valid:
                        st.success("✅ File is valid")
                    else:
                        st.error(f"❌ {error_msg}")

            submitted = st.form_submit_button("Submit Audio Recipe", type="primary", use_container_width=True)

            if submitted:
                if not title.strip():
                    st.error("Please enter a recipe title.")
                elif not audio_file:
                    st.error("Please upload an audio file.")
                else:
                    submit_audio_recipe(title, audio_file, description, user_name)

if __name__ == "__main__":
    main()
