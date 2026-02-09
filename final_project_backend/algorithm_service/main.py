"""
Movement Detection Algorithm Service

This service processes video streams and detects movement in real-time.
It uses background subtraction and contour detection to identify moving objects.
"""

from src.globals.utils.utils import Utils
from src.infrastructure.factories.manager_factory import ManagerFactory
import os
import sys

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))


def main():
    """Main entry point for the algorithm service."""
    print("=" * 60)
    print("Movement Detection Algorithm Service")
    print("=" * 60)

    # Get sensitivity from environment variable (default: 0.5)
    sensitivity = float(os.getenv('ALGORITHM_SENSITIVITY', '0.5'))

    if not 0.0 <= sensitivity <= 1.0:
        print(f"Warning: Invalid sensitivity {sensitivity}, using default 0.5")
        sensitivity = 0.5

    print(f"Starting with sensitivity: {sensitivity}")
    print(f"Higher sensitivity = more sensitive movement detection")
    print("=" * 60)

    try:
        # Create and start the video manager with algorithm
        ManagerFactory.create_all(sensitivity=sensitivity)
    except KeyboardInterrupt:
        print("\nShutting down algorithm service...")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
