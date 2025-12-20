from django.core.exceptions import ValidationError
import os
import re


def validate_image_file(file):
    """
    Validates uploaded image files for size and type.
    
    Args:
        file: The uploaded file object
        
    Raises:
        ValidationError: If file is invalid
    """
    # Define maximum file size (5MB = 5 * 1024 * 1024 bytes)
    max_size_mb = 5
    max_size_bytes = max_size_mb * 1024 * 1024
    
    # Validate file size
    if file.size > max_size_bytes:
        raise ValidationError(
            f'File size must be less than {max_size_mb}MB. Your file is {file.size / (1024 * 1024):.2f}MB.'
        )
    
    # Validate file extension
    allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    ext = os.path.splitext(file.name)[1].lower()
    
    if ext not in allowed_extensions:
        raise ValidationError(
            f'File extension "{ext}" is not allowed. Allowed extensions: {", ".join(allowed_extensions)}'
        )
    
    # Validate content type (MIME type)
    allowed_content_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
    
    if hasattr(file, 'content_type') and file.content_type not in allowed_content_types:
        raise ValidationError(
            f'File type "{file.content_type}" is not allowed. Must be a valid image file.'
        )


def validate_no_scripts(value):
    """
    XSS Protection: Validates that text fields don't contain script tags or dangerous HTML.
    
    This helps prevent Cross-Site Scripting (XSS) attacks where attackers try to inject
    malicious JavaScript code into your database.
    
    Args:
        value: The text to validate
        
    Raises:
        ValidationError: If dangerous content is detected
        
    Example of blocked content:
        - <script>alert('hack')</script>
        - <img src=x onerror="alert('xss')">
        - javascript:alert('xss')
    """
    # List of dangerous patterns that could be used for XSS attacks
    dangerous_patterns = [
        r'<script[^>]*>.*?</script>',  # Script tags
        r'javascript:',                 # JavaScript protocol
        r'on\w+\s*=',                  # Event handlers (onclick, onerror, etc.)
        r'<iframe',                     # iframes
        r'<embed',                      # embed tags
        r'<object',                     # object tags
    ]
    
    # Check each pattern
    for pattern in dangerous_patterns:
        if re.search(pattern, value, re.IGNORECASE):
            raise ValidationError(
                'Input contains potentially dangerous content. Please remove any HTML/JavaScript code.'
            )
    
    return value

