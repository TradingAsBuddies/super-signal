"""Command-line interface for the stock screener.

This module provides the interactive CLI for running stock screenings
with colored terminal output.
"""

import os
import sys
import logging

from .fetchers.yahoo_finance import fetch_stock_info, fetch_vix, is_adr_yahoo
from .fetchers.finviz import determine_adr_status, get_directors
from .analyzers import analyze_stock_risks
from .formatters.display import print_stock_summary
from .config import ANSIColor, RED_FLAGS, DISPLAY_CONFIG

logger = logging.getLogger("super_signal.cli")


def clear_screen() -> None:
    """Clear terminal screen (Windows / Unix compatible)."""
    os.system("cls" if os.name == "nt" else "clear")


def set_console_title(title: str) -> None:
    """Set the console window title (Windows only).

    Args:
        title: Title to set for the console window
    """
    if os.name == "nt":
        os.system(f"title {title}")


def run_for_ticker(ticker_symbol: str) -> bool:
    """Run stock screening for a single ticker.

    Args:
        ticker_symbol: Stock ticker symbol to screen

    Returns:
        True if successful, False if an error occurred
    """
    ticker_symbol = ticker_symbol.strip().upper()
    if not ticker_symbol:
        print("No ticker entered; skipping.", file=sys.stderr)
        return False

    try:
        logger.info(f"Starting screening for {ticker_symbol}")

        # Fetch stock info from Yahoo Finance
        stock_info = fetch_stock_info(ticker_symbol)

        if stock_info is None:
            print(
                f"Error: Unable to retrieve data for {ticker_symbol}",
                file=sys.stderr
            )
            logger.error(f"Failed to fetch stock info for {ticker_symbol}")
            return False

        # Determine ADR status
        yahoo_adr_check = is_adr_yahoo(stock_info)
        stock_info.is_adr = determine_adr_status(ticker_symbol, yahoo_adr_check)

        # Get directors
        stock_info.directors = get_directors(
            ticker_symbol,
            max_count=DISPLAY_CONFIG.directors_max_count
        )

        # Analyze risks
        risk_analysis = analyze_stock_risks(stock_info)

        # Fetch VIX index
        vix_value = fetch_vix()

        # Display results
        print_stock_summary(
            stock_info,
            risk_analysis,
            RED_FLAGS.min_free_float,
            vix_value
        )

        logger.info(f"Successfully completed screening for {ticker_symbol}")
        return True

    except KeyboardInterrupt:
        print("\nOperation cancelled by user.", file=sys.stderr)
        logger.info("User cancelled operation")
        return False

    except Exception as e:
        print(f"Error retrieving data for {ticker_symbol}: {e}", file=sys.stderr)
        logger.exception(f"Unexpected error screening {ticker_symbol}")
        return False


def run_cli() -> None:
    """Run the interactive command-line interface.

    Continuously prompts for ticker symbols and displays stock information
    until the user presses Enter without input.
    """
    # Set console title
    set_console_title("Super Signal")

    logger.info("Starting CLI interface")

    try:
        while True:
            ticker_symbol = input(
                f"{ANSIColor.CYAN.value}\nEnter Stock Symbol "
                f"(or press Enter to quit):{ANSIColor.RESET.value}"
            ).strip()

            if not ticker_symbol:
                print(f"{ANSIColor.CYAN.value}Exiting.{ANSIColor.RESET.value}")
                logger.info("User exited CLI")
                break

            clear_screen()
            run_for_ticker(ticker_symbol)

    except KeyboardInterrupt:
        print(f"\n{ANSIColor.CYAN.value}Exiting.{ANSIColor.RESET.value}")
        logger.info("CLI interrupted by user")

    except Exception as e:
        print(f"\nFatal error: {e}", file=sys.stderr)
        logger.exception("Fatal error in CLI")
        sys.exit(1)
