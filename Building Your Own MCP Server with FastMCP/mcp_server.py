"""
Simple MCP Server using FastMCP
Demonstrates multiple tools with different functionalities
"""

from fastmcp import FastMCP
import json
import datetime
import random
import math

# Initialize the MCP server
mcp = FastMCP("Simple MCP Server")

# Tool 1: Calculator - performs basic arithmetic operations
@mcp.tool
def calculator(operation: str, a: float, b: float) -> str:
    """
    Perform basic arithmetic operations.
    
    Args:
        operation: The operation to perform (add, subtract, multiply, divide, power)
        a: First number
        b: Second number
    
    Returns:
        The result of the operation
    """
    operations = {
        "add": lambda x, y: x + y,
        "subtract": lambda x, y: x - y,
        "multiply": lambda x, y: x * y,
        "divide": lambda x, y: x / y if y != 0 else None,
        "power": lambda x, y: x ** y,
    }
    
    if operation.lower() not in operations:
        return f"Error: Invalid operation. Available operations: {', '.join(operations.keys())}"
    
    if operation.lower() == "divide" and b == 0:
        return "Error: Division by zero is not allowed"
    
    try:
        result = operations[operation.lower()](a, b)
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {str(e)}"


# Tool 2: Text Analyzer - analyzes text content
@mcp.tool
def analyze_text(text: str) -> str:
    """
    Analyze text and provide statistics.
    
    Args:
        text: The text to analyze
    
    Returns:
        JSON string with text statistics
    """
    words = text.split()
    characters = len(text)
    characters_no_spaces = len(text.replace(" ", ""))
    sentences = text.count('.') + text.count('!') + text.count('?')
    paragraphs = text.count('\n\n') + 1 if text else 0
    
    stats = {
        "character_count": characters,
        "character_count_no_spaces": characters_no_spaces,
        "word_count": len(words),
        "sentence_count": sentences,
        "paragraph_count": paragraphs,
        "average_word_length": round(sum(len(word) for word in words) / len(words), 2) if words else 0
    }
    
    return json.dumps(stats, indent=2)


# Tool 3: Date and Time Utilities
@mcp.tool
def get_current_time(timezone: str = "UTC") -> str:
    """
    Get the current date and time.
    
    Args:
        timezone: Timezone (default: UTC). Note: This is a simplified version.
                 For production, use pytz or zoneinfo.
    
    Returns:
        Current date and time in ISO format
    """
    now = datetime.datetime.now(datetime.timezone.utc)
    return f"Current time ({timezone}): {now.isoformat()}"


# Tool 4: Random Number Generator
@mcp.tool
def generate_random_number(min_value: int = 1, max_value: int = 100) -> str:
    """
    Generate a random integer between min and max values.
    
    Args:
        min_value: Minimum value (inclusive)
        max_value: Maximum value (inclusive)
    
    Returns:
        A random number in the specified range
    """
    if min_value > max_value:
        return f"Error: min_value ({min_value}) must be less than or equal to max_value ({max_value})"
    
    number = random.randint(min_value, max_value)
    return f"Random number between {min_value} and {max_value}: {number}"


# Tool 5: String Manipulation
@mcp.tool
def string_operations(text: str, operation: str) -> str:
    """
    Perform various string operations.
    
    Args:
        text: The input text
        operation: Operation to perform (uppercase, lowercase, reverse, length, word_count)
    
    Returns:
        The result of the string operation
    """
    operations = {
        "uppercase": lambda t: t.upper(),
        "lowercase": lambda t: t.lower(),
        "reverse": lambda t: t[::-1],
        "length": lambda t: str(len(t)),
        "word_count": lambda t: str(len(t.split())),
        "title_case": lambda t: t.title(),
        "capitalize": lambda t: t.capitalize(),
    }
    
    if operation.lower() not in operations:
        available = ', '.join(operations.keys())
        return f"Error: Invalid operation. Available operations: {available}"
    
    try:
        result = operations[operation.lower()](text)
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {str(e)}"


# Tool 6: Math Utilities
@mcp.tool
def math_utilities(operation: str, values: list[float]) -> str:
    """
    Perform mathematical operations on a list of numbers.
    
    Args:
        operation: Operation to perform (sum, product, average, min, max)
        values: List of numbers to operate on
    
    Returns:
        The result of the mathematical operation
    """
    if not values:
        return "Error: Values list cannot be empty"
    
    operations = {
        "sum": lambda v: sum(v),
        "product": lambda v: math.prod(v),
        "average": lambda v: sum(v) / len(v),
        "min": lambda v: min(v),
        "max": lambda v: max(v),
    }
    
    if operation.lower() not in operations:
        available = ', '.join(operations.keys())
        return f"Error: Invalid operation. Available operations: {available}"
    
    try:
        result = operations[operation.lower()](values)
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {str(e)}"


# Tool 7: JSON Formatter
@mcp.tool
def format_json(json_string: str) -> str:
    """
    Format and validate JSON string.
    
    Args:
        json_string: The JSON string to format
    
    Returns:
        Formatted JSON string or error message
    """
    try:
        parsed = json.loads(json_string)
        return json.dumps(parsed, indent=2)
    except json.JSONDecodeError as e:
        return f"Error: Invalid JSON - {str(e)}"


# Tool 8: List Operations
@mcp.tool
def list_operations(items: list[str], operation: str) -> str:
    """
    Perform operations on a list of items.
    
    Args:
        items: List of string items
        operation: Operation to perform (sort, reverse, unique, count, join)
    
    Returns:
        The result of the list operation
    """
    if not items:
        return "Error: Items list cannot be empty"
    
    operations = {
        "sort": lambda i: sorted(i),
        "reverse": lambda i: list(reversed(i)),
        "unique": lambda i: list(dict.fromkeys(i)),  # Preserves order
        "count": lambda i: str(len(i)),
        "join": lambda i: ', '.join(i),
    }
    
    if operation.lower() not in operations:
        available = ', '.join(operations.keys())
        return f"Error: Invalid operation. Available operations: {available}"
    
    try:
        result = operations[operation.lower()](items)
        if isinstance(result, str):
            return f"Result: {result}"
        else:
            return f"Result: {result}"
    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    # Run the MCP server
    mcp.run()

