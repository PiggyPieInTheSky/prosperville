# Copyright (C) 2023, Bank of America.  The file below is licensed to LSC for use with HSoF.  All other rights are reserved.
 Copyright (C) 2023, Bank of America.  The file below is licensed to LSC for use with HSoF.  All other rights are reserved.
"""This file defines common elements that are shared among backend files."""

from backend.design import NPeriodsPerMonth # number of simulation periods in a month

def term_2_period(term, term_unit):
    """Converts a term from event definition to number of periods."""
    if term_unit == 'yr':
        return term * 12 * NPeriodsPerMonth
    elif term_unit == 'mth':
        return term * NPeriodsPerMonth
    elif term_unit == 'prd':
        return term
    else:
        raise Exception(f'Unrecognized term_unit "{term_unit}".')

def periodic_amount(amount, pay_freq=1, amt_quote_term='annual'):
    """Converts an amount to its a value suitable for a single simulation period."""
    if amt_quote_term == 'annual':
        return amount * pay_freq / (12 * NPeriodsPerMonth)
    elif amt_quote_term == 'one-time':
        return amount
    else:
        raise Exception(f'Unrecognized amt_quote_term "{amt_quote_term}".')

