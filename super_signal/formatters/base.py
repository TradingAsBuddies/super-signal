"""Base formatter classes for stock output.

This module provides the abstract base class for formatters and
a factory function to get the appropriate formatter.
"""

from abc import ABC, abstractmethod
from typing import Optional

from ..models import StockInfo, RiskAnalysis


class BaseFormatter(ABC):
    """Abstract base class for stock data formatters.

    Subclasses must implement the format() method to convert
    stock data into a specific output format.
    """

    @abstractmethod
    def format(
        self,
        stock_info: StockInfo,
        risk_analysis: RiskAnalysis,
        float_threshold: int,
        vix_value: Optional[float] = None
    ) -> str:
        """Format stock data into the desired output format.

        Args:
            stock_info: Stock information data
            risk_analysis: Risk analysis results
            float_threshold: Minimum float threshold for risk highlighting
            vix_value: Current VIX index value (optional)

        Returns:
            Formatted string output
        """
        pass


def get_formatter(format_type: str) -> BaseFormatter:
    """Factory function to get the appropriate formatter.

    Args:
        format_type: Output format type ('text', 'json', or 'csv')

    Returns:
        Formatter instance for the specified format

    Raises:
        ValueError: If format_type is not supported
    """
    from .text_formatter import TextFormatter
    from .json_formatter import JsonFormatter
    from .csv_formatter import CsvFormatter

    formatters = {
        'text': TextFormatter,
        'json': JsonFormatter,
        'csv': CsvFormatter,
    }

    if format_type not in formatters:
        valid_formats = ', '.join(sorted(formatters.keys()))
        raise ValueError(
            f"Unsupported format: '{format_type}'. "
            f"Valid formats are: {valid_formats}"
        )

    return formatters[format_type]()
