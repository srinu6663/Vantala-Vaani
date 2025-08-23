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
    
    # Recipe submission form
    with st.form("recipe_form"):
        st.subheader("📝 Submit a Recipe")
        
        # Format selection
        format_option = st.radio(
            "Select recipe format:",
            ("Text", "Audio", "Video"),
            help="Choose how you want to submit your recipe"
        )
        
        # Initialize variables
        recipe_content = None
        uploaded_file = None
        
        if format_option == "Text":
            recipe_content = st.text_area(
                "Enter your recipe:",
                height=200,
                placeholder="Share your traditional recipe here. You can write in English or any Indic language...",
                help="Include ingredients, cooking steps, and any special techniques"
            )
            
        elif format_option == "Audio":
            uploaded_file = st.file_uploader(
                "Upload audio file:",
                type=['mp3', 'wav', 'm4a'],
                help="Record yourself explaining the recipe (max 50MB)"
            )
            
        elif format_option == "Video":
            uploaded_file = st.file_uploader(
                "Upload video file:",
                type=['mp4', 'mov', 'avi'],
                help="Show the cooking process in action (max 100MB)"
            )
        
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
            if format_option == "Text" and not recipe_content:
                st.error("Please enter your recipe content.")
                return
            
            if format_option in ["Audio", "Video"] and not uploaded_file:
                st.error(f"Please upload a {format_option.lower()} file.")
                return
            
            # Process submission
            with st.spinner(f"Submitting your {format_option.lower()} recipe..."):
                try:
                    if format_option == "Text":
                        success, message, record_id = record_service.submit_text_recipe(
                            recipe_content, recipe_name, cuisine_type, cooking_time, difficulty
                        )
                    else:
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
        st.markdown("- 📝 Text recipes")
        st.markdown("- 🎵 Audio recordings (.mp3, .wav, .m4a)")
        st.markdown("- 🎥 Video demonstrations (.mp4, .mov, .avi)")
        
        st.markdown("---")
        st.markdown("**Tips:**")
        st.markdown("- Include traditional cooking methods")
        st.markdown("- Mention regional variations")
        st.markdown("- Use local ingredient names")
        st.markdown("- Share family recipes and stories")
        
        # Show recent submissions count
        recent_count = logger.get_recent_submissions_count()
        if recent_count > 0:
            st.markdown("---")
            st.metric("Recent Submissions", recent_count)

if __name__ == "__main__":
    main()
