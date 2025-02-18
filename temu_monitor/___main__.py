# temu_monitor/__main__.py
import asyncio
from .main import main

def command_line_entry():
    print("Hello from temu-monitor!")
    asyncio.run(main())

if __name__ == "__main__":
    command_line_entry()