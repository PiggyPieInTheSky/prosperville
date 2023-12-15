# Copyright (C) 2023, Bank of America.  The file below is licensed to LSC for use with HSoF.  All other rights are reserved.
"""This file defines the main backend engine of the game. 
It contains two entities: the Prosperville class and a variable crntGame. 
The Prosperville class maintains the most of the backend logic 
while the crntGame variable is mainly used to store the current running instance of the Prosperville class.

Learning tip: 
What is the difference between a class and an instance? 
See: https://stackoverflow.com/questions/2885385/what-is-the-difference-between-an-instance-and-an-object
"""

import copy
import backend.gameitems as gamedef 

class Prosperville:
    """Represents the backend logic of the game Prosperville."""

    def __init__(self, player_names=['player 1', 'player 2'], init_cash=0.0):
        """Represents the backend logic of the game Prosperville.
        
        Input Arguments
        ---------------
        player_names:  a list of player names. 
        cash:          the amount of cash that all players have at the start of the game

        """

        from backend.player import Player
        
        # indices that indicate the current turn, stage, player and step the game is at
        self.iTurn = 0
        self.iStage = 0
        # the game progression is controlled by self.iStep and self.iPlayer jointly. 
        # self.iStep determines the game step. A step is the smallest unit of progression based on the game design table self.step_table.
        # self.iPlayer indicates the current player that should play the game. 
        # In a single player game, a step is equivalent to the unit progression of the game as when the "Next" button is clicked. 
        # In a multi-player game, the click of a the Next button progresses through step, then players. 
        # for more info, see the Next method of this class. 
        self.iPlayer = 0
        self.iStep = 0

        # expose game definitions
        # this table contains the info about what stage / turn / event each step corresponds to
        # we use a deep copy here because we need to insert random event names to the table when these events are drawn.
        # to learn more about deep copy vs shallow copy, see https://stackoverflow.com/questions/62349558/mutable-and-inmutable-deep-shallow-copies-python
        self.step_table = copy.deepcopy(gamedef.step_table) 
        # these lists define the first / last of something. They are used in loops to quickly find all elements of an entity. 
        self.last_step_of_stage = gamedef.last_step_of_stage # list index: stage index. list value: index of the first step of the stage
        self.last_turn_of_stage = gamedef.last_turn_of_stage # list index: turn index. list value: index of the last turn of the stage
        self.first_step_of_stage = gamedef.first_step_of_stage # list index: stage index. list value: index of the first step of the stage
        self.first_turn_of_stage = gamedef.first_turn_of_stage # list index: stage index. list value: index of the first turn of the stage
        self.last_step_of_turn = gamedef.last_step_of_turn # list index: turn index. list value: index of the last step of the turn
        self.first_step_of_turn = gamedef.first_step_of_turn # list index: turn index. list value: index of the first step of the turn

        # stage and event definitions organized by their names. 
        # These dictionaries are used by front end and back end to quickly find definitions. 
        # for the content of the elements in them, please refer to stagedef.py and eventdef.py files in backend/design
        self.stage_by_name = gamedef.dict_stages
        self.event_by_name = gamedef.dict_events

        # create player objects and save in a list. The last player on the list is AI. 
        self.players = [Player(pn, self, init_cash=init_cash) for pn in player_names] + [Player('AI',self,is_system=True, init_cash=init_cash)]
        
        # a list of player index in self.players based on the score ranking of human players. 
        # for example, if player 2 is the highest scored player, its index 2 is the first element in self.ranked_players.
        # note that we rank bankrupt players among the surviving ones in the same list.
        self.ranked_players = list(range(len(player_names)))
        # a list of players that are not bankrupt. This list is always equal to or a subset of self.players
        self.players_survived = self.players[:-1]

        # expose the current (= initial) stage, event and player so that the front end can correctly display them
        self.crntStage = gamedef.pvStages[0]
        self.crntEvent = gamedef.dict_events[gamedef.pvStages[0].life_event_seq[0]]
        self.crntPlayer = self.players[self.iPlayer]
        self.crntOptionAvailability = self.crntPlayer.get_option_availability(self.crntEvent.name)
        
        # expose numbers of elements. these fields are primarily for front end.
        self.n_players = len(player_names) # number of human players
        self.n_stages = len(gamedef.pvStages) # number of stages in the game
        self.n_turns = gamedef.step_table['turn'][-1]+1 # number of turns in the game
        self.n_steps = len(gamedef.step_table['turn']) # number of steps in the game
        # number of players who are not bankrupt in the game
        self.n_players_survived = self.n_players 

        # a boolean value to indicate if the game has reached the end
        self.is_end = False

        
        
    @property
    def can_step_back(self):
        """gets a boolean value that indicates if the game currently can step backwards"""
        return self.iPlayer>0 or self.iStep!=self.first_step_of_turn[self.iTurn]
    
    @property
    def is_random_event_step(self):
        """gets a boolean value that indicates if the current step is a random event step"""
        return self.step_table['is_random_event_step'][self.iStep]

    @property
    def is_last_player(self):
        """gets a boolean value that indicates if the current player is the last player to play in the current turn"""
        
        if self.n_players_survived == 0: # if no one survived (everyone is bankrupt)
            return False
        # returns true if last player among surviving or AI player
        return self.players[self.iPlayer] in [self.players_survived[-1], self.players[-1]]
    
    def next(self):
        """Progresses the game to the next.
        This method moves the players first. If the last player has played, it progresses to the next step."""

        # game progression lets one player make all moves for a turn, then moves to the next player. Once all players are done, it moves to the next turn. 
        # a turn is a unit of game progression within which players can go back and forth to make changes to what they selected for non-random events. 
        # a turn may have multiple steps depending on how many non-random events are there in the turn. 
        # a player cannot make changes to their choices in a previous turn. 
        # a random event is a turn of its own. this turn only has one step. 
        # a stage may have multiple turns. 


        # if the game is at last step of the current turn
        if self.iStep == self.last_step_of_turn[self.iTurn]:
            if self.is_last_player: # if the current player is the last player to play, this is when a turn ends
                # simulate and calculate the score for each human player
                self.__score_players()
                # rank human players
                self.ranked_players = self.__rank_players()
                # make choices for the AI, then score the AI choices. 
                # AI makes the best choice among all the options to maximize the score at the end of the current stage. 
                self.__simulate_for_ai()

            # if the game reached the end: because either no one survived or there is no more step left in the game
            if self.n_players_survived ==0 \
                or (
                    self.iStep == self.last_step_of_stage[-1] # last step of the current stage
                    and (self.is_random_event_step or (self.is_random_event_step==False and self.is_last_player)) # step is random event step or last player just played a non-random event step
                ):
                # indicates the game has ended.
                self.is_end = True
            elif self.is_last_player: # if last player at the last step of the current turn
                # move the step counter forward
                self.iStep += 1 
                
                # move to the next player
                if self.is_random_event_step or self.step_table['event_name'][self.iStep] == '':
                    # random event or the step has no event, set AI as the current player 
                    self.iPlayer = -1
                else: # if there are non-random events in the step
                    # move player counter to the first player. aka making the first player ready to play the next turn
                    self.iPlayer = 0
                    # to make sure we move to the surviving player if 0 is bankrupt already
                    if self.players[self.iPlayer].bankrupt:
                        self.__progress_player()
            else: # if not the last player at the last step of the current turn, ie there is still player to go in the turn
                # move to the next player, return the step to the beginning of the turn
                self.__progress_player()
                self.iStep = self.first_step_of_turn[self.iTurn]
        else: # if the current step is not the last step of the turn, move the step counter forward only
            self.iStep += 1 
        
        # update the corresponding stage and turn counters
        self.iStage, self.iTurn = self.step_table['stage'][self.iStep], self.step_table['turn'][self.iStep]
        
        # update the definition objects so the front end modules can correctly display them
        self.__update_crnt_objs()
            
    def back(self):
        """requests to move the game backwards. The request may not be accepted if the game is at the beginning of a turn for the first player."""
        
        if not self.can_step_back:
            return
        
        if self.iStep == self.first_step_of_turn[self.iTurn]: 
            # if the game is at first step of the turn, move player back
            self.__progress_player(back=True)
            # set the step counter to the last step of the current turn. since that's where the previous player left off when the game moved to the next player. 
            self.iStep = self.last_step_of_turn[self.iTurn]
        else: # if the current step is not the first step of the turn, move the step back
            self.iStep -= 1
            
        # update the corresponding stage and turn counters based on the newly set step counter according to the step table
        self.iStage, self.iTurn = self.step_table['stage'][self.iStep], self.step_table['turn'][self.iStep]
        
        # update the current object fields
        self.__update_crnt_objs()

    def __progress_player(self, back=False):
        """Progresses current player counter (iPlayer field) to the next player. If all human players are bankrupt, the player counter does not change."""
        # set the step size
        step_size = -1 if back else 1
        # move tentatively one step away from the current player
        iplr = self.iPlayer + step_size
        # loop through to see if the player we moved to is not bankrupt
        while iplr >=0 and iplr < self.n_players: # the loop condition is if the player counter is within the range available given the number of human players we have
            # if the player we just moved to is not bankrupt
            if self.players[iplr].bankrupt == False:
                # set the current player indicator to this player, then exit the loop
                self.iPlayer = iplr
                break
            else: # if the player we just moved to is bankrupt, move the the next player
                iplr += step_size
    
    def __rank_players(self):
        """Rank all human players then return their player indices from highest score to lowest. Bankrupt players are ranked along the surviving players in the same return list. """
        lstScore = [-self.players[i].score for i in range(self.n_players)]
        return sorted(range(self.n_players), key=lambda k: lstScore[k])
    
    def __update_crnt_objs(self):
        '''updates the current stage, event and player fields'''
        
        self.crntStage = gamedef.pvStages[self.iStage]
        
        # if the current turn is a random event turn, draw a random event card.
        # this will add the drawn event name to the step table for the current step
        if self.is_random_event_step: 
            self.__draw_random_event()
        
        if self.step_table['event_name'][self.iStep] != '': 
            # if the step table has an event name for the current step
            # take the event name out of the step table, then find the event object from self.event_by_name dictionary
            # note that the final stage has no event. thus the step table cannot give a valid event name
            self.crntEvent = self.event_by_name[self.step_table['event_name'][self.iStep]]
        else:
            self.crntEvent = None
            self.crntOptionAvailability = None

        # update the current player instance
        self.crntPlayer = self.players[self.iPlayer]
        if self.crntEvent is not None:
            self.crntOptionAvailability = self.crntPlayer.get_option_availability(self.crntEvent.name)
        
        

    def __score_players(self):
        """Score all human players up to the end of the turn"""
        # loop through all surviving players
        iplyr = 0
        while iplyr < len(self.players_survived):
            crntPlayer = self.players_survived[iplyr]
            # add backend objects relevant to the current turn to the player in the loop 
            self.___add_bkedobj_2_player(crntPlayer, self.iTurn, self.iTurn)
            # simulate all periods corresponding to the current turn for the current player in the loop
            crntPlayer.simulate(gamedef.first_period_of_turn[self.iTurn], gamedef.last_period_of_turn[self.iTurn])
            
            # if the current player in the loop goes bankrupt after the simulation
            if crntPlayer.bankrupt:
                # reduce the surviver count, and remove the current player from the surviver list
                self.n_players_survived -= 1
                self.players_survived.remove(crntPlayer)
                # note that because we removed a player in the list, the current counter iplyr now points to the player next to the player we just removed
            else: # if the current player in the loop is not bankrupt after the simulation
                # progresses to the next player in the loop
                iplyr += 1

        # if there is still surviver
        if self.n_players_survived > 0:
            # update the current player of the game to be the last surviver. this update helps us set to the current next step. 
            # recall in Next method that this method (__score_players) is only called when the current player is last player prior to simulation
            # to meet this same condition, we move the current player to the last surviver
            self.iPlayer = self.players.index(self.players_survived[-1])
        else: # if nobody survived, set to AI
            self.iPlayer = -1
    
    def ___add_bkedobj_2_player(self, crntPlayer, first_turn, last_turn):
        """Adds backend objects to a given player over given turns
        
        Input Arguments
        ---------------
        crntPlayer:     a Player object 
        first_turn:     index of the first turn
        last_turn:      index of the last turn
        """

        # get a list of event names for all the steps of the turns
        evt_names = [self.step_table['event_name'][i] for i in range(self.first_step_of_turn[first_turn], self.last_step_of_turn[last_turn]+1)] 

        for crntEvtNm in evt_names: # loop through each event name
            
            # gather backend objects according to choices
            if crntEvtNm in crntPlayer.choices: 
                # if the event name is in the player choice dictionary, meaning if the player has made a choice for the event
                # note not all events have choices

                # get the option definition corresponding to the player's choice
                crntOPtionDef = self.event_by_name[crntEvtNm].options[crntPlayer.choices[crntEvtNm]]
                # some choices do not have a backend object. This usually happens if the choice does nothing, eg: Q:do you want to take a part time job? A: No. 
                if crntOPtionDef.name not in gamedef.pvBkEndObj_by_name: continue

                # get the backend object indexed by the option definition name
                bkedObj_list = gamedef.pvBkEndObj_by_name[crntOPtionDef.name]
            elif crntEvtNm in gamedef.pvBkEndObj_by_name:
                # if the event has a backend object of its own (eg random event)
                bkedObj_list = gamedef.pvBkEndObj_by_name[crntEvtNm]
            else: # this happens when we simulate ahead of the game play for AI (eg when random events are not drawn for the current stage)
                continue

            # add gathered backend objects to the current player
            for bkedObj in bkedObj_list:
                if bkedObj.start_period == -1: # if event start period is not set
                    # set event start period to the current period of the step
                    bkedObj = copy.deepcopy(bkedObj)
                    bkedObj.start_period = self.step_table['period_first'][self.iStep]
                
                # special logic for the first job: adjust salary if college degree
                if crntEvtNm == 'stg2_firstjob' and bkedObj.type=='salary' and 'stg1_college' in crntPlayer.choices:
                    college_option_name = self.event_by_name['stg1_college'].options[crntPlayer.choices['stg1_college']].name
                    # if the player in stage 1 chose public school
                    if college_option_name in ['stg1_college_public_in_state', 'stg1_college_public_out_state']:
                        bkedObj = copy.deepcopy(bkedObj)
                        bkedObj.amount = bkedObj.amount * 1.1
                        bkedObj.calculate_schedule()
                    elif college_option_name == 'stg1_college_ivy_league':
                        bkedObj = copy.deepcopy(bkedObj)
                        bkedObj.amount = bkedObj.amount * 1.15
                        bkedObj.calculate_schedule()

                # special logic for the second house buying event
                if 'stg2_firsthouse_rent' in crntPlayer.choices \
                    and ('stg3_house_small' in crntPlayer.choices or 'stg3_house_mid' in crntPlayer.choices or 'stg3_house_big' in crntPlayer.choices) \
                    and bkedObj.type=='salary':
                    # if the player rent in stage 2 (no house) and bought a house in stage 3, the new house is a first house for the player
                    # we need to remove the rental income by ignoring it in the loop
                    continue
                
                # add the backend object to the player's list so that the simulation can take into account this object
                crntPlayer.selected_bked_objs.append(bkedObj)

        # since class objects are mutable, returning the player object is technically redundant. 
        # Read below to see why:
        # https://www.mygreatlearning.com/blog/understanding-mutable-and-immutable-in-python/
        return crntPlayer

    def __simulate_for_ai(self):
        '''make best choices for the current stage for the AI player. This is a brute force implementation of optimizing over stage choices.'''

        from collections import deque
        from itertools import product
        import copy

        # define two lists respectively for event names and the list of options the event offers
        # note options variable is a list of lists. Each inner list has all options of an event. The outer list enumerates all events. 
        event_names, options = deque(), deque()
        # this loop finds all events relevant to the current stage, then saves all options of those events in options 
        # the loop goes through all steps of the current stage
        for istp in range(self.first_step_of_turn[self.iTurn], self.last_step_of_turn[self.iTurn]+1):
            # if the event is empty (eg random event not drawn) or it has no option (last stage), skip
            if self.step_table['event_name'][istp] not in self.event_by_name or self.event_by_name[self.step_table['event_name'][istp]].options is None or len(self.event_by_name[self.step_table['event_name'][istp]].options) == 0:
                continue
            # add the event name to the list event_names
            event_names.append(self.step_table['event_name'][istp])
            # for this event, add all its options to the end of list options
            options.append(range(len(self.event_by_name[self.step_table['event_name'][istp]].options)))

        # if there is no choice in this turn, just simulate without picking optimal options
        if len(options) == 0:
            # add backend objects to the current AI player for the current turn
            self.___add_bkedobj_2_player(self.players[-1], self.iTurn, self.iTurn)
            # simulate for the current AI player to the last period of the stage
            self.players[-1].simulate(gamedef.first_period_of_turn[self.first_turn_of_stage[self.iStage]], gamedef.last_period_of_turn[self.last_turn_of_stage[self.iStage]])
            return

        # save the best results. 
        # The structure of the variable: [[best surviving score, player obj with that score], [best bankrupt score, player obj with that score]]
        bestResults = [[-99999,None],[-99999,None]]
        # remove the current game reference so that the deep copy below does not make a whole new copy of the game instance and all its players
        self.players[-1].crntGame = None
        self.players[-1].choices.player = None
        # enumerate all choice combinations. this is a brute force method
        for crntChoice in product(*options):
            altPlayer = copy.deepcopy(self.players[-1])
            altPlayer.crntGame = self # set the current game instance back
            altPlayer.choices.player = altPlayer
            infeasible_choice = False
            # add new possible choices, these are our candidate choice combination
            for ievt in range(len(event_names)):
                try:
                    altPlayer.choices[event_names[ievt]] = crntChoice[ievt]
                except ValueError: 
                    # this error is raised if the current choice is not feasible for the player. 
                    # some choices cannot be selected together (eg someone who's not in college cannot choose to live in a dorm)
                    infeasible_choice = True
            if infeasible_choice:
                continue
            self.___add_bkedobj_2_player(altPlayer, self.iTurn, self.iTurn)
            # simulate / score based on the candidate choice combination all the way to the end of the stage
            altPlayer.simulate(gamedef.first_period_of_turn[self.first_turn_of_stage[self.iStage]], gamedef.last_period_of_turn[self.last_turn_of_stage[self.iStage]])
            # 1 if bankrupt, 0 otherwise
            islot = int(altPlayer.bankrupt) 
            # find the end of stage score
            end_stage_score = altPlayer._score_table['score'][min(self.step_table['period_last'][self.last_step_of_stage[self.iStage]], len(altPlayer._score_table['score'])-1)]
            # if the choice combo has better score than the previously known best score, update
            if bestResults[islot][0] < end_stage_score:
                bestResults[islot][0] = end_stage_score
                bestResults[islot][1] = altPlayer

        # find the best results
        if bestResults[0][1] is not None:
            # if there is a best score and the player is not in bankrupt, use that for AI
            self.players[-1] = bestResults[0][1]
        else: # if all choices lead to bankruptcy, pick the best results among them
            self.players[-1] = bestResults[1][1]
            
    def __draw_random_event(self):
        """draws a random event for the current stage"""

        if not self.is_random_event_step: return

        # we use multinomial distribution to draw from a list of random events available to the current stage
        # the list is saved in the stage definition's random_event field: self.crntStage.random_event
        # the probability of each event that can take place is stored in self.crntStage.backend['rnd_evt_prob']
        # the multinomial distribution is a distribution that describes the probability of one of a list of things happening once at a time at random
        # for more details on multinomial distribution, please see https://en.wikipedia.org/wiki/Multinomial_distribution
        # We use numpy's multinomial function to provide a random draw from the multinomial distribution. 
        # for more details on numpy's implementation of the multinomial function, please refer to 
        # https://numpy.org/doc/stable/reference/random/generated/numpy.random.multinomial.html

        import numpy as np
        from numpy.random import multinomial
        # make one draw from the multinomial distribution. The probability of each random event is provided by self.crntStage.backend['rnd_evt_prob']
        drawRstMN = multinomial(1, self.crntStage.backend['rnd_evt_prob'])
        # find which event is actually drawn. the result is the index of the event
        iRndEvt = np.where(drawRstMN==1)[0][0]
        # save the event definition's name in the step table
        self.step_table['event_name'][self.iStep] = self.crntStage.random_event[iRndEvt]

# this variable is shared among the Jupyter notebook, the backend modules, and GUI modules
# it represents the current running game
crntGame = None

