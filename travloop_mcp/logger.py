import logging
import sys

# Configure logging
logger = logging.getLogger("MCP Server")
logger.setLevel(logging.DEBUG)

# File handler with DEBUG level
file_handler = logging.FileHandler("mcp_server.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)
logger.addHandler(file_handler)

# Console handler with INFO level
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)
logger.addHandler(console_handler)

# Error handler (stderr) - for warnings/errors
error_handler = logging.StreamHandler(sys.stderr)
error_handler.setLevel(logging.WARNING)
error_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)
logger.addHandler(error_handler)