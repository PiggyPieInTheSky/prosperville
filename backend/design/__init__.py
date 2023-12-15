# Copyright (C) 2023, Bank of America.  The file below is licensed to LSC for use with HSoF.  All other rights are reserved.
 Copyright (C) 2023, Bank of America.  The file below is licensed to LSC for use with HSoF.  All other rights are reserved.
 defines number of simulation periods per month
NPeriodsPerMonth = 2
# max number of time periods for the backend simulation
# we assume the life expectancy is 86 years old, each year has 48=4*12 weeks. 18 is the simulaiton starting age. The whole game simulates 70 years
MaxPeriods = NPeriodsPerMonth * 12 * (87-18+1)

