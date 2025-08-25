import streamlit as st
import os
from dotenv import load_dotenv
from services.auth_service import AuthService
from services.record_service import RecordService
from utils.file_handler import FileHandler
from utils.logger import Logger

# Load environment variables
load_dotenv()

# Initialize services
auth_service = AuthService()
record_service = RecordService()
file_handler = FileHandler()
logger = Logger()

def main():
    st.title("🍽️ Food Recipe Collection App")
    st.markdown("---")
    st.markdown("**Collect recipes in text, audio, and video formats for Indic language corpus building**")

    # Check authentication
    if not auth_service.is_authenticated():
        st.error("❌ Authentication failed. Please check your ACCESS_TOKEN in environment variables.")
        st.stop()

    # Clear cache button for debugging
    if st.button("🔄 Refresh Interface", help="Click if the interface is not updating properly"):
        st.rerun()

    # Format selection OUTSIDE the form to make it more reactive
    st.subheader("📝 Submit a Recipe")
    format_option = st.radio(
        "Select recipe format:",
        ("Audio", "Video", "Image"),
        help="Choose how you want to submit your recipe",
        key="format_selector"
    )

    # Show current selection for debugging
    st.info(f"📌 Selected format: {format_option}")

    # Recipe submission form
    with st.form("recipe_form", clear_on_submit=True):
        # Initialize variables
        uploaded_file = None

        if format_option == "Audio":
            st.markdown("**🎵 Audio File Upload**")
            uploaded_file = st.file_uploader(
                "Upload audio file:",
                type=['mp3', 'wav', 'm4a'],
                help="Record yourself explaining the recipe (max 50MB)",
                key="audio_uploader"
            )
            if uploaded_file:
                st.success(f"✅ Audio file selected: {uploaded_file.name} ({uploaded_file.size / (1024*1024):.1f} MB)")

        elif format_option == "Video":
            st.markdown("**🎥 Video File Upload**")
            uploaded_file = st.file_uploader(
                "Upload video file:",
                type=['mp4', 'mov', 'avi'],
                help="Show the cooking process in action (max 100MB)",
                key="video_uploader"
            )
            if uploaded_file:
                st.success(f"✅ Video file selected: {uploaded_file.name} ({uploaded_file.size / (1024*1024):.1f} MB)")

        else:  # Image
            st.markdown("**📸 Image File Upload**")
            uploaded_file = st.file_uploader(
                "Upload image file:",
                type=['jpg', 'jpeg', 'png', 'webp'],
                help="Share photos of your dish, ingredients, or cooking process (max 10MB)",
                key="image_uploader"
            )
            if uploaded_file:
                st.success(f"✅ Image file selected: {uploaded_file.name} ({uploaded_file.size / (1024*1024):.1f} MB)")
                # Show image preview
                st.image(uploaded_file, caption="Recipe Image Preview", use_column_width=True)

        # Additional metadata
        st.subheader("📋 Additional Information (Optional)")
        col1, col2 = st.columns(2)

        with col1:
            recipe_name = st.text_input("Recipe Name:", placeholder="e.g., Grandmother's Biryani")
            cuisine_type = st.text_input("Cuisine Type:", placeholder="e.g., South Indian, Punjabi")

        with col2:
            cooking_time = st.text_input("Cooking Time:", placeholder="e.g., 45 minutes")
            difficulty = st.selectbox("Difficulty Level:", ["Easy", "Medium", "Hard", "Not specified"])

        # Submit button
        submitted = st.form_submit_button("🚀 Submit Recipe", type="primary")

        if submitted:
            # Validate input
            if not uploaded_file:
                st.error(f"Please upload a {format_option.lower()} file.")
                return

            # Process submission
            with st.spinner(f"Submitting your {format_option.lower()} recipe..."):
                try:
                    # Validate file
                    if not file_handler.validate_file(uploaded_file, format_option.lower()):
                        st.error("Invalid file format or size. Please check your file and try again.")
                        return

                    success, message, record_id = record_service.submit_media_recipe(
                        uploaded_file, format_option.lower(), recipe_name, cuisine_type, cooking_time, difficulty
                    )

                    if success:
                        st.success(f"✅ {message}")
                        if record_id:
                            st.info(f"📄 Record ID: {record_id}")

                        # Log successful submission
                        logger.log_submission(format_option, recipe_name or "Unnamed Recipe", "Success", record_id)

                        # Show success metrics
                        st.balloons()

                    else:
                        st.error(f"❌ {message}")
                        logger.log_submission(format_option, recipe_name or "Unnamed Recipe", "Failed", None)

                except Exception as e:
                    st.error(f"❌ An unexpected error occurred: {str(e)}")
                    logger.log_submission(format_option, recipe_name or "Unnamed Recipe", f"Error: {str(e)}", None)

    # Sidebar with information
    with st.sidebar:
        st.header("📊 App Information")
        st.markdown("**Purpose:** Collect traditional recipes for Indic language corpus building")
        st.markdown("**Supported Formats:**")
        st.markdown("- 🎵 Audio recordings (.mp3, .wav, .m4a)")
        st.markdown("- 🎥 Video demonstrations (.mp4, .mov, .avi)")
        st.markdown("- 📸 Recipe images (.jpg, .jpeg, .png, .webp)")

        st.markdown("---")
        st.markdown("**Tips:**")
        st.markdown("- Include traditional cooking methods")
        st.markdown("- Mention regional variations")
        st.markdown("- Use local ingredient names")
        st.markdown("- Share family recipes and stories")
        st.markdown("- For images: show finished dishes, ingredients, or cooking steps")

        # Show recent submissions count
        recent_count = logger.get_recent_submissions_count()
        if recent_count > 0:
            st.markdown("---")
            st.metric("Recent Submissions", recent_count)

if __name__ == "__main__":
    main()
