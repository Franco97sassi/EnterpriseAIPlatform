import asyncio

from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client


async def main() -> None:
    server_params = StdioServerParameters(
        command="python",
        args=["app/mcp/server.py"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize MCP session
            await session.initialize()

            # Discover available tools
            tools = await session.list_tools()

            print("Available tools:")
            for tool in tools.tools:
                print(f"- {tool.name}")

            # Call calculate_sum
            sum_result = await session.call_tool(
                "calculate_sum",
                arguments={
                    "a": 10,
                    "b": 25,
                },
            )

            print("\nSum result:")
            print(sum_result)

            # Call calculate_percentage
            percentage_result = await session.call_tool(
                "calculate_percentage",
                arguments={
                    "value": 200,
                    "percentage": 15,
                },
            )

            print("\nPercentage result:")
            print(percentage_result)


if __name__ == "__main__":
    asyncio.run(main())