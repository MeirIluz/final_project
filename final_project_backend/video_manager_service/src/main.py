"""
Video Manager Service

This service manages video streams from multiple cameras,
processes frames, and handles video I/O operations.
"""

import os
import sys

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.infrastructure.factories.manager_factory import ManagerFactory


def main():
    """Main entry point for the video manager service."""
    print("=" * 60)
    print("Video Manager Service")
    print("=" * 60)
    print("Starting video manager...")
    
    try:
        # Create and start the video manager
        ManagerFactory.create_all()
    except KeyboardInterrupt:
        print("\nShutting down video manager service...")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
