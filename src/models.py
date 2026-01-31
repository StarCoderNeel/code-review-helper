import logging
from typing import List, Dict, Optional, Any, Union
from pydantic import BaseModel, Field
from fastapi import HTTPException
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class InvalidCodeSnippetError(Exception):
    """Raised when the code snippet is invalid or empty."""
    pass

class CodeAnalysisError(Exception):
    """Raised when an error occurs during code analysis."""
    pass

class CodeReviewRequest(BaseModel):
    """
    Model for code review request data.
    
    Example:
        {
            "code_snippet": "def add(a, b):\n    return a + b",
            "repository_info": {
                "repo_url": "https://github.com/example/repo",
                "branch": "main"
            },
            "user_details": {
                "username": "dev_user",
                "email": "user@example.com"
            },
            "analysis_type": "security"
        }
    """
    code_snippet: str = Field(..., description="The code snippet to review")
    repository_info: Dict[str, Any] = Field(default_factory=dict, description="Repository metadata")
    user_details: Dict[str, Any] = Field(default_factory=dict, description="User information")
    analysis_type: str = Field("general", description="Type of analysis to perform")

class CodeReviewResponse(BaseModel):
    """
    Model for code review response data.
    
    Example:
        {
            "findings": [
                {
                    "severity": "high",
                    "description": "Potential SQL injection vulnerability",
                    "line_number": 15,
                    "code_snippet": "query = f"SELECT * FROM users WHERE name = '{user_input}'""
                }
            ],
            "suggestions": [
                "Use parameterized queries to prevent SQL injection"
            ],
            "metadata": {
                "analysis_time": "2023-09-20T12:34:56Z",
                "tool_version": "1.0.0"
            }
        }
    """
    findings: List[Dict[str, Any]] = Field(default_factory=list, description="List of code issues found")
    suggestions: List[str] = Field(default_factory=list, description="Code improvement suggestions")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

class Finding:
    """
    Represents a code issue found during analysis.
    
    Attributes:
        severity (str): Severity level of the issue (low/medium/high)
        description (str): Description of the issue
        line_number (int): Line number in the code snippet where the issue occurs
        code_snippet (str): Relevant code snippet from the original input
        category (str): Category of the issue (e.g., security, best practices)
    """
    def __init__(self, severity: str, description: str, line_number: int, code_snippet: str, category: str):
        self.severity = severity
        self.description = description
        self.line_number = line_number
        self.code_snippet = code_snippet
        self.category = category

    def to_dict(self) -> Dict[str, Any]:
        """Convert the finding to a dictionary for API response."""
        return {
            "severity": self.severity,
            "description": self.description,
            "line_number": self.line_number,
            "code_snippet": self.code_snippet,
            "category": self.category
        }

class CodeAnalyzer:
    """
    Analyzes code for quality, security, and best practices.
    
    Methods:
        analyze_code: Perform code analysis and return findings
    """
    
    def __init__(self):
        self._security_patterns = {
            r"(\bSELECT\s+.*\s+FROM\s+.*\s+WHERE\s+.*\s+=\s+['\"]?([^'\"]*)['\"]?)": "Potential SQL injection vulnerability",
            r"(\bexec\s*\()": "Potential code execution vulnerability",
            r"(\bflag\s+as\s+.*\s+PERSISTENT)": "Potential data persistence vulnerability"
        }
    
    def analyze_code(self, request: CodeReviewRequest) -> CodeReviewResponse:
        """
        Analyze the code snippet for issues.
        
        Args:
            request: CodeReviewRequest object containing code and metadata
            
        Returns:
            CodeReviewResponse object with findings and suggestions
            
        Raises:
            CodeAnalysisError: If an error occurs during analysis
        """
        try:
            logger.info("Starting code analysis for request: %s", request.code_snippet[:50])
            
            if not self._validate_code_snippet(request.code_snippet):
                raise InvalidCodeSnippetError("Invalid or empty code snippet")
            
            findings = []
            suggestions = []
            
            # Security checks
            for pattern, description in self._security_patterns.items():
                matches = re.finditer(pattern, request.code_snippet, re.DOTALL)
                for match in matches:
                    line_number = self._get_line_number(request.code_snippet, match.start())
                    findings.append(
                        Finding(
                            severity="high",
                            description=description,
                            line_number=line_number,
                            code_snippet=match.group(0),
                            category="security"
                        )
                    )
            
            # Best practices checks (example: unused variables)
            unused_vars = re.findall(r"\b(\w+)\s*=\s*.*\s*;\s*.*\s*=\s*.*\s*;", request.code_snippet)
            if unused_vars:
                suggestions.append(f"Unused variables detected: {', '.join(unused_vars)}")
            
            # Return response
            return CodeReviewResponse(
                findings=[f.to_dict() for f in findings],
                suggestions=suggestions,
                metadata={
                    "analysis_time": self._get_current_time(),
                    "tool_version": "1.0.0"
                }
            )
        
        except Exception as e:
            logger.error("Error during code analysis: %s", str(e))
            raise CodeAnalysisError(f"Code analysis failed: {str(e)}") from e

    def _validate_code_snippet(self, code: str) -> bool:
        """
        Validate the code snippet for basic requirements.
        
        Args:
            code: The code snippet to validate
            
        Returns:
            bool: True if valid, False otherwise
            
        Example:
            >>> _validate_code_snippet("def hello():\n    print('Hello')") 
            True
        """
        if not code or len(code.strip()) == 0:
            logger.warning("Empty code snippet provided")
            return False
            
        if not re.search(r"[^\s]", code):  # Check for non-whitespace characters
            logger.warning("Code snippet contains only whitespace")
            return False
            
        return True

    def _get_line_number(self, code: str, position: int) -> int:
        """
        Get the line number in the code snippet for a given position.
        
        Args:
            code: The code snippet
            position: The position in the code
            
        Returns:
            int: Line number (1-based)
            
        Example:
            >>> _get_line_number("def hello():\n    print('Hello')", 14)
            2
        """
        lines = code.splitlines()
        for i, line in enumerate(lines):
            if position < len(line):
                return i + 1
            position -= len(line)
        return len(lines)

    def _get_current_time(self) -> str:
        """Get the current time in ISO 8601 format."""
        from datetime import datetime
        return datetime.now().isoformat()