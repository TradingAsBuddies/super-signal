"""Text formatter for terminal output with ANSI colors.

This formatter wraps the existing display functions to produce
colored terminal output (current default behavior).
"""

from typing import Optional

from .base import BaseFormatter
from .display import (
    format_header,
    format_risk_flags,
    format_basic_info,
    format_headquarters,
    format_ownership_info,
    format_price_info,
    format_trading_info,
    format_financial_info,
    format_company_info,
    format_timestamp,
    format_executives,
    format_risk_details,
    format_vix,
)
from ..models import StockInfo, RiskAnalysis
from ..config import DISPLAY_CONFIG, FIELD_LABELS


class TextFormatter(BaseFormatter):
    """Formatter that produces ANSI-colored text output for terminals."""

    def format(
        self,
        stock_info: StockInfo,
        risk_analysis: RiskAnalysis,
        float_threshold: int,
        vix_value: Optional[float] = None
    ) -> str:
        """Format stock data as colored terminal text.

        Args:
            stock_info: Stock information data
            risk_analysis: Risk analysis results
            float_threshold: Minimum float threshold for risk highlighting
            vix_value: Current VIX index value (optional)

        Returns:
            ANSI-colored text string for terminal display
        """
        sections = [
            format_header(stock_info.ticker),
            format_risk_flags(risk_analysis),
            format_basic_info(stock_info),
            format_headquarters(stock_info),
            format_ownership_info(stock_info),
            format_price_info(stock_info),
            format_trading_info(stock_info, float_threshold),
            format_financial_info(stock_info),
            format_company_info(stock_info),
            format_timestamp(),
        ]

        if vix_value is not None:
            sections.append(f"{FIELD_LABELS['vix']:20}: {format_vix(vix_value)}")

        sections.append("")
        sections.append(format_executives(stock_info.directors))
        sections.append(DISPLAY_CONFIG.horizontal_line * DISPLAY_CONFIG.summary_width)

        if risk_analysis.has_risks:
            sections.append(format_risk_details(risk_analysis))

        return "\n".join(sections)
