### Food Choice Python version is updated in June 2024
### by Xinwei Samantha Han (RA at Columbia Center for Eating Disorders)
### Based on Food Choice Task Matlab Version(2016) by Dr. Karin Foerde and Dr. Joanna Steinglass
### Python version was created by Serena J. Gu (RA) on Nov.18 2022

from fct_library import *

def run():
    import os
    import re
    import glob
    from psychopy import visual, core, data, logging, gui
    from psychopy.hardware.emulator import launchScan
    import numpy as np
    import pandas as pd
    import constants
    import psychopy
    _thisDir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(_thisDir)

    #########################Experiment Imformation########################
    # psychopy.useVersion('2022.2.4')
    expName = 'FCT_2024'
    while True:
        expInfo = {'participant': '', 'TR': 1.000, 'volumes': 400, 'sync': 't',
                   'order': ['Condition_1_HT', 'Condition_1_TH', 'Condition_2_HT', 'Condition_2_TH'],
                   'block': ['all', 'health', 'taste', 'choice'],
                   'h_list': ['Test', 'Test1', 'Test2', 'foodlist1','foodlist2','foodlist3','foodlist4','foodlist5', 'foodlist6'],
                   't_list': ['Test', 'Test1', 'Test2', 'foodlist1','foodlist2','foodlist3','foodlist4','foodlist5', 'foodlist6'],
                   'c_list': ['Test', 'Test1', 'Test2', 'foodlist1','foodlist2','foodlist3','foodlist4','foodlist5', 'foodlist6'],
                   'time point (enter number only)': '',
                   'EDRU admission number (enter number only)': '',
                   'excluded reference food': '',
                   'backup reference food': ['saltines', 'other'],
                   'if "other", please specify': ''}
        MR_settings = {'TR': expInfo['TR'], 'volumes': expInfo['volumes'], 'sync': expInfo['sync'], 'skip': 0}
        dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
        if dlg.OK == False:
            core.quit()  # user pressed cancel

        # validate input for time point
        time_pt_str = expInfo['time point (enter number only)']
        time_pt_val = None
        try:
            time_pt_val = int(time_pt_str)
        except ValueError:
            print()
            error_msg = "Please only enter a number for time point (eg. 1, 2...)"
            error_dlg = gui.Dlg(title="Error")
            error_dlg.addText(error_msg)
            error_dlg.show()
            if error_dlg.OK:
                continue       
        if time_pt_val is not None:
            time_pt = 'T' + str(time_pt_val)
        else:
            print("missing time point value")
            
     # validate input for admission point
        admit_str = expInfo['EDRU admission number (enter number only)']
        admit_val = None
        try:
            admit_val = int(time_pt_str)
        except ValueError:
            print()
            error_msg = "Please only enter a number for the admission number (eg. 1, 2...)"
            error_dlg = gui.Dlg(title="Error")
            error_dlg.addText(error_msg)
            error_dlg.show()
            if error_dlg.OK:
                continue       
        if admit_val is not None:
            admit_pt = 'Admit' + str(admit_val)
        else:
            print("missing EDRU admission number value")
        
        # validate input for excluding reference food
        foodlist = constants.FOODLIST
        excluded_ref = expInfo['excluded reference food']
        if excluded_ref:
            entered_foods = [food.strip() for food in expInfo['excluded reference food'].split(',')]
            invalid_foods = [food for food in entered_foods if food not in foodlist]
            if invalid_foods:
                error_msg = f"Invalid excluded reference food entries detected: {', '.join(invalid_foods)}. Please correct them. " \
                            f"Make sure there is a comma ',' between two food items."
                error_dlg = gui.Dlg(title="Error")
                error_dlg.addText(error_msg)
                error_dlg.show()
                if error_dlg.OK:
                    continue
            else:
                excluded_ref = entered_foods
                print(f"excluded reference food: {excluded_ref}")

        # validate input for backup reference food
        ref_backup = expInfo['if "other", please specify']
        if ref_backup:
            entered_ref_food = expInfo['if "other", please specify'].strip()
            invalid_ref_food = entered_ref_food if entered_ref_food not in foodlist else None
            if invalid_ref_food:
                error_msg = f"Invalid back-up reference food entry detected: {invalid_ref_food}. Please correct it. "
                error_dlg = gui.Dlg(title="Error")
                error_dlg.addText(error_msg)
                error_dlg.show()
                if error_dlg.OK:
                    continue
            else:
                ref_backup = entered_ref_food
                print(f"entered back-up reference food: {ref_backup}")
                break
        else:
            ref_backup = expInfo['backup reference food']
            if ref_backup == 'other':
                error_msg = "Please select or enter a back-up reference food"
                error_dlg = gui.Dlg(title="Error")
                error_dlg.addText(error_msg)
                error_dlg.show()
                if error_dlg.OK:
                    continue
            break

    # save experiment info
    expInfo['date'] = data.getDateStr()  # add a simple timestamp
    expInfo['expName'] = expName
    test_block = expInfo['block']
    #print(f"#################################{expInfo}")

    # read input files
    order_list = f"{_thisDir}/order/{expInfo['order']}.xlsx"
    h_list = f"{_thisDir}/lists/{expInfo['h_list']}.csv"
    t_list = f"{_thisDir}/lists/{expInfo['t_list']}.csv"
    c_list = f"{_thisDir}/lists/{expInfo['c_list']}.csv"
    hList = pd.read_csv(h_list)
    tList = pd.read_csv(t_list)
    cList = pd.read_csv(c_list)
    order = pd.read_excel(order_list)
    cond = re.findall(r'\d+', expInfo['order'])
    condition = int(cond[0])
    # condition == 1 -> ratings will not be reversed(0); condition == 2 -> ratings will be reversed(1)
    rating_reversed = 0 if condition == 1 else 1

    #########################Saving Data File Info########################
    save_all = f"{_thisDir}/data/{expInfo['participant']}_{time_pt}_{admit_pt}_{expInfo['date']}_all"
    save_filename = f"{_thisDir}/data/{expInfo['participant']}_{time_pt}_{admit_pt}_{expInfo['date']}_behav"
    save_choice_output = f"{_thisDir}/data/{expInfo['participant']}_{time_pt}_{admit_pt}_{expInfo['date']}_choiceoutput"
    save_health = f"{_thisDir}/data/{expInfo['participant']}_{time_pt}_{admit_pt}_{expInfo['date']}_health"
    save_taste = f"{_thisDir}/data/{expInfo['participant']}_{time_pt}_{admit_pt}_{expInfo['date']}_taste"
    save_choice = f"{_thisDir}/data/{expInfo['participant']}_{time_pt}_{admit_pt}_{expInfo['date']}_choice"
    save_foodtask = f"{_thisDir}/data/{expInfo['participant']}_{time_pt}_{admit_pt}_{expInfo['date']}_foodtask"

    logFile = logging.LogFile(save_filename+'.log', level=logging.DEBUG)
    logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

    output = []
    columns = ['food_item', 'SubID', 'time point','admit_number', 'date', 'ref_food', 'condition',
               'health_recorded_response', 'h_rt', 'health_rating', 'himage_onset',
               'taste_recorded_response', 't_rt', 'taste_rating', 'timage_onset',
               'choice_rating', 'c_rt', 'cimage_onset',
               'available', 'fat', 'hilo', 'rating_reversed']
    output_df = pd.DataFrame(output, columns=columns)

    #########################Experiment Start########################
    win = visual.Window([1440, 900], fullscr=True, winType='pyglet', monitor="testMonitor",
                        units="height", color="#000000", colorSpace='hex', blendMode="avg")
    win.mouseVisible = False
    
    welcome_text = newText(win, "welcome_text", "Welcome!")
    welcome_text.draw()
    win.flip()
    newKey(keyList=['space'])

    def get_food_name(food_full):
        return ' '.join(re.findall(r'/([\w .\& .\%]+).jpg', food_full))

    def read_file():
        # read from existing health and taste rating file
        pattern = f"{_thisDir}/data/{expInfo['participant']}_{time_pt}_{admit_pt}_*_all.csv"
        # check if we found any files with the pattern
        matching_files = glob.glob(pattern)
        if matching_files:
            input_df = pd.read_csv(matching_files[0])
            # print(matching_files)
        else:
            print("No rating file found for this participant.")
            return None
        return matching_files[0], input_df

    def get_rating(order_row, h_or_t, existed_file):
        newInstruction(win, "inst1", order_row, keyList=['1', 'space'])
        newInstruction(win, "inst2", order_row, keyList=['1', 'space'])
        newInstruction(win, "inst3", order_row, keyList=['1', 'space'])
        foodList = hList if h_or_t == "h" else tList
        duration = expInfo['volumes'] * expInfo['TR']
        globalClock = core.Clock()
        vol = launchScan(win, MR_settings, globalClock=globalClock, wait_msg='loading...')
        # event.waitKeys(keyList =['t'])
        get_ready = newTextWait(win, "ready", constants.GETREADY)
        start_time = core.getTime()
        for index, food in foodList.iterrows():
            food_name = food['food']
            trial_start = food['trialstart']
            start_cross = core.getTime() - start_time
            newCross(win, wait_time=trial_start - start_cross)
            ht_image_onset = core.getTime() - start_time
            key = showImage(win, food_name, 4.0, order_row['rating'], zoom=0.5)
            if key is None:
                tooLate = newText(win, "tooLate", "Too late!")
                tooLate.draw()
                win.flip()
                core.wait(1.0)
                key = [['0'], None]
                corrected_rating = None
            else:
                corrected_rating = int(key[0][0]) if condition == 1 else 6 - int(key[0][0])
            temp_list = (key[0][0], key[1], corrected_rating, ht_image_onset)
            temp_index = output_df[output_df['food_item'] == get_food_name(food_name)].index
            if h_or_t == "h":
                output_df.loc[temp_index, ['health_recorded_response', 'h_rt', 'health_rating', 'himage_onset']] = temp_list
            else:
                output_df.loc[temp_index, ['taste_recorded_response', 't_rt', 'taste_rating', 'timage_onset']] = temp_list
            output_df.to_csv(f"{save_all}.csv", index=False) if existed_file is None else output_df.to_csv(existed_file, index=False)
        end_of_block = newText(win, "end_of_block", constants.ENDOFBLOCK)
        end_of_block.draw()
        win.flip()
        newKey(keyList=['space'])

    def get_ref_food():
        # find a list of neutral food
        def find_ref(a, b):
            neutral_df = output_df[
                ((output_df['health_rating'] == float(a)) & (output_df['taste_rating'] == float(b))) |
                ((output_df['health_rating'] == float(b)) & (output_df['taste_rating'] == float(a)))]
            # print(output_df['health_rating'].dtype)
            return neutral_df['food_item'].tolist()

        # exclude the reference food chosen previously
        if excluded_ref:
            results = [item for x in ['3', '4', '2'] for item in find_ref('3', x) if item not in excluded_ref]
        else:
            results = [item for x in ['3', '4', '2'] for item in find_ref('3', x)]
        results.append(ref_backup)
        ref_food = results[0]
        ref = "stimuli/" + ref_food + ".jpg"
        return ref, ref_food

    def get_choice(ref, ref_food, existed_file):
        # get instruction food
        dummyfood = constants.DUMMYFOOD
        blueberry = constants.BLUEBERRY
        raspberry = constants.RASPBERRY

        # show reference food
        ref_image = newImage(win, image=ref, zoom=0.5, pos=(0, -0.25))
        ref_text = newText(win, "ref_text", constants.REF_TEXT, pos=(0, 0.2))
        ref_image.draw()
        ref_text.draw()
        win.flip()
        newKey(keyList=['space'])

        # show choice phase instruction
        inst_row = {'inst1': constants.C_INST1, 'inst2': constants.C_INST2}
        # instruction 1
        inst1 = newText(win, "inst1", constants.C_INST1, pos=(0, 0.25))
        inst_rating = newText(win, "c_rating", constants.C_RATING, pos=(0, -0.3))
        inst_refimage = newImage(win, blueberry, zoom=0.45, pos=(-0.35, -0.15))
        inst_image = newImage(win, raspberry, zoom=0.45, pos=(0.35, -0.15))
        inst1.draw()
        inst_rating.draw()
        inst_refimage.draw()
        inst_image.draw()
        win.flip()
        newKey(keyList=['space'])
        # instruction 2
        newInstruction(win, "inst2", inst_row, keyList=['space'])

        # get time
        duration = expInfo['volumes'] * expInfo['TR']
        globalClock = core.Clock()
        vol = launchScan(win, MR_settings, globalClock=globalClock, wait_msg='loading...')
        # event.waitKeys(keyList =['t'])
        get_ready = newTextWait(win, "ready", constants.GETREADY)
        start_time = core.getTime()

        snack_list = []
        counter = 0
        for _, food in cList.iterrows():
            trial_start = food['trialstart']
            food_name = food['food']
            available = food['available']
            if food_name == ref:
                food_name = dummyfood
            start_cross = core.getTime() - start_time
            newCross(win, wait_time=trial_start - start_cross)
            c_image_onset = core.getTime() - start_time
            key = showImage(win, food_name, 4.0, constants.C_RATING, zoom=0.5, pos=(0.35, 0.2), ref_image=ref)
            if key is None:
                tooLate = newText(win, "tooLate", "Too late!")
                tooLate.draw()
                win.flip()
                core.wait(1.0)
                key = [['0'], None]
            # save to the csv file after each trial
            temp_list = (ref_food, key[0][0], key[1], c_image_onset)
            if food_name == dummyfood:
                temp_index = output_df[output_df['food_item'] == ref_food].index
            else:
                temp_index = output_df[output_df['food_item'] == get_food_name(food_name)].index
            output_df.loc[temp_index, ['ref_food', 'choice_rating', 'c_rt', 'cimage_onset']] = temp_list
            output_df.to_csv(f"{save_all}.csv", index=False) if existed_file is None else output_df.to_csv(existed_file, index=False)
            # get snack output
            if counter < 5 and available == 1 and food_name is not dummyfood:
                if temp_list[1] < '3' and temp_list[1] > '0':
                    snack_list.append([get_food_name(food_name), ref_food])
                    counter += 1
                elif temp_list[1] > '3':
                    snack_list.append([get_food_name(food_name), get_food_name(food_name)])
                    counter += 1
        end_of_block = newText(win, "end_of_block", constants.C_THANKYOU)
        end_of_block.draw()
        win.flip()
        newKey(keyList=['space'])

        # output the file for snack choosing
        with open(f"{save_choice_output}.txt", 'w') as f:
            for snack in snack_list:
                f.write(f"When choosing between [{ref_food}] and [{snack[0]}], you chose [{snack[1]}].\n")
            f.write(f"Reference Food: {ref_food}")

    ######################### Choosing Test Block(s) ########################
    ref_food = "ref_food"
    # run all test blocks
    if test_block == "all":
        # create an output file
        for _, food in hList.iterrows():
            new_row = {
                'food_item': get_food_name(food['food']),
                'fat': food['fat'],
                'available': food['available'],
                'hilo': food['hilo'],
                'SubID': expInfo['participant'],
                'time point': time_pt,
                'admit_number':admit_pt,
                'date': expInfo['date'][0:10],
                'condition': condition,
                'rating_reversed': rating_reversed
            }
            output.append(new_row)
        output_df = pd.DataFrame(output, columns=columns)
        output_df.to_csv(f"{save_all}.csv", index=False)
        # if health rating goes first -> h_first = True
        for i, row in order.iterrows():
            h_or_t = order.loc[i, "label"][0]
            get_rating(row, h_or_t, None)
        ref, ref_food = get_ref_food()
        get_choice(ref, ref_food, None)
    # only run health or taste block
    # the new _all.csv file will overwrite the original _all.csv file
    elif test_block == "health" or test_block == "taste":
        if read_file() is None:
            # create an output file
            for _, food in hList.iterrows():
                new_row = {
                    'food_item': get_food_name(food['food']),
                    'fat': food['fat'],
                    'available': food['available'],
                    'hilo': food['hilo'],
                    'SubID': expInfo['participant'],
                    'time point': time_pt,
                     'admit_number':admit_pt,
                    'date': expInfo['date'][0:10],
                    'condition': condition,
                    'rating_reversed': rating_reversed
                }
                output.append(new_row)
            output_df = pd.DataFrame(output, columns=columns)
            output_df.to_csv(f"{save_all}.csv", index=False)
            existed_file, output_df = read_file()
        else:
            existed_file, output_df = read_file()
        h_or_t = "h" if test_block == "health" else "t"
        for i, row in order.iterrows():
            if order.loc[i, "label"][0] == h_or_t:
                get_rating(row, h_or_t, existed_file)
    # only run choice block
    # the new _all.csv file will overwrite the original _all.csv file
    elif test_block == "choice":
        if read_file() is None:
            # create an output file
            for _, food in hList.iterrows():
                new_row = {
                    'food_item': get_food_name(food['food']),
                    'fat': food['fat'],
                    'available': food['available'],
                    'hilo': food['hilo'],
                    'SubID': expInfo['participant'],
                    'time point': time_pt,
                     'admit_number':admit_pt,
                    'date': expInfo['date'][0:10],
                    'condition': condition,
                    'rating_reversed': rating_reversed
                }
                output.append(new_row)
            output_df = pd.DataFrame(output, columns=columns)
            output_df.to_csv(f"{save_all}.csv", index=False)
            existed_file, output_df = read_file()
        else:
            existed_file, output_df = read_file()
        ref, ref_food = get_ref_food()
        get_choice(ref, ref_food, existed_file)

    ########################## Saving Logging Files #########################
    if test_block == "all" or test_block == "health":
        hList['food'] = hList['food'].apply(get_food_name)
        oList = read_file()[1]
        hmerged = hList.merge(oList, left_on="food", right_on="food_item")
        health = hmerged[
            ["Unnamed: 0", "fat_x", "himage_onset", "h_rt", "health_recorded_response", "available_x", "food"]].copy()
        health.columns = ["t", "fat", "trialonset", "rt", "resp", "available", "food"]
        health["t"] = health["t"] + 1
        health.to_csv(f"{save_health}.csv", index=False)

    if test_block == "all" or test_block == "taste":
        tList['food'] = tList['food'].apply(get_food_name)
        oList = read_file()[1]
        tmerged = tList.merge(oList, left_on="food", right_on="food_item")
        taste = tmerged[
            ["Unnamed: 0", "fat_x", "timage_onset", "t_rt", "taste_recorded_response", "available_x", "food"]].copy()
        taste.columns = ["t", "fat", "trialonset", "rt", "resp", "available", "food"]
        taste["t"] = taste["t"] + 1
        taste.to_csv(f"{save_taste}.csv", index=False)

    if test_block == "all" or test_block == "choice":
        cList['food'] = cList['food'].apply(get_food_name)
        oList = read_file()[1]
        cmerged = cList.merge(oList, left_on="food", right_on="food_item", how="outer")
        choice = cmerged[
            ["Unnamed: 0", "fat_y", "cimage_onset", "c_rt", "choice_rating", "available_y", "food_item"]].copy()
        choice.columns = ["t", "fat", "trialonset", "rt", "resp", "available", "food"]
        choice["t"] = choice["t"] + 1
        # fill in dummy food and remove the availability for dummy food
        dummy_loc = choice[choice["food"] == ref_food].index[0]
        choice.loc[dummy_loc, "food"] = get_food_name(constants.DUMMYFOOD)
        choice.loc[dummy_loc, "available"] = ''
        choice.to_csv(f"{save_choice}.csv", index=False)

    if test_block == "all":
        with open(f"{save_foodtask}.log", "w") as f:
            print("this is health\n" + health.to_string(index=False) +
                  "\nthis is taste\n" + taste.to_string(index=False) +
                  "\nthis is choice\n" + choice.to_string(index=False), file=f)
    elif test_block == "health":
        with open(f"{save_foodtask}.log", "w") as f:
            print("this is health\n" + health.to_string(index=False), file=f)
    elif test_block == "taste":
        with open(f"{save_foodtask}.log", "w") as f:
            print("this is taste\n" + taste.to_string(index=False), file=f)
    elif test_block == "choice":
        with open(f"{save_foodtask}.log", "w") as f:
            print("this is choice\n" + choice.to_string(index=False), file=f)

    win.close()
    core.quit()
