# Copyright (C) 2023, Bank of America.  The file below is licensed to LSC for use with HSoF.  All other rights are reserved.
 Copyright (C) 2023, Bank of America.  The file below is licensed to LSC for use with HSoF.  All other rights are reserved.
""This file defines backend object classes are in the income category"""

from collections import defaultdict
from backend.othrbkendobj import BackendObjectBase
class Salary(BackendObjectBase):
    """Represents Salary provided by an event."""

    def __init__(self, backend_def):
        """Represents Salary provided by an event.
        
        Input Argument
        --------------
        backend_def:    dict of values needed for this class.
        """

        from backend._shared import periodic_amount

        if backend_def['type'] != 'salary':
            raise Exception('backend_def.type must be "salary" to for the Salary class.')
        
        super().__init__(backend_def)

        self.pay_check = round(periodic_amount(self.amount, backend_def['pay_freq_n_periods'], amt_quote_term=backend_def['amt_quote_term']),2)

        self.calculate_schedule()
        
    def calculate_schedule(self):
        """Calculates the schedule table for the life of the salary.

        Each row of the table represents a simulation period. The rows are 0-indexed. 
        To convert to the global simulation period index, add self.start_period to the table row index.

        This table has one column whose value is the amount the salary pays out in a simulation period.
        """

        paysch = defaultdict(list)
        # loop through each simulation period
        for iPeriod in range(self.n_periods):
            
            if (1+iPeriod) % self.pay_freq_n_periods == 0: 
                #if the current simulation period has a pay check
                pay = self.pay_check
            else: # if the simulation period does not have a pay check
                pay = 0
            paysch['pay'].append(pay)

        self.schedule = paysch

class Asset(BackendObjectBase):
    """Represents a piece of asset provided by an event."""

    def __init__(self, backend_def):
        """Represents a piece of asset provided by an event.
        
        Input Argument
        --------------
        backend_def:    dict of values needed for this class.
        """

        from backend._shared import periodic_amount

        if backend_def['type'] != 'asset':
            raise Exception('backend_def.type must be "asset" to for the Asset class.')
        
        super().__init__(backend_def)

        if 'value_cap' in backend_def:
            self.value_cap = backend_def['value_cap']
        else:
            self.value_cap = 0
        
        self.annual_rate = backend_def['annual_rate']
        self.periodic_rate = periodic_amount(self.annual_rate, self.pay_freq_n_periods)
        if 'recurring_n_periods' in backend_def:
            self.recurring_n_periods = backend_def['recurring_n_periods']
            self.recurring_end_period = backend_def['recurring_end_period']
        else:
            self.recurring_n_periods, self.recurring_end_period = 0, 0

        self.calculate_schedule()
    
    def calculate_schedule(self):
        """Calculates the schedule table for the life of this asset.
        
        Each row of the table represents a simulation period. The rows are 0-indexed. 
        To convert to the global simulation period index, add self.start_period to the table row index.

        The table has the following columns:
        value_init:             the asset value at the beginning of a simulation period before value appreciation
        value_end:              the asset value at the end of a simulation period after the value appreciation has occurred during the period
        appreciation:           the appreciation value that occurred during the simulation period
        total_appreciation:     the total appreciation value up to a a period
        pay:                    the amount of cash the asset pays in a simulation period
        """

        # calculate the income schedule
        paysch = defaultdict(list)
        bal_init, bal_end, tot_app = self.amount, self.amount, 0
        for iPeriod in range(self.n_periods):
            # recurring investment period
            if self.recurring_n_periods!=0 and iPeriod !=0 and iPeriod % self.recurring_n_periods == 0 and iPeriod+self.start_period <= self.recurring_end_period:
                bal_init += self.amount

            if (1+iPeriod) % self.pay_freq_n_periods == 0: 
                # if pay period
                bal_end = round(bal_init * (1+self.periodic_rate),2)
                if self.value_cap != 0 and bal_end > self.value_cap:
                    bal_end = self.value_cap
                income = round(bal_end - bal_init,2)
                tot_app += income
            paysch['value_init'].append(bal_init)
            paysch['value_end'].append(bal_end)
            paysch['appreciation'].append(income)
            paysch['total_appreciation'].append(tot_app)
            paysch['pay'].append(0)
            bal_init = bal_end

        # for the last period, we liquidate the asset 
        paysch['pay'][-1] = paysch['value_end'][-1]
        paysch['value_end'][-1] = 0
        
        self.schedule = paysch

