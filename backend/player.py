# Copyright (C) 2023, Bank of America.  The file below is licensed to LSC for use with HSoF.  All other rights are reserved.
 Copyright (C) 2023, Bank of America.  The file below is licensed to LSC for use with HSoF.  All other rights are reserved.
""This file defines the Player class. Player represents a player (human or AI), 
stores player attributes and scores the player based on the attribute values."""

from backend.design import NPeriodsPerMonth
from collections import defaultdict
from backend.prosperville import Prosperville
from typing import Optional, Callable

class Player:
    """Represents a player in the game."""
    
    def __init__(self, name:str, game_instance:Prosperville, is_system=False, init_cash=0.0):
        """Represents a player in the game.
        
        Input Arguments
        ---------------
        name:           required str that represents the name of the player.
        game_instance:  required object of Prosperville class that represents the current running game.
        is_system:      optional boolean value that indiates if the player is an AI or a human player. 
        init_cash:      optional float value that presents the initial cash the player has upon creation. 
        """
        
        if not isinstance(game_instance, Prosperville):
            raise Exception('game_instance input argument must be an instance of Prosperville class.')

        if init_cash < 0:
            raise ValueError(f'init_cash should be non-negative. "{init_cash}" is given.')

        # save the input argument values
        self.name = name # name of the player
        self.crntGame = game_instance # this variable is used to access current game information such as step table, game progression, etc
        self.is_system=is_system
        self.init_cash = init_cash # this is used to generate the starting point of the score table

        # current value of player attributes
        self.score = 0
        self.happiness = 100
        self.equity = self.init_cash; self.debt = 0; self.asset=0

        self.net_income=0; self.income=0; self.spending=0
        self.debt_std=0; self.debt_mort=0; self.debt_car=0; self.debt_other=0
        
        # set the score adjustment ratio so that no matter the initial cash given to the player at the start of the game, 
        # all games start with 100 happiness for all players
        self.score_adj_ratio = 100/self.__calculate_happiness(self.init_cash,0)
        
        # bankruptcy related fields
        self.bankrupt = False # bankruptcy indicator
        self.bankrupt_period = -1 # simulation period when the player becomes insolvent. 
        self.bankrupt_step = -1 # game step at which the player becomes insolvent

        # A special access controlled dictionary that saves the player's choices. The index is an event name. 
        # The value is the option index under backend.design.eventdef.stctEvent.options. 
        # Player.__on_set_choice is called when elements in self.choices is added or modified
        self.choices = RestrictedDict(on_set=Player.__on_set_choice)
        # set the player instance to the choice so that the __on_set_choice method can access the parent player object from choices collection
        self.choices.player = self
        # this is an internal cache that saves the availability of options for events that the game has visited
        self._available_options = dict()

        # a list of backend objects that are affecting this player.
        # these objects are added by self.crntGame via ___add_bkedobj_2_player method in backend/prosperville.py
        self.selected_bked_objs = list()
        # this is the raw structure of the score table. it keeps track of items that are essential to the game. 
        # each row in this table represents a simulation period
        self._score_table = defaultdict(list)

        # these two are used to cache the choice table property. 
        # The property does not generate the whole table every time it is accessed. 
        # It simply adds new content to the previous cached table as the game progresses
        self._last_turn_cached = 0
        self._cache_choice_table = None

    # this class level method is called when elements in self.choices is added or modified
    def __on_set_choice(collection, eventName, newChoice):
        """adds special logic to option dependency"""
        
        # if new event or new value for the event
        if eventName not in collection or collection[eventName] != newChoice:
            
            # special logic to set available options for the 'stg1_lodging' event based on the choice made in 'stg1_college' event
            # the available options for 'stg1_lodging' event is set when a choice is made in the 'stg1_college' event
            if eventName == 'stg1_college':
                if collection.player.crntGame.event_by_name[eventName].options[newChoice].name == 'stg1_no_college':
                    collection.player._available_options['stg1_lodging'] = [False, True, True]
                else:
                    collection.player._available_options['stg1_lodging'] = [True, True, True]

        # if the new choice is not available to the player
        if collection.player.get_option_availability(eventName)[newChoice] == False:
            raise ValueError('Option "{0}" (index {1}) is not available to player {2}.'.format(collection.player.crntGame.event_by_name[eventName].options[newChoice].name, newChoice, collection.player.name))

        # return True to indicate the setting option should proceed. if return False, the setting operation is blocked. 
        return True

    @property
    def score_table(self):
        """gets the score table of the player up to the end of the game's current step"""
        import pandas as pd
        import numpy as np
        from backend.design import NPeriodsPerMonth # number of simulation periods per month
        
        # total number of periods in the internal score table (_score_table)
        end_period = len(self._score_table['score'])
        # the next two lines get the values for the month column
        # this first line sets a sequence from 1 to end_period to get the length of the values right.
        # Dividing by NPeriodsPerMonth sets the right number of months. 
        # Taking the remainder of 12 (%12) converts to actual month number so that Jan = 1, Feb = 2, etc
        mth_vals = np.arange(start=1,stop=end_period+1,step=1)/NPeriodsPerMonth%12
        # Due to the remainder operation, any multiple of 12 gets the value of 0. we need to set it to 12 to indicate December.
        mth_vals = np.where(mth_vals==0,12,mth_vals)
        
        # assemble the raw data in a dictionary with each key-value pair being a column. 
        # then convert the dictionary to pandas dataframe. 
        # finally, limit the rows to the end period of the current turn. 
        # Note that AI may simulate ahead within a stage even if it does not know the outcome of random event turns.
        return pd.DataFrame({
            'Stage': ""
            , 'Age':(np.floor(np.arange(start=0,stop=end_period,step=1)/12/NPeriodsPerMonth)
                    +self.crntGame.stage_by_name[self.crntGame.step_table['stage_name'][0]].init_age
                ).astype(int)
            , 'Month':mth_vals
            , 'Score':np.array(self._score_table['score'],int)
            , 'Happiness':np.array(self._score_table['happiness'],int)
            , 'Equity':np.array(self._score_table['wealth'],int)
            , 'Debt':np.array(self._score_table['debt'],int)
        }).loc[:(self.bankrupt_period if self.bankrupt else self.crntGame.step_table['period_sim_last'][self.crntGame.iStep])]

    @property
    def choice_table(self):
        """gets a table that shows the choices the player made"""
        import pandas as pd

        # if the cache has not been made yet, set up the table structure
        if self._cache_choice_table is None:
            from collections import defaultdict
            # we will create a dictionary of lists first. 
            # each list represents a column. The column name is the key in the dictionary for the list.
            tmp_tbl = defaultdict(list)
            
            # add stage index and turn index
            tmp_tbl['istage'] = self.crntGame.step_table['stage']
            tmp_tbl['iturn'] = self.crntGame.step_table['turn']
            
            # go through each turn and add stage and event name, and turn number
            # the content is already in crntGame.step_table. we are just repackaging it
            for istp in range(len(self.crntGame.step_table['stage'])):
                tmp_tbl['Stage'].append(self.crntGame.stage_by_name[self.crntGame.step_table['stage_name'][istp]].title)
                tmp_tbl['Turn'].append(self.crntGame.step_table['turn'][istp]+1)
                tmp_tbl['Random'].append('Yes' if self.crntGame.step_table['is_random_event_step'][istp] else 'No')
                if self.crntGame.step_table['event_name'][istp] != "":
                    tmp_tbl['Event'].append(self.crntGame.event_by_name[self.crntGame.step_table['event_name'][istp]].title)
                else:
                    tmp_tbl['Event'].append('')
            
            # leave all choices empty
            tmp_tbl['Choice'] = [''] * len(tmp_tbl['istage'])
            
            self._cache_choice_table = pd.DataFrame(tmp_tbl)
        
        rtn = self._cache_choice_table
        # we only refresh the table for the turns between the last cached turn and the current turn. 
        # choices in turns before the previous turn cannot change. so we don't need to update them
        for itrn in range(self._last_turn_cached, self.crntGame.iTurn+1,1):
            for istp in range(self.crntGame.first_step_of_turn[itrn],self.crntGame.last_step_of_turn[itrn]+1):
                # if random event has not been drawn, skip this step
                if self.crntGame.step_table['event_name'][istp] == '': 
                    rtn.loc[istp,'Choice'] = 'N/A'
                    continue 
                
                # get the current event object
                evtObj = self.crntGame.event_by_name[self.crntGame.step_table['event_name'][istp]]
                
                # if the event is a random event, add the event title to the return table
                if self.crntGame.step_table['is_random_event_step'][istp]:
                    rtn.loc[istp,'Event'] = evtObj.title

                # add choices
                if evtObj.options is None or len(evtObj.options) == 0:
                    # if the event does not have options, set choice to NA
                    rtn.loc[istp,'Choice'] = 'N/A'
                elif evtObj.name in self.choices:
                    # if the user has made a choice for the event
                    rtn.loc[istp, 'Choice'] = evtObj.options[self.choices[evtObj.name]].title

        # set the current turn as the cahced turn. choices made in the previous turn cannot be changed.    
        self._last_turn_cached = self.crntGame.iTurn
        self._cache_choice_table = rtn
        return rtn

    def get_option_availability(self, eventName):
        """returns a list of booleans that indicate the availability of options for a given event"""

        # this method is needed because certain options may not be available if another option is chosen
        
        # if the event is empty or has no options, return None
        if eventName not in self.crntGame.event_by_name or self.crntGame.event_by_name[eventName].options is None or len(self.crntGame.event_by_name[eventName].options) == 0:
            return None
        
        # if the event has no previously cached results, create it. 
        # Player.__on_set_choice method creates and updates the cache for the dependent event choices whenever the user makes changes to the contingent event choice
        # because of the above, when an event has no cache, it simply means it is not an event (dependent) that depends on another (contingent)
        # in that case, we just set all options of non-dependent event to be available.
        if eventName not in self._available_options:
            self._available_options[eventName] = [True] * len(self.crntGame.event_by_name[eventName].options)
        return self._available_options[eventName]

    def simulate(self, period_start, period_end):
        """Simulates for the player between two simulation periods
        
        Input Argument
        --------------
        period_start:   required int that indicates the starting period to simulate
        peirod_end:     required int that indicates the last period to simulate to. This period is included in the simulation.
        """

        # no the simulation if the player is already bankrupted
        if self.bankrupt:
            return
        
        # loop through the periods, and performs scoring. this is where the actual simulation results are combined
        for iPeriod in range(period_start, period_end+1):
            self.__update_score_table(iPeriod)

            # if after this period (=iPeriod), the player becomes bankrupt
            if self.bankrupt:
                # adjust the end period to when they bankrupt. 
                # Note self.bankrupt_period is set by self.__update_score_table 
                period_end = self.bankrupt_period
                break # simulate no more when bankrupt
        
        # calculate total number of periods that we just simulated. 
        sim_n_periods = period_end - period_start + 1
        
        self.happiness = self._score_table['happiness'][period_end]
        # calculate the average monthly net income over this simulation
        self.net_income = sum(self._score_table['net_income'][period_start:(period_end+1)]) * NPeriodsPerMonth / sim_n_periods
        # calculate the average monthly spending over this simulation
        self.spending = sum(self._score_table['spending'][period_start:(period_end+1)]) * NPeriodsPerMonth / sim_n_periods
        # calculate the average monthly income over this simulation
        self.income = sum(self._score_table['income'][period_start:(period_end+1)]) * NPeriodsPerMonth / sim_n_periods

        # gather the other attribute values at the end of the simulation
        self.debt_std = self._score_table['debt_std'][period_end]
        self.debt_mort = self._score_table['debt_mort'][period_end]
        self.debt_car = self._score_table['debt_car'][period_end]
        self.debt_other = self._score_table['debt_other'][period_end]
        
        self.score = self._score_table['score'][period_end]
        self.debt = self._score_table['debt'][period_end]
        self.equity = self._score_table['wealth'][period_end]
        self.asset = self._score_table['asset'][period_end]
        
    
    def __update_score_table(self, iprd):
        """Calculates effects of all backend objects attached to this player
        
        Input Argument
        --------------
        iprd:       required int that represents the period this method works on. This is a 0-based index.
        """

        if self.bankrupt:
            return
        
        # set the happiness adjustment ratio to the initial value that all players should have when the game initially started
        # this is the value that makes all players to have 100 happiness score at the beginning of the game irregardless of the initial cash value.
        hAdjRate = self.score_adj_ratio
        # has the current period been simulated for this player already. this happens for AI when it simulates ahead of turn to the end of a stage (ignoring undrawn random events).
        does_period_exists = iprd < len(self._score_table['income'])
        
        # the following for loop gathers variable values / attributes for this player 
        # by looping through all backend objects this player has, 
        # and adding their effects to the correct variables.
        income, spending, debt, hpness_spding, asset, annual_salary = 0,0,0,0,0,0
        debt_std, debt_mort, debt_car, debt_other = 0,0,0,0
        # loop through each backend object that this player has
        for crntObj in self.selected_bked_objs:
            # this is the index used in the backend object's schedule table. Because not all events start at period 0, 
            # crntObj.start_period to adjust the schedule table to always start at 0. To reverse that effect, 
            # we simply subtract crntObj.start_period from the global simulation period value. 
            obj_iprd = iprd-crntObj.start_period
            # if the current simulation period is before the backend object's first period when it should have an effect on the player, 
            # or the current simulation period is past the last period the backend object should have an effect on the player
            # move to the next backend object
            if obj_iprd < 0 or obj_iprd >= crntObj.n_periods:
                continue
            
            # check the backend object type so that we can put the right amount to the right variable. 
            if crntObj.type != 'har':
                # if the backend object is not Happiness adjustment ratio: HappinessAdjustmentRatio class from backend/othrbkendobj.py
                # get the pay value for the current period
                # the pay value could be a payment to loan or a pay check from a salaried job
                crntPay = crntObj.schedule['pay'][obj_iprd]
            if crntObj.type == 'salary':
                # if salary, add to income, tally annual salary. annual salary is used in bankruptcy logic
                income += crntPay
                annual_salary += crntObj.amount 
            elif crntObj.type == 'loan':
                # add loan payment to spending variable
                spending += crntPay
                # find the principal amount still owe for this period
                crnt_obj_debt = crntObj.schedule['bal_end'][obj_iprd]
                # add the debt principal to the debt variable
                debt += crnt_obj_debt
                # if this payment is counted as part of spending value for the happiness calculation. 
                # note some payment such as student debt is not considered leisure spending. 
                # so it does not make sense to use it to boost happiness. 
                # However, a mortgage payment is considered a leisure spending in this game to approximate the enjoyment of a house. 
                # bigger house -> bigger mortgage payment -> happier
                if crntObj.is_happiness_spending:
                    hpness_spding += crntPay
                # categorize the debt
                if crntObj.category == 'student':
                    debt_std += crnt_obj_debt
                elif crntObj.category == 'mortgage':
                    debt_mort += crnt_obj_debt
                elif crntObj.category == 'car':
                    debt_car += crnt_obj_debt
                else:
                    debt_other += crnt_obj_debt
            elif crntObj.type == 'expense':
                # if spending, add to spending variable, tally if it should be counted for happiness
                spending += crntPay
                if crntObj.is_happiness_spending:
                    hpness_spding += crntPay
            elif crntObj.type == 'asset':
                # if asset, find the asset value
                asset += crntObj.schedule['value_end'][obj_iprd]
                # if it pays, add to income
                income += crntPay
            elif crntObj.type == 'har':
                # if happiness adjustment ratio object, this is the object that directly influences happiness outside of the wealth and spending dependency.
                hAdjRate *= crntObj.adjRate
            else:
                raise NotImplementedError(f'The backend object type (="{crntObj.type}") is not supported.')
        
        net_income = income-spending

        # add new period to the table if the period has not been simulated
        colnames = ['income', 'spending', 'net_income', 'debt', 'asset', 'spd_on_hapns','mth_spd_hapns','wealth','happiness','score','debt_std','debt_mort','debt_car', 'debt_other','debt_ratio']
        colvalues = [income, spending, net_income, debt, asset, hpness_spding,0,0,0,0,debt_std,debt_mort,debt_car,debt_other,0]
        if does_period_exists == False:
            for crntCol in colnames:
                self._score_table[crntCol].append(0)
        # add new value to the current period
        for crntCol, crntVal in zip(colnames, colvalues):
            if crntCol not in ['mth_spd_hapns','wealth','happiness','score','debt_ratio']:
                self._score_table[crntCol][iprd] = crntVal

        # this if statement deals with wealth, debt and asset
        # we separate the case of initial period and later period 
        # because calculation of these values requires their values from previous periods
        if iprd == 0: # if first simulation period globally
            self._score_table['mth_spd_hapns'][iprd] = hpness_spding # use current happiness spending
            self._score_table['wealth'][iprd] = net_income-debt+asset+self.init_cash # use current period wealth + initial wealth coming from the start of the game
        else: # if not first simulation period
            # calculate monthly happiness spending: this period + NPeriodsPerMonth periods before. 
            # If there aren't NPeriodsPerMonth periods simulated yet, go back as far as we can
            self._score_table['mth_spd_hapns'][iprd] = sum(self._score_table['spd_on_hapns'][max(0,iprd-NPeriodsPerMonth+1):(iprd+1)])
            # find debt and asset change
            net_debt_chg = self._score_table['debt'][iprd] - self._score_table['debt'][iprd-1]
            net_asset_chg = self._score_table['asset'][iprd] - self._score_table['asset'][iprd-1]
            # the wealth is the last period wealth + this period net income + debt and assset change from last period
            self._score_table['wealth'][iprd] = self._score_table['wealth'][iprd-1] + self._score_table['net_income'][iprd] - net_debt_chg + net_asset_chg
        
        if self._score_table['wealth'][iprd] == 0:
            if self._score_table['debt'][iprd] - self._score_table['debt_std'][iprd] > 0:
                debt_ratio = 999
            else:
                debt_ratio = 0
        else:
            debt_ratio = (self._score_table['debt'][iprd] - self._score_table['debt_std'][iprd]) / self._score_table['wealth'][iprd]
        self._score_table['debt_ratio'][iprd] = debt_ratio
        
        # calculate the happiness for this period
        self._score_table['happiness'][iprd] = self.__calculate_happiness(self._score_table['wealth'][iprd], self._score_table['mth_spd_hapns'][iprd], adj_ratio=hAdjRate)
        # calculate the score: the average happiness value up to this simulation period
        self._score_table['score'][iprd] = sum(self._score_table['happiness'][:(iprd+1)]) / (iprd+1)

        # bankrupt condition: wealth excluding student debt is less than -2 times annual income
        self.bankrupt = self._score_table['wealth'][iprd]+self._score_table['debt_std'][iprd] < -2*annual_salary
        if self.bankrupt:
            # set the period at which the player went bankrupt
            self.bankrupt_period = iprd

    def __calculate_happiness(self, wealth, mthly_spending, adj_ratio=1):
        """calculates the player's happiness. 
        The happiness is a function of a player's total wealth and qualifying monthly spending. 
        In general, the wealthier a person is, the happier they are. However, wealth ceases to have meaningful impact beyond $1.5M.
        Qualifying monthly spending represents the leisure spending. In general, the more leisure spending one commits to, the happier they are.
        
        Input Argument
        --------------
        wealth:             total wealth of the player
        mthly_spending:     qualifying monthly spending that represents leisure spending. 
        adj_ratio:          a ratio to apply to the raw happiness. This is the way a certain backend object may influence happiness outside of the wealth / spending relationship with happiness.

        Output Argument
        ---------------
        the happiness value
        """
        import math
        return (1/(1+math.exp(-wealth/167000+1))+math.tanh(mthly_spending / 2122))*adj_ratio/2

    # this function provides restrictions what can be set to the self.choices field itself, not the conent of it.
    # for more info on this function, see data model document below:
    # https://docs.python.org/3.11/reference/datamodel.html?highlight=setitem#object.__setitem__
    def __setattr__(self, name, value):
        if name == 'choices':
            if isinstance(value, dict):
                self.__dict__[name] = RestrictedDict(on_set=Player.__on_set_choice, init_dict=value)
            elif isinstance(value, RestrictedDict):
                self.__dict__[name] = value
            else:
                raise TypeError('choices attribute can only accept dictionary or RestrictedDict object.')
        else:
            self.__dict__[name] = value
        
