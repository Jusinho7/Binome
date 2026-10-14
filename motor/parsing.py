import sys
try:
    import pydantic
except ImportError:
    print("pydantic is not installed. Please install it to use the parsing features.")
    sys.exit(1)