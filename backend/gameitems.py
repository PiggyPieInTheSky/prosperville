# Copyright (C) 2023, Bank of America.  The file below is licensed to LSC for use with HSoF.  All other rights are reserved.
 Copyright (C) 2023, Bank of America.  The file below is licensed to LSC for use with HSoF.  All other rights are reserved.
""This file processes stage and event definitions into mapping tables so that they are easily accessed by the game logic. 
The step table is also created here. The script also creates backend objects that are associated with each event."""
import math
import numpy as np
from collections import defaultdict

from backend.design import NPeriodsPerMonth
# load the event definitions as a list
from backend.design.eventdef import pvEvents
# load the stage definitions as an ordered list
from backend.design.stagedef import pvStages


# tables that show the first / last step (list element) of a given turn / stage (list index)
last_step_of_stage, last_turn_of_stage, first_step_of_stage, first_turn_of_stage = [0]*len(pvStages), [0]*len(pvStages),[0]*len(pvStages),[0]*len(pvStages)
last_step_of_turn, first_step_of_turn = [], []

# step table that shows how step, stage, turn, event and simulation period are mapped
step_table = defaultdict(list)
itrn, istp = 0, 0
preGameAge = pvStages[0].init_age - 1
for istg in range(len(pvStages)):
    first_step_of_stage[istg], first_turn_of_stage[istg] = istp, itrn
    first_step_of_turn.append(istp)
    crntStageDef = pvStages[istg]
    pFrist = (crntStageDef.init_age-preGameAge-1)*NPeriodsPerMonth*12
    pLast = (crntStageDef.end_age-preGameAge)*NPeriodsPerMonth*12 - 1
    
    # if no events, usually the last stage
    if len(pvStages[istg].life_event_seq) == 0:
        step_table['stage'].append(istg)
        step_table['turn'].append(itrn)
        step_table['ievent_in_stage'].append(0)
        step_table['stage_name'].append(crntStageDef.name)
        step_table['event_name'].append('')
        step_table['period_first'].append(pFrist)
        step_table['period_sim_last'].append(0)
        step_table['period_last'].append(pLast)
        step_table['is_random_event_step'].append(False)
        step_table['is_last_turn_of_stage'].append(False)
        step_table['is_last_step_of_stage'].append(False)
        last_step_of_stage[istg], last_turn_of_stage[istg] = istp, itrn
        last_step_of_turn.append(istp)

        istp += 1

    # if stage has events
    for iCrntEvDef in range(len(pvStages[istg].life_event_seq)):
        crntEvtNm = crntStageDef.life_event_seq[iCrntEvDef]
        step_table['stage'].append(istg)
        step_table['turn'].append(itrn)
        step_table['ievent_in_stage'].append(iCrntEvDef)
        step_table['stage_name'].append(crntStageDef.name)
        step_table['event_name'].append(crntEvtNm)
        step_table['period_first'].append(pFrist)
        step_table['period_sim_last'].append(0)
        step_table['period_last'].append(pLast)
        

        if crntStageDef.n_random_event_turn < 0:
            raise Exception(f'In stage definition for "{crntStageDef.name}", n_random_event_turn should be non-negative.')
        
        # last life stage event of the current stage
        if crntEvtNm == crntStageDef.life_event_seq[-1]: 
            last_step_of_turn.append(istp)
            # if the stage has random event turns
            if crntStageDef.n_random_event_turn!= 0:
                if crntStageDef.random_event is None or len(crntStageDef.random_event)==0:
                    raise Exception(f'In stage definition for "{crntStageDef.name}", random_event is not defined even though n_random_event_turn!=0')
                if crntStageDef.rand_event_weight is None or len(crntStageDef.rand_event_weight) != len(crntStageDef.random_event):
                    raise Exception(f'In stage definition for "{crntStageDef.name}", the number of elements in rand_event_weight and random_event is not consistent.')
                # finish the current turn
                step_table['is_random_event_step'].append(False)
                step_table['is_last_turn_of_stage'].append(False)
                step_table['is_last_step_of_stage'].append(False)
                prlen = (pLast - pFrist + 1) / (crntStageDef.n_random_event_turn+1)
                # add new random event turns
                for ir in range(crntStageDef.n_random_event_turn):
                    # add a new step for the random event card turn
                    itrn += 1; istp += 1
                    step_table['stage'].append(istg)
                    step_table['turn'].append(itrn)
                    step_table['ievent_in_stage'].append(ir)
                    step_table['stage_name'].append(crntStageDef.name)
                    step_table['event_name'].append('')
                    step_table['period_first'].append(math.ceil(prlen*(ir+1)+pFrist-1))
                    step_table['period_sim_last'].append(0)
                    step_table['period_last'].append(math.ceil(prlen*(ir+2)+pFrist-1))
                    step_table['is_random_event_step'].append(True)
                
                    last_step_of_turn.append(istp)
                    first_step_of_turn.append(istp)

                    step_table['is_last_turn_of_stage'].append(ir == crntStageDef.n_random_event_turn-1)
                    step_table['is_last_step_of_stage'].append(ir == crntStageDef.n_random_event_turn-1)
                
            else:
                step_table['is_last_turn_of_stage'].append(True)
                step_table['is_last_step_of_stage'].append(True)
            last_step_of_stage[istg], last_turn_of_stage[istg] = istp, itrn
            
        else: # if the current life stage event is not the last of its stage
            step_table['is_random_event_step'].append(False) # random event turn is always the last turns of a stage
            step_table['is_last_turn_of_stage'].append(False)
            step_table['is_last_step_of_stage'].append(False)
            
        istp += 1
    
    itrn += 1

# find the first and last simulation periods for each turn
first_period_of_turn = [0] * len(first_step_of_turn)
last_period_of_turn = [0] * len(first_step_of_turn)
for iRefTurn in range(1, len(last_step_of_turn)):
    first_period_of_turn[iRefTurn] = step_table['period_first'][first_step_of_turn[iRefTurn]]
    last_period_of_turn[iRefTurn-1] = step_table['period_first'][first_step_of_turn[iRefTurn]] - 1
    # update period_sim_last column in the step table
    for istp in range(first_step_of_turn[iRefTurn - 1], last_step_of_turn[iRefTurn - 1]+1):
        step_table['period_sim_last'][istp] = step_table['period_first'][first_step_of_turn[iRefTurn]] - 1
step_table['period_sim_last'][-1] = step_table['period_last'][-1]
last_period_of_turn[-1] = step_table['period_last'][-1]

# a dictionary of events by their name
dict_events = {c.name:c for c in pvEvents}

# add a mapping table to go from stage name to stage definition object
dict_stages = dict()
for crntStage in pvStages:
    dict_stages[crntStage.name] = crntStage
    # process random event odds
    if crntStage.n_random_event_turn == 0:
        continue
    for crntRndEvtNm in crntStage.random_event:
        if crntRndEvtNm not in dict_events:
            raise Exception(f'Random event name "{crntRndEvtNm}" is not defined in backend/design/eventdef.py for stage "{crntStage.name}"')
    total_weight = sum(crntStage.rand_event_weight)
    crntStage.backend['rnd_evt_prob'] = np.array([c/total_weight for c in crntStage.rand_event_weight])

# create backend objects. Here we use a dictionary to map the backend object type defined in the event defition to its corresponding backend object class.
from backend import Loan, Salary, Asset, Expense, HappinessAdjustmentRatio
bked_obj_map = {'salary':Salary, 'loan':Loan, 'expense':Expense, 'asset':Asset, 'har':HappinessAdjustmentRatio}
# this dictionary has all the backend objects. The dictionary is organized by the event names. 
# Under each event name, there is a list of backend objects that are associated with the event.
pvBkEndObj_by_name = dict()
# this helper function converts a backend object definition (=backend_def) to backend object, 
# then save it to backend_def under the key that equals input argument name.
def __instantiate_backend_objects(name, backend_def):
    if backend_def is None:
        return
    if isinstance(backend_def, dict):
        lst_obj = [backend_def]
    elif isinstance(backend_def, list):
        lst_obj = backend_def
    else:
        raise Exception('Backend object type can only be dict or list for defition named "{}"')
    rtn_list = []
    for crntDef in lst_obj:
        # instantiates the backend object, then add to the list. 
        # Note that "bked_obj_map[crntDef['type']]"" part of the line returns a class according to the type defined in crntDef
        # and "(crntDef)" part of the line instantiates the class.
        rtn_list.append(bked_obj_map[crntDef['type']](crntDef))
    pvBkEndObj_by_name[name] = rtn_list

for crntEvtDef in pvEvents:
    if crntEvtDef.backend is not None:
        if crntEvtDef.name in pvBkEndObj_by_name:
            raise Exception(f'Event name "{crntEvtDef.name}" is shared with another object. This is likely caused by an event definition and an option definition share a same name.')
        __instantiate_backend_objects(crntEvtDef.name, crntEvtDef.backend)
    if crntEvtDef.options is not None and len(crntEvtDef.options)!=0:
        # if current event has options, then loop through each option definition
        for crntOptionDef in crntEvtDef.options:
            if crntOptionDef.name in pvBkEndObj_by_name:
                raise Exception(f'Option name "{crntOptionDef.name}" is shared with another object. This is likely caused by an event definition and an option definition share a same name.')
            __instantiate_backend_objects(crntOptionDef.name, crntOptionDef.backend)


