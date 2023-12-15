# Copyright (C) 2023, Bank of America.  The file below is licensed to LSC for use with HSoF.  All other rights are reserved.
"""This file defines the miscellaneous backend objects and their base class"""
class BackendObjectBase:
    """a base class for all backend objects. This class defines the common routines that are shared among all backend objects."""
    def __init__(self, backend_def):
        from backend._shared import term_2_period

        self.type = backend_def['type']
        self.amount = backend_def['amt']*1.0 # convert to float
        self.title = backend_def['title']
        self.start_period = backend_def['start_period']
        self.is_happiness_spending = backend_def['happiness_spending'] if 'happiness_spending' in backend_def else False
        self.category = backend_def['category']

        self.pay_freq_n_periods = backend_def['pay_freq_n_periods']
        self.term, self.term_unit = backend_def['term'], backend_def['term_unit']

        self.n_periods = term_2_period(backend_def['term'], backend_def['term_unit'])
        self.n_payments = self.n_periods / backend_def['pay_freq_n_periods']

class HappinessAdjustmentRatio(BackendObjectBase):
    """Represents a direct impact on happiness outside of the influence of wealth and spending. 
    This class has no schedule filed and is only a data holder with no simulation logic. 
    The actual happiness adjustment is implemented in Player class."""
    def __init__(self, backend_def):

        if backend_def['type'] != 'har':
            raise Exception('backend_def.type must be "har" to for the HappinessAdjustmentRatio class.')

        super().__init__(backend_def)

        self.adjRate = self.amount