# this class below functionally provides the ability to add additional logic when a dictionary is modified.
# we use this implementation to introduce Python's data model. Please refer to the following link for an in depth read:
# https://docs.python.org/3.11/reference/datamodel.html
class RestrictedDict():
    """Represents a access restricted dictionary"""

    def __init__(self, on_get:Optional[Callable]=None, on_set:Optional[Callable]=None, on_delete:Optional[Callable]=None, init_dict:Optional[dict]=None):
        """Represents a access restricted dictionary.
        
        Input Argument
        --------------
        on_get:     function that is called before a value is accessed via its key. None or a callable with 2 input arguments.

        on_set:     function that is called before a value is set via its key. None or a callable with 3 input arguments.

        on_delete:  function that is called before a value is a key-value pair is removed from the dictionary. None or a callable with 2 input arguments.

        init_dict:  optional dict object whose content will be added upon instantiation of this class without any of the above functions being called. This also means no restriction is put on the content of init_dict.
        
        Input Function Signature
        ------------------------
        on_get(d, name):
            Called before a value in the dictionary is accessed.

            [Inputs]

            d is the RestrictedDict instance from which a key is accessed from.

            name is a str typed argument for key.
        
        on_set(d, name, value):
            Called before a value in the dictionary is about to be set.

            [Inputs]

            d is the RestrictedDict instance of which a new value is about to be added or modified.

            name is the key whose value is about to be added or modified. 

            value is the value object to be added or modified for the name. to access the old value, simply refer to d[name].


            [Outputs]
            
            True if you want the set operation to proceed, eg name and value pair is allowed to be added / modified.
            False if you want to cancel the set operation.


         on_delete(d, name)
            Called before a key and its value in the dictionary is about to be deleted.

            [Inputs]
            
            d is the RestrictedDict instance of which a new value is about to be added or modified.

            name is the key whose value is about to be deleted from the dictionary. 

            [Outputs]
            
            True if deletion is allowed to proceed.
            False if you want to cancel the deletion.
        
        """
        if on_get is not None and RestrictedDict.__check_callable_arg_length(on_get, 2)==False:
            raise TypeError('on_get must be a callable with 2 input arguments.')
        if on_set is not None and RestrictedDict.__check_callable_arg_length(on_set, 3)==False:
            raise TypeError('on_set must be a callable with 3 input arguments.')
        if on_delete is not None and RestrictedDict.__check_callable_arg_length(on_delete, 2)==False:
            raise TypeError('on_delete must be a callable with 2 input arguments.')
        
        if init_dict is None:
            self._data = dict()
        elif isinstance(init_dict, dict): 
            self._data = init_dict
        else:
            raise TypeError('init_dict must be a dictionary or None.')

        self._on_get = on_get
        self._on_set = on_set
        self._on_delete = on_delete
            
    def __check_callable_arg_length(func, n_args):
        if callable(func) == False:
            return False

        from inspect import signature
        return len(signature(func).parameters) == n_args

    # implements the in operator. to learn more, 
    # see https://docs.python.org/3.11/reference/datamodel.html#object.__contains__
    def __contains__(self, item):
        return item in self._data

    # the next three functions define the indexer behavior for read, set and delete actions
    # for more info on these three, please refer to 
    # https://docs.python.org/3.11/reference/datamodel.html?highlight=setitem#object.__getitem__

    def __getitem__(self, name):
        if name not in self._data:
            raise IndexError(f'"{name}" is not in the collection.')
        
        if self._on_get is not None:
            self._on_get(self, name)
        
        return self._data[name]

    def __setitem__(self, name, value):
        if self._on_set is not None:
            if self._on_set(self, name, value) == False:
                return 

        self._data[name] = value

    def __delitem__(self, name):
        if name not in self._data:
            return

        if self._on_delete is not None:
            if self._on_delete(self, name) == False:
                return

        del self._data[name]

    # for a quick introduction of __str__ and __repr__ functions, please refer to
    # https://docs.python.org/3.11/reference/datamodel.html?highlight=setitem#object.__str__ and 
    # https://docs.python.org/3.11/reference/datamodel.html?highlight=setitem#object.__repr__ and 
    # https://stackoverflow.com/questions/1436703/what-is-the-difference-between-str-and-repr

    def __str__(self):
        return str(self._data)

    def __repr__(self) -> str:
        return object.__repr__(self) + '\n' + str(self._data)

