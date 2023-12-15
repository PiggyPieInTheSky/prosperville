# Copyright (C) 2023, Bank of America.  The file below is licensed to LSC for use with HSoF.  All other rights are reserved.
 Copyright (C) 2023, Bank of America.  The file below is licensed to LSC for use with HSoF.  All other rights are reserved.
""This file defines events and their options for the game. See section "Option Backend Definition Manifest" code documentation for more details."""

from collections import namedtuple

# define a structure that can describe an event
stctEvent = namedtuple('stctEvent', 'name title options desc tip backend')
# define a structure that can describe an option
stctOption = namedtuple('stctOption', 'name title image desc backend')

# a list of all events. Order of the events does not matter
pvEvents = [
    # stage 1 event -- car purchase
    stctEvent(name='stg1_car', title='Do you want to buy a car?', desc=''
                  , options=[
                      stctOption(name='stg1_car_none', title='No car', image='res/walk_icon1.png'
                                 , desc='Although life without a car can be a little difficult, the lack of financial burden might be worth considering.\nThis option can reduce your raw happiness score by 5% until the end of this stage.'
                                 , backend=[{'type':'har', 'category':'car', 'title':'no car happiness reduction', 'amt':0.95, 'amt_quote_term':'one-time', 'pay_freq_n_periods':1, 'term':4, 'term_unit':'yr', 'start_period':0}]
                                )
                      , stctOption(name='stg1_car_cheap', title='Second Hand Car', image='res/car_icon1.png'
                                 , desc='A second hand car costs $5,000. The value immediately drops to $2,500 once you bought it. \n\nTo finance the purchase, you will need to take out a 5-year fixed-rate loan at 6.5% annual interest rate.\n\nThe required monthly loan payment is $97.84.\nTotal interest you will pay over the life of the loan is $869.73.'
                                 , backend=[
                                     # car loan
                                     {'type':'loan', 'category':'car', 'title':'car loan', 'amt':5000, 'amt_quote_term':'one-time', 'term':5, 'term_unit':'yr', 'annual_rate':0.065, 'pay_freq_n_periods':2, 'start_period':0, 'happiness_spending':True}
                                     # depreciating car value
                                     , {'type':'asset', 'category':'car', 'title':'second hand car', 'amt':2500, 'annual_rate':-0.15, 'pay_freq_n_periods':1, 'start_period':0, 'term':5, 'term_unit':'yr', 'happiness_spending':False}
                                 ]
                                )
                      , stctOption(name='stg1_car_mid', title='New Sedan (Mid-tier)', image='res/car_icon1.png'
                                   , desc='This car costs $20,000. The value immediately drops to $16,000 once you bought it. \n\nTo finance the purchase, you will need to take out a 5-year fixed-rate loan at 6.5% annual interest rate.\n\nThe required monthly loan payment is $331.46.\nTotal interest you will pay over the life of the loan is $3864.96.'
                                   , backend=[
                                        {'type':'loan', 'category':'car', 'title':'car loan', 'amt':20000, 'amt_quote_term':'one-time', 'term':5, 'term_unit':'yr', 'annual_rate':0.065, 'pay_freq_n_periods':2, 'start_period':0, 'happiness_spending':True}
                                        , {'type':'asset', 'category':'car', 'title':'second hand car', 'amt':16000, 'annual_rate':-0.15, 'pay_freq_n_periods':1, 'start_period':0, 'term':5, 'term_unit':'yr', 'happiness_spending':False}
                                   ]
                                  )
                      , stctOption(name='stg1_car_exp', title='New SUV', image='res/car_icon1.png'
                                   , desc='This car costs $40,000.  The value immediately drops to $32,000 once you bought it. \n\nTo finance the purchase, you will need to take out a 5-year fixed-rate loan at 6.5% annual interest rate.\n\nThe required monthly loan payment is $662.92.\nTotal interest you will pay over the life of the loan is $7729.92.'
                                   , backend=[
                                        {'type':'loan', 'category':'car', 'title':'car loan', 'amt':40000, 'amt_quote_term':'one-time', 'term':5, 'term_unit':'yr', 'annual_rate':0.065, 'pay_freq_n_periods':2, 'start_period':0, 'happiness_spending':True}
                                        , {'type':'asset', 'category':'car', 'title':'second hand car', 'amt':32000, 'annual_rate':-0.15, 'pay_freq_n_periods':1, 'start_period':0, 'term':5, 'term_unit':'yr', 'happiness_spending':False}
                                   ]
                                  )
                  ]
                  , tip='', backend=None
    )
    # stage 1 event -- higher ed
    , stctEvent(name='stg1_college', title='What is your plan after high school?', desc=''
                , options=[
                    # there is special logic to turn off the dorm option in 'stg1_lodging' event if 'stg1_no_college' is chosen
                    # see Player.__on_set_choice class method in backend/player.py for the special logic
                    stctOption(name='stg1_no_college', title='First job full time', image='res/desk_icon1.png'
                                    , desc='Annual income: $20,000. Paid bi-weekly at $1,666.67. '
                                    , backend={'type':'salary', 'category':'income', 'title':'salary', 'amt':20000, 'amt_quote_term':'annual', 'pay_freq_n_periods':1, 'term':4, 'term_unit':'yr', 'start_period':0}
                              )
                    , stctOption(name='stg1_college_public_in_state', title='In-State Public University', image='res/college_icon1.png'
                                    , desc='Student loan amount: 25,000. Monthly payment: $277.56. Total interest: $8,305.86.\n\nYou receive $400 monthly allowance.'
                                    , backend=[
                                        # student loan
                                        {'type':'loan', 'category':'student', 'title':'student loan', 'amt':25000, 'amt_quote_term':'one-time', 'term':10, 'term_unit':'yr', 'annual_rate':0.06, 'pay_freq_n_periods':2, 'start_period':96, 'happiness_spending':False}
                                        # student loan allowance
                                        , {'type':'salary', 'category':'income', 'title':'student loan benefit', 'amt':4800, 'amt_quote_term':'annual', 'pay_freq_n_periods':2, 'term':4, 'term_unit':'yr', 'start_period':0}
                                    ]
                              )
                    , stctOption(name='stg1_college_public_out_state', title='Out-of-State Public University', image='res/college_icon1.png'
                                    , desc='Student loan amount: 50,000. Monthly payment: $555.11. Total interest: $16,611.94.\n\nYou receive $600 monthly allowance.'
                                    , backend=[
                                        # student loan
                                        {'type':'loan', 'category':'student', 'title':'student loan', 'amt':50000, 'amt_quote_term':'one-time', 'term':10, 'term_unit':'yr', 'annual_rate':0.06, 'pay_freq_n_periods':2, 'start_period':96, 'happiness_spending':False}
                                        # student loan allowance
                                        , {'type':'salary', 'category':'income', 'title':'student loan benefit', 'amt':7200, 'amt_quote_term':'annual', 'pay_freq_n_periods':2, 'term':4, 'term_unit':'yr', 'start_period':0}
                                    ]
                                )
                    , stctOption(name='stg1_college_ivy_league', title='Ivy League', image='res/college_icon1.png'
                                    , desc='Student loan amount: 150,000. Monthly payment: $1,665.31. Total interest: $49,836.85.\n\nYou receive $1000 monthly allowance.'
                                    , backend=[
                                        # student loan
                                        {'type':'loan', 'category':'student', 'title':'student loan', 'amt':150000, 'amt_quote_term':'one-time', 'term':10, 'term_unit':'yr', 'annual_rate':0.06, 'pay_freq_n_periods':2, 'start_period':96, 'happiness_spending':False}
                                        # student loan allowance
                                        , {'type':'salary', 'category':'income', 'title':'student loan benefit', 'amt':12000, 'amt_quote_term':'annual', 'pay_freq_n_periods':2, 'term':4, 'term_unit':'yr', 'start_period':0}
                                    ]
                                )
                ]
                , tip='', backend=None
    )
    # stage 1 event -- part time job
    , stctEvent(name='stg1_part_time_job', title='Would you want to take a part time job?', desc=''
                , options=[
                    stctOption(name='stg1_part_time_job_no', title='No part time job', image='res/book_icon1.png'
                                     , desc='Life is difficult as it is. Why adding more?'
                                     , backend=None
                              )
                    , stctOption(name='stg1_part_time_job_yes', title='Yes to a part time job', image='res/suitcase_icon1.png'
                                     , desc='This job pays $250 twice a month. \n\nThe job reduces your raw happiness value by 5% until the end of the stage.'
                                     , backend=[
                                        # income definition
                                        {'type':'salary', 'category':'income', 'title':'post high school part time job', 'amt':6000, 'amt_quote_term':'annual', 'pay_freq_n_periods':2, 'term':4, 'term_unit':'yr', 'start_period':0}
                                        # adjust happiness directly
                                        , {'type':'har', 'category':'happiness', 'title':'happiness reduction', 'amt':0.95, 'amt_quote_term':'one-time', 'pay_freq_n_periods':1, 'term':4, 'term_unit':'yr', 'start_period':0}
                                     ]
                              )
                ]
                , tip='', backend=None
    )
    # stage 1 event -- lodging
    , stctEvent(name='stg1_lodging', title='Lodging', desc=''
                # due to the special logic to turn off 'stg1_lodging_dorm' option when a player chooses 'stg1_no_college' option in 'stg1_college' event,
                # the options list in this event is ordered. please do not change the order of the options
                # see Player.__on_set_choice class method in backend/player.py
                , options=[
                    stctOption(name='stg1_lodging_dorm', title='Dorm', image='res/bed_icon1.png'
                                     , desc='Living in the dorm costs $1800 every 6 months. \n\nThis option is not available if you did not choose to go to college in the previous screen.'
                                     , backend={'type':'expense', 'category':'housing', 'title':'dorm', 'amt':1800, 'amt_quote_term':'one-time', 'pay_freq_n_periods':12, 'term':4, 'term_unit':'yr', 'start_period':0, 'happiness_spending':True, 'annual_rate':0, 'rate_freq':1, 'rate_freq_unit':'yr'}
                              )
                    , stctOption(name='stg1_lodging_off_campus_shared', title='Off campus with roommates', image='res/tall_building_icon1.png'
                                     , desc='Staying off campus with roommates costs $250/month paid monthly.'
                                     , backend={'type':'salary', 'category':'housing', 'title':'Off campus with roommates', 'amt':500, 'amt_quote_term':'one-time', 'pay_freq_n_periods':2, 'term':4, 'term_unit':'yr', 'start_period':0}
                              )
                    , stctOption(name='stg1_lodging_off_campus_single', title='Off campus by yourself', image='res/tall_building_icon2.png'
                                     , desc='Staying off campus by yourself costs $500/month paid monthly.'
                                     , backend={'type':'salary', 'category':'housing', 'title':'Off campus by yourself', 'amt':1000, 'amt_quote_term':'one-time', 'pay_freq_n_periods':2, 'term':4, 'term_unit':'yr', 'start_period':0}
                              )
                ]
                , tip='', backend=None
    )

    # stage 2 ============================
    
    # stage 2 event -- job offer
    , stctEvent(name='stg2_firstjob', title='Which job do you want to take?', desc=''
                , options=[
                    stctOption(name='stg2_firstjob_opt1', title='Job offer 2.1: Low Stress', image='res/money_icon1.png'
                                     , desc='Annual income is $25,000. Monthly income is $1,667 paid biweekly. \n\n 10% income boost ($2,292/mth) if you went to a public college. \n\n15% income boost ($2,395/mth) if you went to an Ivy league college. \n\n1% increase in raw happiness score until the end of the life stage.'
                                     , backend=[
                                        {'type':'salary', 'category':'income', 'title':'salary', 'amt':25000, 'amt_quote_term':'annual', 'pay_freq_n_periods':1, 'term':15, 'term_unit':'yr', 'start_period':96}
                                        , {'type':'har', 'category':'happiness', 'title':'happiness increase', 'amt':1.01, 'amt_quote_term':'one-time', 'pay_freq_n_periods':1, 'term':15, 'term_unit':'yr', 'start_period':96}
                                        # mandatory stage wide spending
                                        , {'type':'expense', 'category':'spending', 'title':'Stage 2 Mandatory Spending', 'amt':500, 'amt_quote_term':'one-time', 'pay_freq_n_periods':2, 'term':15, 'term_unit':'yr', 'start_period':96, 'happiness_spending':False, 'annual_rate':0.0, 'rate_freq':1, 'rate_freq_unit':'yr'}
                                     ]
                              )
                    , stctOption(name='stg2_firstjob_opt2', title='Job offer 2.2', image='res/money_icon1.png'
                                     , desc='Annual income is $30,000. Monthly income is $2,500 paid biweekly.  \n\n 10% income boost ($2,750/mth) if you went to a public college. \n\n15% income boost ($2,870/mth) if you went to an Ivy league college.'
                                     , backend=[
                                        {'type':'salary', 'category':'income', 'title':'salary', 'amt':30000, 'amt_quote_term':'annual', 'pay_freq_n_periods':1, 'term':15, 'term_unit':'yr', 'start_period':96}
                                        # mandatory stage wide spending
                                        , {'type':'expense', 'category':'spending', 'title':'Stage 2 Mandatory Spending', 'amt':700, 'amt_quote_term':'one-time', 'pay_freq_n_periods':2, 'term':15, 'term_unit':'yr', 'start_period':96, 'happiness_spending':False, 'annual_rate':0.0, 'rate_freq':1, 'rate_freq_unit':'yr'}
                                     ]
                                )
                ]
                , tip='', backend=None
    )
    # stage 2 event -- house buying
    , stctEvent(name='stg2_firsthouse', title='Do you want to buy a house?', desc=''
                , options=[
                    stctOption(name='stg2_firsthouse_rent', title='Rent', image='res/tall_building_icon1.png'
                                     , desc='Monthly Rent: $800. \n\nRent increases annually by 5%.'
                                     , backend={'type':'expense', 'category':'rent', 'title':'Rent', 'amt':800, 'amt_quote_term':'one-time', 'pay_freq_n_periods':2, 'term':15, 'term_unit':'yr', 'start_period':0, 'happiness_spending':True, 'annual_rate':0.05, 'rate_freq':1, 'rate_freq_unit':'yr'}
                              )
                    , stctOption(name='stg2_firsthouse_small', title='Small House', image='res/house_icon1.png'
                                     , desc='House\nPrice: $200,000 \nAppreciation: 4% annual compounding \n\nMaintenance: \nCost: $160/month \nAnnual increase: 2% \n\nMortage \nPrincipal: $160,000 \nDown payment: $40,000 \nMonthly Payment: $718 \n Rate: 3.5% \nLength: 30 years \nTotal Interest: $98,647'
                                     , backend=[
                                         # mortgage
                                         {'type':'loan', 'category':'mortgage', 'title':'Mortgage 1', 'amt':160000, 'amt_quote_term':'one-time', 'term':30, 'term_unit':'yr', 'annual_rate':0.035, 'pay_freq_n_periods':2, 'start_period':96, 'happiness_spending':True}
                                         # house value appreciation
                                         , {'type':'asset', 'category':'house', 'title':'House 1', 'amt':200000, 'annual_rate':0.02, 'pay_freq_n_periods':1, 'start_period':96, 'term':66, 'term_unit':'yr', 'happiness_spending':True, 'value_cap':500000}
                                         # down payment
                                        , {'type':'expense', 'category':'down payment', 'title':'House 1 Down Payment', 'amt':40000, 'amt_quote_term':'one-time', 'pay_freq_n_periods':1, 'term':1, 'term_unit':'prd', 'start_period':96, 'happiness_spending':False, 'annual_rate':0, 'rate_freq':1, 'rate_freq_unit':'yr'}
                                        # monthly maintenance
                                         , {'type':'expense', 'category':'house', 'title':'House 2 Monthly Expense', 'amt':160, 'amt_quote_term':'one-time', 'pay_freq_n_periods':2, 'term':66, 'term_unit':'prd', 'start_period':96, 'happiness_spending':True, 'annual_rate':0.02, 'rate_freq':1, 'rate_freq_unit':'yr'}
                                     ]
                                )
                    , stctOption(name='stg2_firsthouse_mid', title='Medium House', image='res/house_icon1.png'
                                     , desc='House\nPrice: $300,000 \nAppreciation: 4% annual compounding \n\nMaintenance: \nCost: $250/month \nAnnual increase: 2% \n\nMortage \nPrincipal: $240,000 \nDown payment: $60,000 \nMonthly Payment: $1,078 \n Rate: 3.5% \nLength: 30 years \nTotal Interest: $147,974'
                                     , backend=[
                                         # mortgage
                                         {'type':'loan', 'category':'mortgage', 'title':'Mortgage 2', 'amt':240000, 'amt_quote_term':'one-time', 'term':30, 'term_unit':'yr', 'annual_rate':0.035, 'pay_freq_n_periods':2, 'start_period':96, 'happiness_spending':True}
                                         # house value appreciation
                                         , {'type':'asset', 'category':'house', 'title':'House 2', 'amt':300000, 'annual_rate':0.015, 'pay_freq_n_periods':1, 'start_period':96, 'term':66, 'term_unit':'yr', 'happiness_spending':True, 'value_cap':750000}
                                         # down payment
                                         , {'type':'expense', 'category':'down payment', 'title':'House 2 Down Payment', 'amt':60000, 'amt_quote_term':'one-time', 'pay_freq_n_periods':1, 'term':1, 'term_unit':'prd', 'start_period':96, 'happiness_spending':False, 'annual_rate':0, 'rate_freq':1, 'rate_freq_unit':'yr'}
                                         # monthly maintenance
                                         , {'type':'expense', 'category':'house', 'title':'House 2 Monthly Expense', 'amt':250, 'amt_quote_term':'one-time', 'pay_freq_n_periods':2, 'term':66, 'term_unit':'prd', 'start_period':96, 'happiness_spending':True, 'annual_rate':0.02, 'rate_freq':1, 'rate_freq_unit':'yr'}
                                     ]
                                )
                    , stctOption(name='stg2_house_big', title='Large House', image='res/house_icon1.png'
                                     , desc='House\nPrice: $800,000 \nAppreciation: 1% annual compounding \n\nMaintenance: \nCost: $1334/month \nAnnual increase: 2% \n\nMortage \nPrincipal: $640,000 \nDown payment: $160,000 \nMonthly Payment: $2,874 \n Rate: 3.5% \nLength: 30 years \nTotal Interest: $394,598'
                                     , backend=[
                                         # mortgage
                                         {'type':'loan', 'category':'mortgage', 'title':'Mortgage 5', 'amt':640000, 'amt_quote_term':'one-time', 'term':30, 'term_unit':'yr', 'annual_rate':0.035, 'pay_freq_n_periods':2, 'start_period':96, 'happiness_spending':True}
                                         # house value appreciation
                                         , {'type':'asset', 'category':'house', 'title':'House 5', 'amt':800000, 'annual_rate':0.01, 'pay_freq_n_periods':1, 'start_period':96, 'term':66, 'term_unit':'yr', 'happiness_spending':True, 'value_cap':2000000}
                                         # down payment
                                         , {'type':'expense', 'category':'down payment', 'title':'House 5 Down Payment', 'amt':160000, 'amt_quote_term':'one-time', 'pay_freq_n_periods':1, 'term':1, 'term_unit':'prd', 'start_period':96, 'happiness_spending':False, 'annual_rate':0, 'rate_freq':1, 'rate_freq_unit':'yr'}
                                         # monthly maintenance
                                         , {'type':'expense', 'category':'house', 'title':'House 5 Monthly Expense', 'amt':667, 'amt_quote_term':'one-time', 'pay_freq_n_periods':1, 'term':66, 'term_unit':'yr', 'start_period':96, 'happiness_spending':True, 'annual_rate':0.02, 'rate_freq':1, 'rate_freq_unit':'yr'}
                                     ]
                                )
                ]
                , tip='', backend=None
    )
    # stage 2 event - saving / investing
    , stctEvent(name='stg2_saving_program', title="How much do you want to invest monthly?", desc='You have extra $200 left every month. How do you want to spend?'
        , options=[
            stctOption(name='stg2_saving_none', title='$0/month', image='res/dance_icon1.png'
                , desc='YOLO! I don\'t want to invest any amount of my income in an investment account.'
                , backend={'type':'expense', 'category':'consumption', 'title':'spend $200 for fun', 'amt':200, 'amt_quote_term':'one-time', 'pay_freq_n_periods':2, 'term':15, 'term_unit':'yr', 'start_period':96, 'happiness_spending':True, 'annual_rate':0, 'rate_freq':1, 'rate_freq_unit':'yr'}
            )
            , stctOption(name='stg2_saving_opt1', title='$100/month', image='res/chart_icon1.png'
                , desc='Invest $100/month; spend $100/month. \n\nAnnual return is 6% compounding rate.'
                , backend=[
                    {'type':'expense', 'category':'transfer', 'title':'invest transfer $100/month', 'amt':100, 'amt_quote_term':'one-time', 'pay_freq_n_periods':2, 'term':15, 'term_unit':'yr', 'start_period':96, 'happiness_spending':False, 'annual_rate':0, 'rate_freq':1, 'rate_freq_unit':'yr'}
                    , {'type':'asset', 'category':'investment', 'title':'invest $100/month', 'amt':100, 'annual_rate':0.06, 'pay_freq_n_periods':1, 'start_period':96, 'term':66, 'term_unit':'yr', 'happiness_spending':False, 'recurring_n_periods':2, 'recurring_end_period':455}
                    , {'type':'expense', 'category':'consumption', 'title':'spend $100 for fun', 'amt':100, 'amt_quote_term':'one-time', 'pay_freq_n_periods':2, 'term':15, 'term_unit':'yr', 'start_period':96, 'happiness_spending':True, 'annual_rate':0, 'rate_freq':1, 'rate_freq_unit':'yr'}
                ]
            )
            , stctOption(name='stg2_saving_opt2', title='$200/month', image='res/chart_icon1.png'
                , desc='Invest $200/month. \n\nAnnual return is 6% compounding rate.'
                , backend=[
                    {'type':'expense', 'category':'transfer', 'title':'invest transfer $100/month', 'amt':200, 'amt_quote_term':'one-time', 'pay_freq_n_periods':2, 'term':15, 'term_unit':'yr', 'start_period':96, 'happiness_spending':False, 'annual_rate':0, 'rate_freq':1, 'rate_freq_unit':'yr'}
                    , {'type':'asset', 'category':'investment', 'title':'invest $200/month', 'amt':200, 'annual_rate':0.06, 'pay_freq_n_periods':1, 'start_period':96, 'term':66, 'term_unit':'yr', 'happiness_spending':False, 'recurring_n_periods':2, 'recurring_end_period':455}
                ]
            )
        ]
        , tip='', backend=None
    )
    # stage 2 -- car purchase
    , stctEvent(name='stg2_car', title='Car purchase', desc='Your previous car needs to be replaced after 5 years. Choose an option below.'
                , options=[
                    stctOption(name='stg2_car_2nd_hand', title='Second Hand Car', image='res/car_icon1.png'
                                , desc='This second hand car costs $10,000, depreciates by 20% annually. The value immeidately drops to $5,000 once you bought it. \n\nTo finance the purchase, you will need to take out a 5-year fixed-rate loan at 6.5% annual interest rate.\n\nThe required monthly loan payment is $195.67.\nTotal interest you will pay over the life of the loan is $1,739.63.'
                                , backend=[
                                    # car loan
                                    {'type':'loan', 'category':'car', 'title':'car loan', 'amt':10000, 'amt_quote_term':'one-time', 'term':5, 'term_unit':'yr', 'annual_rate':0.065, 'pay_freq_n_periods':2, 'start_period':144, 'happiness_spending':True}
                                    # depreciating car value
                                    , {'type':'asset', 'category':'car', 'title':'second hand car', 'amt':5000, 'annual_rate':-0.20, 'pay_freq_n_periods':1, 'start_period':144, 'term':14, 'term_unit':'yr', 'happiness_spending':False}
                                ]
                        )
                    , stctOption(name='stg2_car_mid', title='New Sedan (Mid-tier)', image='res/car_icon1.png'
                                , desc='This car costs $20,000, depreciates by 15% annually. The value immeidately drops to $16,000 once you bought it. \n\nTo finance the purchase, you will need to take out a 5-year fixed-rate loan at 6.5% annual interest rate.\n\nThe required monthly loan payment is $331.46.\nTotal interest you will pay over the life of the loan is $3,864.96.'
                                , backend=[
                                    {'type':'loan', 'category':'car', 'title':'car loan', 'amt':20000, 'amt_quote_term':'one-time', 'term':5, 'term_unit':'yr', 'annual_rate':0.065, 'pay_freq_n_periods':2, 'start_period':144, 'happiness_spending':True}
                                    , {'type':'asset', 'category':'car', 'title':'second hand car', 'amt':16000, 'annual_rate':-0.15, 'pay_freq_n_periods':1, 'start_period':144, 'term':14, 'term_unit':'yr', 'happiness_spending':False}
                                ]
                        )
                    , stctOption(name='stg2_car_exp', title='New SUV', image='res/car_icon1.png'
                                , desc='This car costs $40,000., depreciates by 15% annually. The value immeidately drops to $32,000 once you bought it. \n\nTo finance the purchase, you will need to take out a 5-year fixed-rate loan at 6.5% annual interest rate.\n\nThe required monthly loan payment is $662.92.\nTotal interest you will pay over the life of the loan is $7,729.92.'
                                , backend=[
                                    {'type':'loan', 'category':'car', 'title':'car loan', 'amt':40000, 'amt_quote_term':'one-time', 'term':5, 'term_unit':'yr', 'annual_rate':0.065, 'pay_freq_n_periods':2, 'start_period':144, 'happiness_spending':True}
                                    , {'type':'asset', 'category':'car', 'title':'second hand car', 'amt':32000, 'annual_rate':-0.15, 'pay_freq_n_periods':1, 'start_period':144, 'term':14, 'term_unit':'yr', 'happiness_spending':False}
                                ]
                        )
                    , stctOption(name='stg2_car_lux', title='New Luxury Car', image='res/car_icon1.png'
                                , desc='This car costs $100,000, depreciates by 20% annually.  The value immeidately drops to $70,000 once you bought it. \n\nTo finance the purchase, you will need to take out a 5-year fixed-rate loan at 6.5% annual interest rate.\n\nThe required monthly loan payment is $1,956.62.\nTotal interest you will pay over the life of the loan is $17,396.88.'
                                , backend=[
                                    {'type':'loan', 'category':'car', 'title':'car loan', 'amt':100000, 'amt_quote_term':'one-time', 'term':5, 'term_unit':'yr', 'annual_rate':0.065, 'pay_freq_n_periods':2, 'start_period':144, 'happiness_spending':True}
                                    , {'type':'asset', 'category':'car', 'title':'second hand car', 'amt':70000, 'annual_rate':-0.20, 'pay_freq_n_periods':1, 'start_period':144, 'term':14, 'term_unit':'yr', 'happiness_spending':False}
                                ]
                        )
                ]
                , tip='', backend=None
    )

    # stage 3 ==================================================
    # stage 3 event -- job offer
    , stctEvent(name='stg3_job_offers', title='Which job do you want to take?', desc=''
                , options=[
                    stctOption(name='stg3_job_offers_opt1', title='Job offer 3.1: Low Stress', image='res/money_icon1.png'
                                     , desc='Annual income is $50,000. Monthly income is $4,167 paid biweekly. \n\n1% increase in raw happiness score until the end of the life stage.'
                                     , backend=[
                                        {'type':'salary', 'category':'income', 'title':'salary', 'amt':50000, 'amt_quote_term':'annual', 'pay_freq_n_periods':1, 'term':20, 'term_unit':'yr', 'start_period':456}
                                        , {'type':'har', 'category':'happiness', 'title':'happiness increase', 'amt':1.01, 'amt_quote_term':'one-time', 'pay_freq_n_periods':1, 'term':20, 'term_unit':'yr', 'start_period':456}
                                        # mandatory stage wide spending
                                        , {'type':'expense', 'category':'spending', 'title':'Stage 3 Mandatory Spending', 'amt':700, 'amt_quote_term':'one-time', 'pay_freq_n_periods':1, 'term':20, 'term_unit':'yr', 'start_period':456, 'happiness_spending':False, 'annual_rate':0.02, 'rate_freq':1, 'rate_freq_unit':'yr'}
                                     ]
                              )
                    , stctOption(name='stg3_job_offers_opt2', title='Job offer 3.2: Average Pay', image='res/money_icon1.png'
                                     , desc='Annual income is $80,000. Monthly income is $6,667 paid biweekly.'
                                     , backend=[
                                        {'type':'salary', 'category':'income', 'title':'salary', 'amt':80000, 'amt_quote_term':'annual', 'pay_freq_n_periods':1, 'term':20, 'term_unit':'yr', 'start_period':456}
                                        # mandatory stage wide spending
                                        , {'type':'expense', 'category':'spending', 'title':'Stage 3 Mandatory Spending', 'amt':700, 'amt_quote_term':'one-time', 'pay_freq_n_periods':1, 'term':20, 'term_unit':'yr', 'start_period':456, 'happiness_spending':False, 'annual_rate':0.02, 'rate_freq':1, 'rate_freq_unit':'yr'}
                                     ]
                                )
                    , stctOption(name='stg3_job_offers_opt3', title='Job offer 3.3: High Stress', image='res/money_icon1.png'
                                     , desc='Annual income is $120,000. Monthly income is $10,000 paid biweekly.  \n\n5% reduction of the raw happiness score until the end of the life stage.'
                                     , backend=[
                                        {'type':'salary', 'category':'income', 'title':'salary', 'amt':120000, 'amt_quote_term':'annual', 'pay_freq_n_periods':1, 'term':20, 'term_unit':'yr', 'start_period':456}
                                        , {'type':'har', 'category':'happiness', 'title':'happiness increase', 'amt':0.95, 'amt_quote_term':'one-time', 'pay_freq_n_periods':1, 'term':20, 'term_unit':'yr', 'start_period':456}
                                        # mandatory stage wide spending
                                        , {'type':'expense', 'category':'spending', 'title':'Stage 3 Mandatory Spending', 'amt':700, 'amt_quote_term':'one-time', 'pay_freq_n_periods':1, 'term':20, 'term_unit':'yr', 'start_period':456, 'happiness_spending':False, 'annual_rate':0.02, 'rate_freq':1, 'rate_freq_unit':'yr'}
                                       ]
                                )
                ]
                , tip='', backend=None
    )
    # stage 3 event -- house buying. special logic in backend for this, together with 'stg2_firsthouse_rent' option in stage 2
    , stctEvent(name='stg3_house', title='Do you want to buy a house?', desc='If you bought a house in the previous stage, the house you are buying here is going to be a rental property. After maintenance and easy of renting (bigger houses are harder to rent), you average $2000/month as rental income.'
                , options=[
                    stctOption(name='stg3_house_small', title='Small House', image='res/house_icon1.png'
                                     , desc='House\nPrice: $250,000 \nAppreciation: 4% annual compounding \n\nMaintenance: \nCost: $600/month \nAnnual increase: 2% \n\nMortage \nPrincipal: $218,000 \nDown payment: $32,000 \nMonthly Payment: $979 \n Rate: 3.5% \nLength: 30 years \nTotal Interest: $134,410'
                                     , backend=[
                                         # mortgage
                                         {'type':'loan', 'category':'mortgage', 'title':'Mortgage 3', 'amt':218000, 'amt_quote_term':'one-time', 'term':30, 'term_unit':'yr', 'annual_rate':0.035, 'pay_freq_n_periods':2, 'start_period':456, 'happiness_spending':True}
                                         # house value appreciation
                                         , {'type':'asset', 'category':'house', 'title':'House 3', 'amt':250000, 'annual_rate':0.04, 'pay_freq_n_periods':1, 'start_period':96, 'term':51, 'term_unit':'yr', 'happiness_spending':True}
                                         # down payment
                                         , {'type':'expense', 'category':'down payment', 'title':'House 3 Down Payment', 'amt':32000, 'amt_quote_term':'one-time', 'pay_freq_n_periods':1, 'term':1, 'term_unit':'prd', 'start_period':456, 'happiness_spending':False, 'annual_rate':0, 'rate_freq':1, 'rate_freq_unit':'yr'}
                                         # monthly maintenance
                                         , {'type':'expense', 'category':'house', 'title':'House 3 Monthly Expense', 'amt':300, 'amt_quote_term':'one-time', 'pay_freq_n_periods':1, 'term':51, 'term_unit':'yr', 'start_period':456, 'happiness_spending':True, 'annual_rate':0.02, 'rate_freq':1, 'rate_freq_unit':'yr'}
                                         # rent income
                                         , {'type':'salary', 'category':'house', 'title':'House 3 Rental Income', 'amt':2000, 'amt_quote_term':'one-time', 'pay_freq_n_periods':2, 'term':51, 'term_unit':'yr', 'start_period':456, 'happiness_spending':False}
                                     ]
                                )
                    , stctOption(name='stg3_house_mid', title='Medium House', image='res/house_icon1.png'
                                     , desc='House\nPrice: $450,000 \nAppreciation: 4% annual compounding \n\nMaintenance: \nCost: $740/month \nAnnual increase: 2% \n\nMortage \nPrincipal: $360,000 \nDown payment: $90,000 \nMonthly Payment: $1,617 \n Rate: 3.5% \nLength: 30 years \nTotal Interest: $221,960'
                                     , backend=[
                                         # mortgage
                                         {'type':'loan', 'category':'mortgage', 'title':'Mortgage 4', 'amt':360000, 'amt_quote_term':'one-time', 'term':30, 'term_unit':'yr', 'annual_rate':0.035, 'pay_freq_n_periods':2, 'start_period':456, 'happiness_spending':True}
                                         # house value appreciation
                                         , {'type':'asset', 'category':'house', 'title':'House 4', 'amt':450000, 'annual_rate':0.04, 'pay_freq_n_periods':1, 'start_period':96, 'term':51, 'term_unit':'yr', 'happiness_spending':True}
                                         # down payment
                                         , {'type':'expense', 'category':'down payment', 'title':'House 4 Down Payment', 'amt':90000, 'amt_quote_term':'one-time', 'pay_freq_n_periods':1, 'term':1, 'term_unit':'prd', 'start_period':456, 'happiness_spending':False, 'annual_rate':0, 'rate_freq':1, 'rate_freq_unit':'yr'}
                                         # monthly maintenance
                                         , {'type':'expense', 'category':'house', 'title':'House 4 Monthly Expense', 'amt':740, 'amt_quote_term':'one-time', 'pay_freq_n_periods':1, 'term':51, 'term_unit':'yr', 'start_period':456, 'happiness_spending':True, 'annual_rate':0.02, 'rate_freq':1, 'rate_freq_unit':'yr'}
                                         # rent income
                                         , {'type':'salary', 'category':'house', 'title':'House 4 Rental Income', 'amt':2000, 'amt_quote_term':'one-time', 'pay_freq_n_periods':2, 'term':51, 'term_unit':'yr', 'start_period':456, 'happiness_spending':False}
                                     ]
                                )
                ]
                , tip='', backend=None
    )
    # stage 3 event - saving / investing
    , stctEvent(name='stg3_saving_program', title="How much do you want to invest monthly?", desc='You have $800 left every month. How do you want to spend?'
        , options=[
            # stctOption(name='stg3_saving_none', title='$0/month', image='res/dance_icon1.png'
            #     , desc='YOLO! I don\'t want to invest any amount of my income in an investment account.'
            #     , backend={'type':'expense', 'category':'consumption', 'title':'spend $800 for fun', 'amt':800, 'amt_quote_term':'one-time', 'pay_freq_n_periods':2, 'term':10, 'term_unit':'yr', 'start_period':936, 'happiness_spending':True, 'annual_rate':0, 'rate_freq':1, 'rate_freq_unit':'yr'}
            # )
            stctOption(name='stg3_saving_opt1', title='$150/month', image='res/chart_icon1.png'
                , desc='Invest $150/month; spend $650/month. \n\nAnnual return is 6% compounding rate.'
                , backend=[
                    {'type':'expense', 'category':'transfer', 'title':'invest transfer $150/month', 'amt':150, 'amt_quote_term':'one-time', 'pay_freq_n_periods':2, 'term':10, 'term_unit':'yr', 'start_period':936, 'happiness_spending':False, 'annual_rate':0, 'rate_freq':1, 'rate_freq_unit':'yr'}
                    , {'type':'asset', 'category':'investment', 'title':'invest $150/month', 'amt':150, 'annual_rate':0.06, 'pay_freq_n_periods':1, 'start_period':936, 'term':21, 'term_unit':'yr', 'happiness_spending':False, 'recurring_n_periods':2, 'recurring_end_period':1175}
                    , {'type':'expense', 'category':'consumption', 'title':'spend $650 for fun', 'amt':650, 'amt_quote_term':'one-time', 'pay_freq_n_periods':2, 'term':10, 'term_unit':'yr', 'start_period':936, 'happiness_spending':True, 'annual_rate':0, 'rate_freq':1, 'rate_freq_unit':'yr'}
                ]
            )
            , stctOption(name='stg3_saving_opt2', title='$250/month', image='res/chart_icon1.png'
                , desc='Invest $250/month; spend $550/month. \n\nAnnual return is 6% compounding rate.'
                , backend=[
                    {'type':'expense', 'category':'transfer', 'title':'invest transfer $250/month', 'amt':250, 'amt_quote_term':'one-time', 'pay_freq_n_periods':2, 'term':10, 'term_unit':'yr', 'start_period':936, 'happiness_spending':False, 'annual_rate':0, 'rate_freq':1, 'rate_freq_unit':'yr'}
                    , {'type':'asset', 'category':'investment', 'title':'invest $250/month', 'amt':250, 'annual_rate':0.06, 'pay_freq_n_periods':1, 'start_period':936, 'term':21, 'term_unit':'yr', 'happiness_spending':False, 'recurring_n_periods':2, 'recurring_end_period':1175}
                    , {'type':'expense', 'category':'consumption', 'title':'spend $550 for fun', 'amt':550, 'amt_quote_term':'one-time', 'pay_freq_n_periods':2, 'term':10, 'term_unit':'yr', 'start_period':936, 'happiness_spending':True, 'annual_rate':0, 'rate_freq':1, 'rate_freq_unit':'yr'}
                ]
            )
            , stctOption(name='stg3_saving_opt3', title='$400/month', image='res/chart_icon1.png'
                , desc='Invest $400/month; spend $400/month. \n\nAnnual return is 6% compounding rate.'
                , backend=[
                    {'type':'expense', 'category':'transfer', 'title':'invest transfer $400/month', 'amt':400, 'amt_quote_term':'one-time', 'pay_freq_n_periods':2, 'term':10, 'term_unit':'yr', 'start_period':936, 'happiness_spending':False, 'annual_rate':0, 'rate_freq':1, 'rate_freq_unit':'yr'}
                    , {'type':'asset', 'category':'investment', 'title':'invest $400/month', 'amt':400, 'annual_rate':0.06, 'pay_freq_n_periods':1, 'start_period':936, 'term':21, 'term_unit':'yr', 'happiness_spending':False, 'recurring_n_periods':2, 'recurring_end_period':1175}
                    , {'type':'expense', 'category':'consumption', 'title':'spend $400 for fun', 'amt':400, 'amt_quote_term':'one-time', 'pay_freq_n_periods':2, 'term':10, 'term_unit':'yr', 'start_period':936, 'happiness_spending':True, 'annual_rate':0, 'rate_freq':1, 'rate_freq_unit':'yr'}
                ]
            )
            , stctOption(name='stg3_saving_opt4', title='$550/month', image='res/chart_icon1.png'
                , desc='Invest $550/month; spend $250. \n\nAnnual return is 6% compounding rate.'
                , backend=[
                    {'type':'expense', 'category':'transfer', 'title':'invest transfer $550/month', 'amt':550, 'amt_quote_term':'one-time', 'pay_freq_n_periods':2, 'term':10, 'term_unit':'yr', 'start_period':936, 'happiness_spending':False, 'annual_rate':0, 'rate_freq':1, 'rate_freq_unit':'yr'}
                    , {'type':'asset', 'category':'investment', 'title':'invest $550/month', 'amt':550, 'annual_rate':0.06, 'pay_freq_n_periods':1, 'start_period':936, 'term':21, 'term_unit':'yr', 'happiness_spending':False, 'recurring_n_periods':2, 'recurring_end_period':1175}
                    , {'type':'expense', 'category':'consumption', 'title':'spend $250 for fun', 'amt':250, 'amt_quote_term':'one-time', 'pay_freq_n_periods':2, 'term':10, 'term_unit':'yr', 'start_period':936, 'happiness_spending':True, 'annual_rate':0, 'rate_freq':1, 'rate_freq_unit':'yr'}
                ]
            )
            , stctOption(name='stg3_saving_opt5', title='$800/month', image='res/chart_icon1.png'
                , desc='Invest all $800/month. \n\nAnnual return is 6% compounding rate.'
                , backend=[
                    {'type':'expense', 'category':'transfer', 'title':'invest transfer $800/month', 'amt':800, 'amt_quote_term':'one-time', 'pay_freq_n_periods':2, 'term':10, 'term_unit':'yr', 'start_period':936, 'happiness_spending':False, 'annual_rate':0, 'rate_freq':1, 'rate_freq_unit':'yr'}
                    , {'type':'asset', 'category':'investment', 'title':'invest $800/month', 'amt':800, 'annual_rate':0.06, 'pay_freq_n_periods':1, 'start_period':936, 'term':21, 'term_unit':'yr', 'happiness_spending':False, 'recurring_n_periods':2, 'recurring_end_period':1175}
                ]
            )
        ]
        , tip='', backend=None
    )
    # car purchase
    , stctEvent(name='stg3_car', title='Car purchase', desc='Your previous car needs to be replaced. Choose an option below.'
                , options=[
                    stctOption(name='stg3_car_2nd_hand', title='Second Hand Car', image='res/car_icon1.png'
                                , desc='This second hand car costs $10,000, depreciates by 20% annually. The value immeidately drops to $5,000 once you bought it. \n\nTo finance the purchase, you will need to take out a 5-year fixed-rate loan at 6.5% annual interest rate.\n\nThe required monthly loan payment is $195.67.\nTotal interest you will pay over the life of the loan is $1,739.63.'
                                , backend=[
                                    # car loan
                                    {'type':'loan', 'category':'car', 'title':'car loan', 'amt':10000, 'amt_quote_term':'one-time', 'term':5, 'term_unit':'yr', 'annual_rate':0.065, 'pay_freq_n_periods':2, 'start_period':456, 'happiness_spending':True}
                                    # depreciating car value
                                    , {'type':'asset', 'category':'car', 'title':'second hand car', 'amt':5000, 'annual_rate':-0.20, 'pay_freq_n_periods':1, 'start_period':456, 'term':20, 'term_unit':'yr', 'happiness_spending':False}
                                ]
                        )
                    , stctOption(name='stg3_car_mid', title='New Sedan (Mid-tier)', image='res/car_icon1.png'
                                , desc='This car costs $20,000, depreciates by 15% annually. The value immeidately drops to $16,000 once you bought it. \n\nTo finance the purchase, you will need to take out a 5-year fixed-rate loan at 6.5% annual interest rate.\n\nThe required monthly loan payment is $331.46.\nTotal interest you will pay over the life of the loan is $3,864.96.'
                                , backend=[
                                    {'type':'loan', 'category':'car', 'title':'car loan', 'amt':20000, 'amt_quote_term':'one-time', 'term':5, 'term_unit':'yr', 'annual_rate':0.065, 'pay_freq_n_periods':2, 'start_period':456, 'happiness_spending':True}
                                    , {'type':'asset', 'category':'car', 'title':'second hand car', 'amt':16000, 'annual_rate':-0.15, 'pay_freq_n_periods':1, 'start_period':456, 'term':20, 'term_unit':'yr', 'happiness_spending':False}
                                ]
                        )
                    , stctOption(name='stg3_car_exp', title='New SUV', image='res/car_icon1.png'
                                , desc='This car costs $40,000., depreciates by 15% annually. The value immeidately drops to $32,000 once you bought it. \n\nTo finance the purchase, you will need to take out a 5-year fixed-rate loan at 6.5% annual interest rate.\n\nThe required monthly loan payment is $662.92.\nTotal interest you will pay over the life of the loan is $7,729.92.'
                                , backend=[
                                    {'type':'loan', 'category':'car', 'title':'car loan', 'amt':40000, 'amt_quote_term':'one-time', 'term':5, 'term_unit':'yr', 'annual_rate':0.065, 'pay_freq_n_periods':2, 'start_period':456, 'happiness_spending':True}
                                    , {'type':'asset', 'category':'car', 'title':'second hand car', 'amt':32000, 'annual_rate':-0.15, 'pay_freq_n_periods':1, 'start_period':456, 'term':20, 'term_unit':'yr', 'happiness_spending':False}
                                ]
                        )
                    , stctOption(name='stg3_car_lux', title='New Luxury Car', image='res/car_icon1.png'
                                , desc='This car costs $100,000, depreciates by 15% annually. The value immeidately drops to $70,000 once you bought it. \n\nTo finance the purchase, you will need to take out a 5-year fixed-rate loan at 6.5% annual interest rate.\n\nThe required monthly loan payment is $1,956.62.\nTotal interest you will pay over the life of the loan is $17,396.88.'
                                , backend=[
                                    {'type':'loan', 'category':'car', 'title':'car loan', 'amt':100000, 'amt_quote_term':'one-time', 'term':5, 'term_unit':'yr', 'annual_rate':0.065, 'pay_freq_n_periods':2, 'start_period':456, 'happiness_spending':True}
                                    , {'type':'asset', 'category':'car', 'title':'second hand car', 'amt':70000, 'annual_rate':-0.15, 'pay_freq_n_periods':1, 'start_period':456, 'term':20, 'term_unit':'yr', 'happiness_spending':False}
                                ]
                        )
                ]
                , tip='', backend=None
    )


    # stage 4 ==================================================
    # stage 4 event -- job offer
    , stctEvent(name='stg4_job_offers', title='Which job do you want to take?', desc=''
                , options=[
                    stctOption(name='stg4_job_offers_early_retirement', title='Early Retirement', image='res/money_icon1.png'
                                     , desc='No income. \n\n10% increase in raw happiness score until the end of the life stage.'
                                     , backend=[
                                        {'type':'har', 'category':'happiness', 'title':'happiness increase', 'amt':1.1, 'amt_quote_term':'one-time', 'pay_freq_n_periods':1, 'term':10, 'term_unit':'yr', 'start_period':936}
                                        # mandatory stage wide spending
                                        , {'type':'expense', 'category':'spending', 'title':'Stage 4 Mandatory Spending', 'amt':700, 'amt_quote_term':'one-time', 'pay_freq_n_periods':1, 'term':10, 'term_unit':'yr', 'start_period':936, 'happiness_spending':False, 'annual_rate':0.0, 'rate_freq':1, 'rate_freq_unit':'yr'}
                                     ]
                              )
                    , stctOption(name='stg4_job_offers_opt1', title='Job offer 4.1: Low Stress', image='res/money_icon1.png'
                                     , desc='Annual income is $65,000. Monthly income is $5,417 paid biweekly. \n\n3% increase in raw happiness score until the end of the life stage.'
                                     , backend=[
                                        {'type':'salary', 'category':'income', 'title':'salary', 'amt':65000, 'amt_quote_term':'annual', 'pay_freq_n_periods':1, 'term':10, 'term_unit':'yr', 'start_period':936}
                                        , {'type':'har', 'category':'happiness', 'title':'happiness increase', 'amt':1.03, 'amt_quote_term':'one-time', 'pay_freq_n_periods':1, 'term':10, 'term_unit':'yr', 'start_period':936}
                                        # mandatory stage wide spending
                                        , {'type':'expense', 'category':'spending', 'title':'Stage 4 Mandatory Spending', 'amt':700, 'amt_quote_term':'one-time', 'pay_freq_n_periods':1, 'term':10, 'term_unit':'yr', 'start_period':936, 'happiness_spending':False, 'annual_rate':0.0, 'rate_freq':1, 'rate_freq_unit':'yr'}
                                     ]
                              )
                    , stctOption(name='stg4_job_offers_opt2', title='Job offer 4.2: Average Pay', image='res/money_icon1.png'
                                     , desc='Annual income is $80,000. Monthly income is $6,667 paid biweekly.'
                                     , backend=[
                                        {'type':'salary', 'category':'income', 'title':'salary', 'amt':80000, 'amt_quote_term':'annual', 'pay_freq_n_periods':1, 'term':10, 'term_unit':'yr', 'start_period':936}
                                        # mandatory stage wide spending
                                        , {'type':'expense', 'category':'spending', 'title':'Stage 4 Mandatory Spending', 'amt':700, 'amt_quote_term':'one-time', 'pay_freq_n_periods':1, 'term':10, 'term_unit':'yr', 'start_period':936, 'happiness_spending':False, 'annual_rate':0.0, 'rate_freq':1, 'rate_freq_unit':'yr'}
                                     ]
                                )
                    , stctOption(name='stg4_job_offers_opt3', title='Job offer 4.3: High Stress', image='res/money_icon1.png'
                                     , desc='Annual income is $120,000. Monthly income is $10,000 paid biweekly.  \n\n4% reduction of the raw happiness score until the end of the life stage.'
                                     , backend=[
                                        {'type':'salary', 'category':'income', 'title':'salary', 'amt':120000, 'amt_quote_term':'annual', 'pay_freq_n_periods':1, 'term':10, 'term_unit':'yr', 'start_period':936}
                                        , {'type':'har', 'category':'happiness', 'title':'happiness increase', 'amt':0.96, 'amt_quote_term':'one-time', 'pay_freq_n_periods':1, 'term':10, 'term_unit':'yr', 'start_period':936}
                                        # mandatory stage wide spending
                                        , {'type':'expense', 'category':'spending', 'title':'Stage 4 Mandatory Spending', 'amt':700, 'amt_quote_term':'one-time', 'pay_freq_n_periods':1, 'term':10, 'term_unit':'yr', 'start_period':936, 'happiness_spending':False, 'annual_rate':0.0, 'rate_freq':1, 'rate_freq_unit':'yr'}
                                     ]
                                )
                ]
                , tip='', backend=None
    )
    # stage 4 event - saving / investing
    , stctEvent(name='stg4_saving_program', title="How much do you want to invest monthly?", desc='You have extra $500 per month left. How do you want to spend?'
        , options=[
            stctOption(name='stg4_saving_none', title='$0/month', image='res/dance_icon1.png'
                , desc='YOLO! I don\'t want to invest any amount of my income in an investment account.'
                , backend={'type':'expense', 'category':'consumption', 'title':'monthly spending $500', 'amt':500, 'amt_quote_term':'one-time', 'pay_freq_n_periods':2, 'term':20, 'term_unit':'yr', 'start_period':456, 'happiness_spending':True, 'annual_rate':0, 'rate_freq':1, 'rate_freq_unit':'yr'}
            )
            , stctOption(name='stg4_saving_opt1', title='$100/month', image='res/chart_icon1.png'
                , desc='Invest $100/month; spend $400/month. \n\nAnnual return is 6% compounding rate.'
                , backend=[
                    {'type':'expense', 'category':'transfer', 'title':'invest transfer $100/month', 'amt':100, 'amt_quote_term':'one-time', 'pay_freq_n_periods':2, 'term':20, 'term_unit':'yr', 'start_period':456, 'happiness_spending':False, 'annual_rate':0, 'rate_freq':1, 'rate_freq_unit':'yr'}
                    , {'type':'asset', 'category':'investment', 'title':'invest $100/month', 'amt':100, 'annual_rate':0.06, 'pay_freq_n_periods':1, 'start_period':456, 'term':51, 'term_unit':'yr', 'happiness_spending':False, 'recurring_n_periods':2, 'recurring_end_period':614}
                    , {'type':'expense', 'category':'consumption', 'title':'monthly spending $400', 'amt':400, 'amt_quote_term':'one-time', 'pay_freq_n_periods':2, 'term':20, 'term_unit':'yr', 'start_period':456, 'happiness_spending':True, 'annual_rate':0, 'rate_freq':1, 'rate_freq_unit':'yr'}
                ]
            )
            , stctOption(name='stg4_saving_opt2', title='$200/month', image='res/chart_icon1.png'
                , desc='Invest $200/month; spend $300/month. \n\nAnnual return is 6% compounding rate.'
                , backend=[
                    {'type':'expense', 'category':'transfer', 'title':'invest transfer $200/month', 'amt':200, 'amt_quote_term':'one-time', 'pay_freq_n_periods':2, 'term':20, 'term_unit':'yr', 'start_period':456, 'happiness_spending':False, 'annual_rate':0, 'rate_freq':1, 'rate_freq_unit':'yr'}
                    , {'type':'asset', 'category':'investment', 'title':'invest $200/month', 'amt':200, 'annual_rate':0.06, 'pay_freq_n_periods':1, 'start_period':456, 'term':51, 'term_unit':'yr', 'happiness_spending':False, 'recurring_n_periods':2, 'recurring_end_period':614}
                    , {'type':'expense', 'category':'consumption', 'title':'monthly spending $300', 'amt':300, 'amt_quote_term':'one-time', 'pay_freq_n_periods':2, 'term':20, 'term_unit':'yr', 'start_period':456, 'happiness_spending':True, 'annual_rate':0, 'rate_freq':1, 'rate_freq_unit':'yr'}
                ]
            )
            , stctOption(name='stg4_saving_opt3', title='$500/month', image='res/chart_icon1.png'
                , desc='Invest $500/month. \n\nAnnual return is 6% compounding rate.'
                , backend=[
                    {'type':'expense', 'category':'transfer', 'title':'invest transfer $500/month', 'amt':500, 'amt_quote_term':'one-time', 'pay_freq_n_periods':2, 'term':20, 'term_unit':'yr', 'start_period':456, 'happiness_spending':False, 'annual_rate':0, 'rate_freq':1, 'rate_freq_unit':'yr'}
                    , {'type':'asset', 'category':'investment', 'title':'invest $500/month', 'amt':500, 'annual_rate':0.06, 'pay_freq_n_periods':1, 'start_period':456, 'term':51, 'term_unit':'yr', 'happiness_spending':False, 'recurring_n_periods':2, 'recurring_end_period':614}
                ]
            )
        ]
        , tip='', backend=None
    )
    # stage 4 - car purchase
    , stctEvent(name='stg4_car', title='Car purchase', desc='Your previous car needs to be replaced. Choose an option below.'
                , options=[
                    stctOption(name='stg4_car_2nd_hand', title='Second Hand Car', image='res/car_icon1.png'
                                , desc='This second hand car costs $10,000, depreciates by 20% annually. The value immeidately drops to $5,000 once you bought it. \n\nTo finance the purchase, you will need to take out a 5-year fixed-rate loan at 6.5% annual interest rate.\n\nThe required monthly loan payment is $195.67.\nTotal interest you will pay over the life of the loan is $1,739.63.'
                                , backend=[
                                    # car loan
                                    {'type':'loan', 'category':'car', 'title':'car loan', 'amt':10000, 'amt_quote_term':'one-time', 'term':5, 'term_unit':'yr', 'annual_rate':0.065, 'pay_freq_n_periods':2, 'start_period':936, 'happiness_spending':True}
                                    # depreciating car value
                                    , {'type':'asset', 'category':'car', 'title':'second hand car', 'amt':5000, 'annual_rate':-0.20, 'pay_freq_n_periods':1, 'start_period':936, 'term':31, 'term_unit':'yr', 'happiness_spending':False}
                                ]
                        )
                    , stctOption(name='stg4_car_mid', title='New Sedan (Mid-tier)', image='res/car_icon1.png'
                                , desc='This car costs $20,000, depreciates by 15% annually. The value immeidately drops to $16,000 once you bought it. \n\nTo finance the purchase, you will need to take out a 5-year fixed-rate loan at 6.5% annual interest rate.\n\nThe required monthly loan payment is $331.46.\nTotal interest you will pay over the life of the loan is $3,864.96.'
                                , backend=[
                                    {'type':'loan', 'category':'car', 'title':'car loan', 'amt':20000, 'amt_quote_term':'one-time', 'term':5, 'term_unit':'yr', 'annual_rate':0.065, 'pay_freq_n_periods':2, 'start_period':936, 'happiness_spending':True}
                                    , {'type':'asset', 'category':'car', 'title':'second hand car', 'amt':16000, 'annual_rate':-0.15, 'pay_freq_n_periods':1, 'start_period':936, 'term':31, 'term_unit':'yr', 'happiness_spending':False}
                                ]
                        )
                    , stctOption(name='stg4_car_exp', title='New SUV', image='res/car_icon1.png'
                                , desc='This car costs $40,000., depreciates by 15% annually. The value immeidately drops to $32,000 once you bought it. \n\nTo finance the purchase, you will need to take out a 5-year fixed-rate loan at 6.5% annual interest rate.\n\nThe required monthly loan payment is $662.92.\nTotal interest you will pay over the life of the loan is $7,729.92.'
                                , backend=[
                                    {'type':'loan', 'category':'car', 'title':'car loan', 'amt':40000, 'amt_quote_term':'one-time', 'term':5, 'term_unit':'yr', 'annual_rate':0.065, 'pay_freq_n_periods':2, 'start_period':936, 'happiness_spending':True}
                                    , {'type':'asset', 'category':'car', 'title':'second hand car', 'amt':32000, 'annual_rate':-0.15, 'pay_freq_n_periods':1, 'start_period':936, 'term':31, 'term_unit':'yr', 'happiness_spending':False}
                                ]
                        )
                    , stctOption(name='stg4_car_lux', title='New Luxury Car', image='res/car_icon1.png'
                                , desc='This car costs $100,000, depreciates by 20% annually. The value immeidately drops to $70,000 once you bought it. \n\nTo finance the purchase, you will need to take out a 5-year fixed-rate loan at 6.5% annual interest rate.\n\nThe required monthly loan payment is $1,956.62.\nTotal interest you will pay over the life of the loan is $17,396.88.'
                                , backend=[
                                    {'type':'loan', 'category':'car', 'title':'car loan', 'amt':100000, 'amt_quote_term':'one-time', 'term':5, 'term_unit':'yr', 'annual_rate':0.065, 'pay_freq_n_periods':2, 'start_period':936, 'happiness_spending':True}
                                    , {'type':'asset', 'category':'car', 'title':'second hand car', 'amt':70000, 'annual_rate':-0.2, 'pay_freq_n_periods':1, 'start_period':936, 'term':31, 'term_unit':'yr', 'happiness_spending':False}
                                ]
                        )
                ]
                , tip='', backend=None
    )


    # random events ============================
    # random event - lottery
    , stctEvent(name='rnd_lotto', title='Congratulations! Yon won the lottery!!!', options=None
                , desc='Congratulations! You won $5,000, paid immediately to you!'
                , tip=''
                , backend={'type':'salary', 'category':'lottery', 'title':'lottery', 'amt':50000, 'amt_quote_term':'one-time', 'pay_freq_n_periods':1, 'term':1, 'term_unit':'prd', 'start_period':-1}
               )
    # random event - small car accident
    , stctEvent(name='rnd_car_accident_partial', title='You had a car accident :(', options=None
                , desc='After deductibles, the out of pocket cost is $700.'
                , tip=''
                , backend={'type':'expense', 'category':'car', 'title':'small car accident', 'amt':700, 'amt_quote_term':'one-time', 'pay_freq_n_periods':1, 'term':1, 'term_unit':'prd', 'start_period':-1, 'happiness_spending':False, 'annual_rate':0, 'rate_freq':1, 'rate_freq_unit':'yr'}
               )
    # random event - road trip to Cancun
    , stctEvent(name='rnd_road_trip_cancun', title='Road trip to Cancun', options=None
                , desc='You had a blast with a high school friend who came visit. Your friend wants you to join them for a road trip to Cancun. \n\nThe trip would cost $1,500.'
                , tip=''
                , backend={'type':'expense', 'category':'travel', 'title':'road trip to cancun', 'amt':1500, 'amt_quote_term':'one-time', 'pay_freq_n_periods':1, 'term':1, 'term_unit':'prd', 'start_period':-1, 'happiness_spending':True, 'annual_rate':0, 'rate_freq':1, 'rate_freq_unit':'yr'}
               )
    # random event - road trip to a national park
    , stctEvent(name='rnd_road_trip_natl_park', title='Road trip to a nearby national park?', options=None
                , desc='Spring break rolls around. Bunch of friends are planning to go to a nearby national park for a week.  \n\nThe trip would cost $200.'
                , tip=''
                , backend={'type':'expense', 'category':'travel', 'title':'road trip to nearby national park', 'amt':1500, 'amt_quote_term':'one-time', 'pay_freq_n_periods':1, 'term':1, 'term_unit':'prd', 'start_period':-1, 'happiness_spending':True, 'annual_rate':0, 'rate_freq':1, 'rate_freq_unit':'yr'}
               )
    # random event - grandma $500 check
    , stctEvent(name='rnd_grandma_visit', title='Grandma\'s Visit', options=None
                , desc='Grandma came visit recently and gave you a $500 check.'
                , tip=''
                , backend={'type':'salary', 'category':'income', 'title':'gradma\'s visit', 'amt':500, 'amt_quote_term':'one-time', 'pay_freq_n_periods':1, 'term':1, 'term_unit':'prd', 'start_period':-1}
               )
    # random event - replace laptop
    , stctEvent(name='rnd_broken_laptop', title='Broken Laptop', options=None
                , desc='Partied too hard last night and accidentally threw your laptop into the pool. The replacement of the laptop costs $900.'
                , tip=''
                , backend={'type':'expense', 'category':'tech', 'title':'broken laptop', 'amt':900, 'amt_quote_term':'one-time', 'pay_freq_n_periods':1, 'term':1, 'term_unit':'prd', 'start_period':-1, 'happiness_spending':False, 'annual_rate':0, 'rate_freq':1, 'rate_freq_unit':'yr'}
               )
    # random event - raise
    , stctEvent(name='rnd_salary_increase', title='You got a promotion!', options=None
                , desc='Due to your hard work, your annual salary is increased by $20,000.'
                , tip=''
                , backend={'type':'salary', 'category':'income', 'title':'job raise', 'amt':20000, 'amt_quote_term':'annual', 'pay_freq_n_periods':2, 'term':70, 'term_unit':'yr', 'start_period':-1}
               )
    # random event - domestic trip
    , stctEvent(name='rnd_extended_fam_trip', title='Extended Family Trip', options=None
                , desc='The extended family decided to take a trip at the beach. The trip costs $2,500.'
                , tip=''
                , backend={'type':'expense', 'category':'travel', 'title':'Extended Family Trip', 'amt':2500, 'amt_quote_term':'one-time', 'pay_freq_n_periods':1, 'term':1, 'term_unit':'prd', 'start_period':-1, 'happiness_spending':True, 'annual_rate':0, 'rate_freq':1, 'rate_freq_unit':'yr'}
               )
    # random event - destination wedding
    , stctEvent(name='rnd_destination_wedding', title='Destination Wedding', options=None
                , desc='Your cousin invited you to a wedding in France. You decided to go and check out the country. The trip costs $5000.'
                , tip=''
                , backend={'type':'expense', 'category':'travel', 'title':'Extended Family Trip', 'amt':5000, 'amt_quote_term':'one-time', 'pay_freq_n_periods':1, 'term':1, 'term_unit':'prd', 'start_period':-1, 'happiness_spending':True, 'annual_rate':0, 'rate_freq':1, 'rate_freq_unit':'yr'}
               )
    , stctEvent(name='rnd_illness_major', title='Major Illness', options=None
                , desc='Your fell after a day fun at a ski resort. The medical expense is $5,000. You feel terrible and take a 40% reduction of happiness for 6 months.'
                , tip=''
                , backend=[
                    {'type':'expense', 'category':'medical', 'title':'Medical bill', 'amt':5000, 'amt_quote_term':'one-time', 'pay_freq_n_periods':1, 'term':1, 'term_unit':'prd', 'start_period':-1, 'happiness_spending':False, 'annual_rate':0, 'rate_freq':1, 'rate_freq_unit':'yr'}
                    , {'type':'har', 'category':'illness', 'title':'Major Illness', 'amt':0.60, 'amt_quote_term':'one-time', 'pay_freq_n_periods':1, 'term':6, 'term_unit':'mth', 'start_period':-1}
                ]
               )
    
]

