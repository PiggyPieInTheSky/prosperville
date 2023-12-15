# Copyright (C) 2023, Bank of America.  The file below is licensed to LSC for use with HSoF.  All other rights are reserved.
 Copyright (C) 2023, Bank of America.  The file below is licensed to LSC for use with HSoF.  All other rights are reserved.
""This file defines the Expense backend object class."""

from backend.othrbkendobj import BackendObjectBase

class Expense(BackendObjectBase):
    """Represents an Expense item from an event."""

    def __init__(self, backend_def):
        """Represents an Expense item from an event.
        
        Input Argument
        --------------
        backend_def:    dict of values needed for this class.
        """

        from backend._shared import term_2_period, periodic_amount

        if backend_def['type'] != 'expense':
            raise Exception('backend_def.type must be "expense" to for the Expense class.')
        
        super().__init__(backend_def)

        self.amt_annual_rate = backend_def['annual_rate']
        self.rate_freq, self.rate_freq_unit = backend_def['rate_freq'], backend_def['rate_freq_unit']
        if self.amt_annual_rate == 0:
            self.periodic_amt__rate = 0
        else:
            self.rate_freq_n_periods = term_2_period(self.rate_freq, self.rate_freq_unit)
            self.periodic_amt__rate = periodic_amount(self.amt_annual_rate, self.rate_freq_n_periods)

        self.calculate_schedule()
    
    def calculate_schedule(self):
        """Calculates the schedule table for the life of this expense item.
        
        Each row of the table represents a simulation period. The rows are 0-indexed. 
        To convert to the global simulation period index, add self.start_period to the table row index.

        This table has one column whose value is the expense amount for a simulation period.
        """

        from collections import defaultdict
        
        crnt_pay = self.amount
        
        # calculate the expense schedule
        paysch = defaultdict(list)
        # cum_pay = 0
        for iPeriod in range(self.n_periods):
            
            if self.amt_annual_rate !=0 and iPeriod >= self.rate_freq_n_periods and iPeriod % self.rate_freq_n_periods == 1:
                crnt_pay = round((1+self.periodic_amt__rate) * crnt_pay,2)

            if (1+iPeriod) % self.pay_freq_n_periods == 0: 
                #if payment period
                pay = crnt_pay
            else: # if not payment period
                pay = 0
            paysch['pay'].append(pay)

        self.schedule = paysch

