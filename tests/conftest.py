import sys
from pathlib import Path

# scripts/ ships inside the plugin and is not an importable package, so the
# tests import the module by putting its directory on the path.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
