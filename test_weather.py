import asyncio
import sys
import os

# Add the servers directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'servers'))

from weather import get_alerts

async def main():
    print("Fetching weather alerts for NY...")
    alerts = await get_alerts("NY")
    print(alerts)

if __name__ == "__main__":
    asyncio.run(main()) 