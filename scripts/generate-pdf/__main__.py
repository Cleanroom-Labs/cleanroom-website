"""Allow running as python -m scripts.generate-pdf"""

import sys
from pathlib import Path

# Add the module directory to path
sys.path.insert(0, str(Path(__file__).parent))

from main import main

if __name__ == "__main__":
    sys.exit(main())
