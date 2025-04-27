import re

def clean_text(text):
    """
    Cleans the input text by removing unwanted characters and formatting.
    
    Args:
        text (str): The text to be cleaned.
        
    Returns:
        str: The cleaned text.
    """
    # remove HTML tags
    clean = re.compile('<[^>]*?>')
    text = re.sub(clean, '', text)
    
    # remove special characters and extra spaces
    text = re.sub(r'[^a-zA-Z0-9]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    # remove URLs
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
    
    # trim leading and trailing whitespace
    text = text.strip()
    
    # remove extra whitespace
    text = ' '.join(text.split())
    return text