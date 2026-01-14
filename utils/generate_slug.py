# Add this at the top of serializers.py
import re
from django.utils.text import slugify
from django.utils import timezone

def generate_slug_from_bengali(text):
    """
    Generate slug from Bengali text
    """
    if not text:
        return f"news-{timezone.now().strftime('%Y%m%d-%H%M%S')}"
    
    # Try regular slugify first
    slug = slugify(text)
    if slug and slug.strip():
        return slug
    
    # For Bengali text, transliterate to English letters
    # Simple transliteration map for common Bengali characters
    bengali_to_english = {
        'অ': 'o', 'আ': 'a', 'ই': 'i', 'ঈ': 'i', 'উ': 'u', 'ঊ': 'u',
        'ঋ': 'ri', 'এ': 'e', 'ঐ': 'oi', 'ও': 'o', 'ঔ': 'ou',
        'ক': 'k', 'খ': 'kh', 'গ': 'g', 'ঘ': 'gh', 'ঙ': 'ng',
        'চ': 'ch', 'ছ': 'chh', 'জ': 'j', 'ঝ': 'jh', 'ঞ': 'n',
        'ট': 't', 'ঠ': 'th', 'ড': 'd', 'ঢ': 'dh', 'ণ': 'n',
        'ত': 't', 'থ': 'th', 'দ': 'd', 'ধ': 'dh', 'ন': 'n',
        'প': 'p', 'ফ': 'ph', 'ব': 'b', 'ভ': 'bh', 'ম': 'm',
        'য': 'j', 'র': 'r', 'ল': 'l', 'শ': 'sh', 'ষ': 'sh', 'স': 's',
        'হ': 'h', 'ড়': 'r', 'ঢ়': 'rh', 'য়': 'y', 'ৎ': 't',
        'ং': 'ng', 'ঃ': 'h', 'ঁ': 'n',
        'া': 'a', 'ি': 'i', 'ী': 'i', 'ু': 'u', 'ূ': 'u',
        'ৃ': 'ri', 'ে': 'e', 'ৈ': 'oi', 'ো': 'o', 'ৌ': 'ou',
        '্': '', '়': '', 'ৗ': 'a', '৺': 'pr',
    }
    
    # Convert Bengali to approximate English
    transliterated = ''
    for char in text:
        if char in bengali_to_english:
            transliterated += bengali_to_english[char]
        elif char.isalnum() or char in ' -_':
            transliterated += char
        else:
            transliterated += '-'
    
    # Remove multiple hyphens and trim
    slug = re.sub(r'[-]+', '-', transliterated)
    slug = slug.strip('-')
    
    if not slug:
        # Last resort: use numeric slug
        slug = f"news-{timezone.now().strftime('%Y%m%d%H%M%S')}"
    
    return slug[:100]  # Limit length