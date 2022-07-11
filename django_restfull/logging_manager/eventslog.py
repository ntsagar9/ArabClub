import logging

logging.basicConfig(level=logging.DEBUG)
# Crate custom massage format
formatter = """
%(asctime)s - %(levelname)s - %(pathname)s - %(funcName)s - %(message)s
"""
# handler format style
formatter = logging.Formatter(formatter)

# Make own logger
logger = logging.getLogger(__name__)
# Stop public logger
logger.propagate = 0

# Crate stream handler
stream_h = logging.StreamHandler()
# Create File handler
file_h = logging.FileHandler("error.log")
# Success Process handler
success_h = logging.FileHandler("success.log")

# Set event level for stream
stream_h.setLevel(logging.WARNING)
# Set event level for file
file_h.setLevel(logging.ERROR)
# set event leve for success process
success_h.setLevel(logging.INFO)

# Set format massage style
stream_h.setFormatter(formatter)
file_h.setFormatter(formatter)
success_h.setFormatter(formatter)

# Add handler for logger
logger.addHandler(stream_h)
logger.addHandler(file_h)
logger.addHandler(success_h)
