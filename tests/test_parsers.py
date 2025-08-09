import pytest
from services.parsers import parse_ingredients, validate_audio_file, format_file_size

class TestParseIngredients:
    """Test ingredients parsing functionality"""

    def test_empty_input(self):
        """Test with empty input"""
        assert parse_ingredients("") == []
        assert parse_ingredients("   ") == []
        assert parse_ingredients(None) == []

    def test_single_ingredient_with_quantity(self):
        """Test parsing single ingredient with quantity"""
        result = parse_ingredients("Chicken — 500g")
        expected = [{"name_te": "Chicken", "qty": "500g"}]
        assert result == expected

    def test_multiple_ingredients(self):
        """Test parsing multiple ingredients"""
        text = """Chicken — 500g
Basmati Rice — 2 cups
Onions — 2 large"""

        result = parse_ingredients(text)
        expected = [
            {"name_te": "Chicken", "qty": "500g"},
            {"name_te": "Basmati Rice", "qty": "2 cups"},
            {"name_te": "Onions", "qty": "2 large"}
        ]
        assert result == expected

    def test_different_separators(self):
        """Test parsing with different separators"""
        # Em dash
        result1 = parse_ingredients("Salt — to taste")
        assert result1 == [{"name_te": "Salt", "qty": "to taste"}]

        # Hyphen
        result2 = parse_ingredients("Pepper - 1 tsp")
        assert result2 == [{"name_te": "Pepper", "qty": "1 tsp"}]

        # Comma
        result3 = parse_ingredients("Sugar, 2 tbsp")
        assert result3 == [{"name_te": "Sugar", "qty": "2 tbsp"}]

    def test_ingredient_without_quantity(self):
        """Test parsing ingredient without quantity"""
        result = parse_ingredients("Fresh herbs")
        expected = [{"name_te": "Fresh herbs", "qty": ""}]
        assert result == expected

    def test_empty_lines_ignored(self):
        """Test that empty lines are ignored"""
        text = """Chicken — 500g

Onions — 2 large

"""
        result = parse_ingredients(text)
        expected = [
            {"name_te": "Chicken", "qty": "500g"},
            {"name_te": "Onions", "qty": "2 large"}
        ]
        assert result == expected

    def test_whitespace_trimmed(self):
        """Test that whitespace is properly trimmed"""
        text = "  Chicken  —  500g  "
        result = parse_ingredients(text)
        expected = [{"name_te": "Chicken", "qty": "500g"}]
        assert result == expected

class TestValidateAudioFile:
    """Test audio file validation"""

    def test_valid_file(self):
        """Test validation of valid audio file"""
        file_bytes = b"fake audio content" * 1000  # ~17KB
        is_valid, error = validate_audio_file(file_bytes, "recipe.mp3", ["mp3", "wav"], 50)
        assert is_valid is True
        assert error == ""

    def test_empty_file(self):
        """Test validation of empty file"""
        is_valid, error = validate_audio_file(b"", "recipe.mp3", ["mp3"], 50)
        assert is_valid is False
        assert "No file content" in error

    def test_file_too_large(self):
        """Test validation of oversized file"""
        file_bytes = b"x" * (51 * 1024 * 1024)  # 51MB
        is_valid, error = validate_audio_file(file_bytes, "recipe.mp3", ["mp3"], 50)
        assert is_valid is False
        assert "exceeds maximum" in error

    def test_invalid_extension(self):
        """Test validation of invalid file extension"""
        file_bytes = b"fake content"
        is_valid, error = validate_audio_file(file_bytes, "recipe.txt", ["mp3", "wav"], 50)
        assert is_valid is False
        assert "not allowed" in error

    def test_no_extension(self):
        """Test validation of file without extension"""
        file_bytes = b"fake content"
        is_valid, error = validate_audio_file(file_bytes, "recipe", ["mp3"], 50)
        assert is_valid is False
        assert "must have an extension" in error

    def test_case_insensitive_extension(self):
        """Test that file extension check is case insensitive"""
        file_bytes = b"fake content"
        is_valid, error = validate_audio_file(file_bytes, "recipe.MP3", ["mp3"], 50)
        assert is_valid is True
        assert error == ""

class TestFormatFileSize:
    """Test file size formatting"""

    def test_bytes(self):
        """Test formatting bytes"""
        assert format_file_size(500) == "500 B"
        assert format_file_size(1023) == "1023 B"

    def test_kilobytes(self):
        """Test formatting kilobytes"""
        assert format_file_size(1024) == "1.0 KB"
        assert format_file_size(1536) == "1.5 KB"
        assert format_file_size(1048575) == "1024.0 KB"

    def test_megabytes(self):
        """Test formatting megabytes"""
        assert format_file_size(1048576) == "1.0 MB"
        assert format_file_size(1572864) == "1.5 MB"
        assert format_file_size(52428800) == "50.0 MB"
