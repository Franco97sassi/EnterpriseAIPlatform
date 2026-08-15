from mcp.server import MCPServer


mcp = MCPServer("enterprise-ai-platform")


@mcp.tool()
def get_platform_status() -> dict[str, str]:
    """
    Return the current status of the Enterprise AI Platform.
    """
    return {
        "status": "ok",
        "platform": "enterprise-ai-platform",
    }


@mcp.tool()
def calculate_sum(a: float, b: float) -> dict[str, float]:
    """
    Add two numbers and return the result.
    """
    return {
        "result": a + b,
    }


@mcp.tool()
def calculate_percentage(value: float, percentage: float) -> dict[str, float]:
    """
    Calculate a percentage of a value.
    """

    if value < 0:
        raise ValueError("value must be greater than or equal to 0")

    if percentage < 0 or percentage > 100:
        raise ValueError("percentage must be between 0 and 100")

    return {
        "result": value * (percentage / 100),
    }


if __name__ == "__main__":
    mcp.run()