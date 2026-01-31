import logging
from typing import List, Optional
from pydantic import BaseModel
import ast

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class CodeProcessingError(Exception):
    """Base exception for code processing errors."""
    def __init__(self, message: str, code: int = 500):
        self.message = message
        self.code = code
        super().__init__(self.message)

class CodeReviewMetadata(BaseModel):
    """Metadata for code review requests."""
    file_path: str
    line_numbers: List[int]
    code_snippet: str
    commit_hash: Optional[str] = None

class CodeProcessor:
    """Utility class for processing code snippets."""
    def __init__(self):
        pass

    def format_code(self, code: str) -> str:
        """
        Format code by adding line breaks and trimming whitespace.
        
        Args:
            code (str): The code snippet to format.
            
        Returns:
            str: Formatted code.
            
        Raises:
            CodeProcessingError: If code is empty or invalid.
        """
        if not code.strip():
            logger.error("Empty code snippet provided.")
            raise CodeProcessingError("Code snippet cannot be empty.", code=400)
        
        # Basic formatting: add line breaks and trim whitespace
        formatted = '\n'.join(line.strip() for line in code.split('\n'))
        logger.debug(f"Formatted code: {formatted}")
        return formatted

    def sanitize_code(self, code: str) -> str:
        """
        Sanitize code by removing comments and unnecessary whitespace.
        
        Args:
            code (str): The code snippet to sanitize.
            
        Returns:
            str: Sanitized code.
            
        Raises:
            CodeProcessingError: If code is empty or invalid.
        """
        if not code.strip():
            logger.error("Empty code snippet provided.")
            raise CodeProcessingError("Code snippet cannot be empty.", code=400)
        
        # Remove comments (simple approach, may not handle all cases)
        lines = code.split('\n')
        sanitized = []
        for line in lines:
            # Remove inline comments
            line = line.split('#')[0].strip()
            sanitized.append(line)
        sanitized_code = '\n'.join(sanitized)
        logger.debug(f"Sanitized code: {sanitized_code}")
        return sanitized_code

    def validate_code(self, code: str) -> bool:
        """
        Validate code syntax using Python's AST module.
        
        Args:
            code (str): The code snippet to validate.
            
        Returns:
            bool: True if code is valid, False otherwise.
            
        Raises:
            CodeProcessingError: If code is empty or invalid.
        """
        if not code.strip():
            logger.error("Empty code snippet provided.")
            raise CodeProcessingError("Code snippet cannot be empty.", code=400)
        
        try:
            ast.parse(code)
            logger.info("Code syntax validation passed.")
            return True
        except (SyntaxError, IndentationError) as e:
            logger.error(f"Syntax error in code: {e}")
            raise CodeProcessingError(f"Invalid code syntax: {e}", code=400)
        except Exception as e:
            logger.error(f"Unexpected error during validation: {e}")
            raise CodeProcessingError(f"Unexpected error: {e}", code=500)

def extract_code_from_diff(diff: str) -> str:
    """
    Extract code from a diff string using a simple regex.
    
    Args:
        diff (str): The diff string containing code blocks.
        
    Returns:
        str: Extracted code snippet.
        
    Raises:
        CodeProcessingError: If no code is found in the diff.
    """
    import re
    code_blocks = re.findall(r'