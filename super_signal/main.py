"""Main entry point for Super Signal.

This module sets up logging and launches the appropriate interface
(CLI for now, with future support for GUI).
"""

import sys
import argparse

from .config import setup_logging
from .cli import run_cli


def parse_arguments():
    """Parse command-line arguments.

    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        description="Super Signal - Advanced stock analysis with risk factor detection"
    )

    parser.add_argument(
        "--ticker",
        "-t",
        type=str,
        help="Ticker symbol to screen (skips interactive mode)"
    )

    parser.add_argument(
        "--log-level",
        "-l",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Set logging level (default: INFO)"
    )

    # Future: Add --gui flag for desktop application
    # parser.add_argument(
    #     "--gui",
    #     action="store_true",
    #     help="Launch GUI interface instead of CLI"
    # )

    return parser.parse_args()


def main():
    """Main application entry point."""
    # Parse command-line arguments
    args = parse_arguments()

    # Set up logging
    setup_logging()

    # Launch CLI interface
    try:
        if args.ticker:
            # Single ticker mode
            from .cli import run_for_ticker
            success = run_for_ticker(args.ticker)
            sys.exit(0 if success else 1)
        else:
            # Interactive mode
            run_cli()
            sys.exit(0)

    except KeyboardInterrupt:
        print("\nInterrupted by user")
        sys.exit(0)

    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
