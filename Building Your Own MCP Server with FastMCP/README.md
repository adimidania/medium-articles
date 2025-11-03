# Simple MCP Server with FastMCP

This is a simple example of a Model Context Protocol (MCP) server built with FastMCP, demonstrating various tools and capabilities.

## What is MCP?

The Model Context Protocol (MCP) is a standard protocol for connecting AI assistants to external data sources and tools. MCP servers provide a way to extend AI capabilities with custom tools and resources.

## Features

This MCP server includes 8 different tools:

1. **Calculator** - Perform basic arithmetic operations (add, subtract, multiply, divide, power)
2. **Text Analyzer** - Analyze text and provide statistics (character count, word count, sentence count, etc.)
3. **Date/Time Utilities** - Get current date and time
4. **Random Number Generator** - Generate random numbers within a specified range
5. **String Operations** - Various string manipulations (uppercase, lowercase, reverse, etc.)
6. **Math Utilities** - Mathematical operations on lists (sum, product, average, min, max)
7. **JSON Formatter** - Format and validate JSON strings
8. **List Operations** - Operations on lists (sort, reverse, unique, count, join)

## Installation

1. Install Python 3.8 or higher
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Running the Server

To run the MCP server:

```bash
python mcp_server.py
```

The server will start and be ready to accept connections via the MCP protocol.

### Using with MCP Clients

This server can be used with any MCP-compatible client. The tools are automatically registered and can be called by the client.

### Example Tool Calls

Here are some examples of how the tools can be used:

#### Calculator
```python
calculator(operation="add", a=5, b=3)  # Returns: "Result: 8"
calculator(operation="multiply", a=4, b=7)  # Returns: "Result: 28"
```

#### Text Analyzer
```python
analyze_text("Hello world! This is a test.")  
# Returns JSON with statistics about the text
```

#### Random Number Generator
```python
generate_random_number(min_value=1, max_value=100)  
# Returns a random number between 1 and 100
```

#### String Operations
```python
string_operations("Hello World", "uppercase")  # Returns: "Result: HELLO WORLD"
string_operations("test", "reverse")  # Returns: "Result: tset"
```

#### Math Utilities
```python
math_utilities(operation="sum", values=[1, 2, 3, 4, 5])  # Returns: "Result: 15"
math_utilities(operation="average", values=[10, 20, 30])  # Returns: "Result: 20.0"
```

#### JSON Formatter
```python
format_json('{"name":"John","age":30}')  
# Returns nicely formatted JSON
```

#### List Operations
```python
list_operations(items=["banana", "apple", "cherry"], operation="sort")  
# Returns sorted list
```

## Project Structure

```
simple MCP/
├── mcp_server.py      # Main MCP server implementation
├── requirements.txt   # Python dependencies
└── README.md         # This file
```

## Extending the Server

To add your own tools, simply:

1. Import necessary modules at the top
2. Define a function with proper type hints
3. Add the `@mcp.tool` decorator
4. Include a docstring describing the tool's purpose, arguments, and return value

Example:

```python
@mcp.tool
def my_custom_tool(param1: str, param2: int) -> str:
    """
    Description of what the tool does.
    
    Args:
        param1: Description of param1
        param2: Description of param2
    
    Returns:
        Description of the return value
    """
    # Your tool logic here
    return "Result"
```

## Resources

- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)

## License

This is an example project provided as-is for educational purposes.

