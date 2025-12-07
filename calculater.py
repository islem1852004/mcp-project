from mcp.server.fastmcp import FastMCP


mcp=FastMCP(name='Calculater')
@mcp.tool()
def add(a: float, b: float):
    """fonction to add two numbers"""
    return a + b
@mcp.tool()
def subtract(a: float, b: float):   
    """fonction to subtract two numbers"""
    return a - b        
@mcp.tool()
def multiply(a: float, b: float):   
    """fonction to multiply two numbers"""
    return a * b    
@mcp.tool()
def divide(a: float, b: float):   
    """fonction to divide two numbers"""
    if b == 0:
        return "Error: Division by zero"
    return a / b
@mcp.tool()
def power(a: float, b: float):   
    """fonction to raise a to the power of b"""
    return a ** b



if __name__ == "__main__":
    mcp.run(transport="stdio")
