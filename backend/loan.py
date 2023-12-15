# Copyright (C) 2023, Bank of America.  The file below is licensed to LSC for use with HSoF.  All other rights are reserved.
 Copyright (C) 2023, Bank of America.  The file below is licensed to LSC for use with HSoF.  All other rights are reserved.
"""""
from collections import defaultdict
from backend.othrbkendobj import BackendObjectBase

class Loan(BackendObjectBase):
    """Represents loan provided by an event that requires fixed amount of payment over a the life of the loan."""

    def __init__(self, backend_def):
        """Represents loan provided by an event that requires fixed amount of payment over a the life of the loan.
        
        Input Argument
        --------------
        backend_def:    dict of values needed for this class.
        """

        from backend._shared import periodic_amount
        import math

        if backend_def['type'] != 'loan':
            raise Exception('backend_def.type must be "loan" to for the Loan class.')
        
        super().__init__(backend_def)
        
        self.annual_rate = backend_def['annual_rate'] # this is the interest rate charged on the loan
        if self.annual_rate == 0:
            self.periodic_rate = 0
            self.periodic_payment_amt = math.ceil(self.amount / self.n_payments * 100) / 100.0
        else:
            self.periodic_rate = periodic_amount(self.annual_rate, self.pay_freq_n_periods)
            # calculate the payment amount for each payment period. Note payment period is not necessarily 1 simulation period. 
            # you may find the calculation explained here:
            # https://en.wikipedia.org/wiki/Amortization_calculator
            self.periodic_payment_amt = math.ceil(self.amount * self.periodic_rate / (1-(1+self.periodic_rate)**(-self.n_payments))*100)/100.0
        
        self.calculate_schedule()

    def calculate_schedule(self):
        """Calculates the schedule / amortization table for the life of the loan. 
        
        Each row of the table represents a simulation period. The rows are 0-indexed. 
        To convert to the global simulation period index, add self.start_period to the table row index.
        
        The table has the following columns:
        bal_init:           loan principal at the beginning of the simulation period before loan payment
        bal_end:            loan principal amount at the end of the simulation period after the payment is made
        payment:            amount of loan payment made in a simulation period
        payment_interest:   amount of loan payment that pays the interest
        payment_principal:  amount of loan payment that pays down the principal for a simulation period
        interest:           total interest paid up to a simulation period.
        pay:                =payment.
        """

        paysch = defaultdict(list)
        bal_init, bal_end, tot_int = self.amount, self.amount, 0
        # loop through each simulation period
        for iPeriod in range(self.n_periods):
            
            if (1+iPeriod) % self.pay_freq_n_periods == 0: # if the simulation period is a payment period
                # calculate the initial balance / principal at the beginning of a simulation period
                bal_init = round(bal_end * (1+self.periodic_rate),2)
                # use the payment amount per payment period if there is more than that amount left to be paid. otherwise, payment amount = the remaining balance.
                payment = min(self.periodic_payment_amt, bal_init)
                # interest payment: the amount of payment that contributes to paying the interest
                pay_int = round(bal_end * self.periodic_rate,2)
                # principal / loan balance at the end of the simulation period (after payment). 
                # this amount reduces how much you still owe on the loan
                bal_end = bal_init - payment
                # principal payment: the amount of payment that contributes to paying down the principal
                pay_prcpl = payment - pay_int
                # total interest since the beginning of the loan
                tot_int += pay_int
            else: # if the simulation period is not payment period
                # set payment variables to 0 for this period.
                pay_int = pay_prcpl = payment = 0

            # add the values to a row of each of the following columns    
            paysch['bal_init'].append(bal_init)
            paysch['bal_end'].append(bal_end)
            paysch['payment'].append(payment)
            paysch['payment_interest'].append(pay_int)
            paysch['payment_principal'].append(pay_prcpl)
            paysch['interest'].append(tot_int)
            paysch['pay'].append(payment)
            
        self.schedule = paysch

