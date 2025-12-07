from mcp.server.fastmcp import FastMCP


mcp=FastMCP(name='say hello')
@mcp.tool()
def say_hello(name: str):
    """fonction to say hello"""
    
    return f"Hello, {name}!"


if __name__ == "__main__":
    mcp.run(transport="stdio")
