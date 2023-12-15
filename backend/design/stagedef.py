# Copyright (C) 2023, Bank of America.  The file below is licensed to LSC for use with HSoF.  All other rights are reserved.
 Copyright (C) 2023, Bank of America.  The file below is licensed to LSC for use with HSoF.  All other rights are reserved.
""This file defines the stages of the game. See code documentation for more details."""

from collections import namedtuple

# define a structure that can describe a life stage
stctStage = namedtuple('stctStage', 'name title desc n_random_event_turn init_age end_age life_event_seq random_event rand_event_weight backend')

# a list of all life stages. Order matters. First stage should appear first.
pvStages = [
    stctStage(name='post_hi_schl'
                , title='Post High School'
                , init_age=18, end_age=21 # 4 years
                , desc='This is the first stage of the game. This stage goes from age 18 to 21.'
                , life_event_seq=['stg1_college','stg1_car','stg1_lodging','stg1_part_time_job']
                , n_random_event_turn=1
                , random_event=['rnd_lotto','rnd_car_accident_partial','rnd_road_trip_cancun','rnd_road_trip_natl_park','rnd_grandma_visit','rnd_broken_laptop']
                , rand_event_weight=[0.01,0.05,0.1,0.25,0.25,0.05]
                , backend = dict()
             )
    , stctStage(name='young_adlt'
                , title='Young Adult'
                , init_age=22, end_age=36 #15 years
                , desc='This is the second stage of the game. This stage lasts from age 22 to 36. Your monthly spending for basic living is $700.'
                , life_event_seq=['stg2_firstjob', 'stg2_firsthouse', 'stg2_car', 'stg2_saving_program']
                , n_random_event_turn=1
                , random_event=['rnd_lotto','rnd_car_accident_partial','rnd_salary_increase','rnd_extended_fam_trip','rnd_destination_wedding','rnd_illness_major']
                , rand_event_weight=[0.01,10,50,70,20,5]
                , backend = dict()
               )
    , stctStage(name='peak_career'
                , title='Peak Career'
                , init_age=37, end_age=56 #20 years
                , desc='This is the third stage of the game. This stage lasts from age 37 to 56. Your monthly spending for basic living is $1,400.\n\nPeople in this stage typically reach their peak earning potential.'
                , life_event_seq=['stg3_job_offers','stg3_car','stg3_saving_program'] #,'stg3_house'
                , n_random_event_turn=2
                , random_event=['rnd_lotto','rnd_car_accident_partial','rnd_salary_increase','rnd_extended_fam_trip','rnd_destination_wedding','rnd_illness_major']
                , rand_event_weight=[1,5,20,50,10,10]
                , backend = dict()
               )
    , stctStage(name='near_retirement'
                , title='Near Retirement'
                , init_age=57, end_age=66 #10 years
                , desc='This is the 4th stage of the game. This stage lasts from age 57 to 66. Your monthly spending for basic living is $1,400.'
                , life_event_seq=['stg4_job_offers','stg4_car','stg4_saving_program']
                , n_random_event_turn=1
                , random_event=['rnd_lotto','rnd_car_accident_partial','rnd_salary_increase','rnd_extended_fam_trip','rnd_destination_wedding','rnd_illness_major']
                , rand_event_weight=[1,20,60,50,30,15]
                , backend = dict()
               )
    , stctStage(name='retired'
                , title='Retired'
                , init_age=67, end_age=87 # 21 years
                , desc='This is the last stage of the game. This stage lasts from age 67 to 87.\n\nThere is no playable turn in this stage. Please click Next to see the winner.'
                , life_event_seq=[]
                , n_random_event_turn=0
                , random_event=None, rand_event_weight=None
                , backend = dict()
               )
]

