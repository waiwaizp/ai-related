from mcp.server.fastmcp import FastMCP

app = FastMCP()

@app.tool()
def add(a: int, b: int) -> int:
    print(f"Adding {a} and {b}")
    return a + b

if __name__ == '__main__':
    app.run(transport='streamable-http')