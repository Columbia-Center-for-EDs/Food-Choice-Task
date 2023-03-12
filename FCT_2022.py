### Food Choice Task Matlab Version(2016) by Dr. Karin Foerde and Dr. Joanna Steinglass
### Food Choice Python version is created on Sep 3rd, 2022
### by Serena J. Gu (RA at Columbia Center for Eating Disorders)
from fct_library import *

def run():
    import os
    import re
    from psychopy import visual, core, data, logging, gui
    import numpy as np
    import pandas as pd
    import constants

    _thisDir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(_thisDir)

    #########################Experiment Imformation########################

    expName = 'FCT_2022'  # from the Builder filename that created this script
    expInfo = {'participant': ''
        , 'order': ['Condition_1_HT', 'Condition_1_TH', 'Condition_2_HT', 'Condition_2_TH']
        , 'h_list': ['Test', 'Test1', 'Test2', 'foodlist1','foodlist2','foodlist3','foodlist4','foodlist5', 'foodlist6']
        , 't_list': ['Test', 'Test1', 'Test2', 'foodlist1','foodlist2','foodlist3','foodlist4','foodlist5', 'foodlist6']
        , 'c_list': ['Test', 'Test1', 'Test2', 'foodlist1','foodlist2','foodlist3','foodlist4','foodlist5', 'foodlist6']}
    #, 'foodlist': ['Test', 'foodlist1','foodlist2','foodlist3','foodlist4','foodlist5', 'foodlist6']
    dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
    if dlg.OK == False:
        core.quit()  # user pressed cancel
    expInfo['date'] = data.getDateStr()  # add a simple timestamp
    expInfo['expName'] = expName
    #print(f"#################################{expInfo}")

    #########################Saving Data File Info########################

    save_filename = f"{_thisDir}/data/{expInfo['participant']}_{expInfo['date']}_behav"
    save_output = f"{_thisDir}/data/{expInfo['participant']}_{expInfo['date']}_choiceoutput"

    logFile = logging.LogFile(save_filename+'.log', level=logging.DEBUG)
    logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

    #########################Experiment Start########################
    win = visual.Window([1470,956],fullscr=True, winType='pyglet',
        monitor="testMonitor", units="height", color="#000000", colorSpace='hex',
        blendMode="avg")
    win.mouseVisible = False

    welcome_text = newText(win, "welcome_text", "Welcome!")
    welcome_text.draw()
    win.flip()
    newKey()

    order = f"{_thisDir}/order/{expInfo['order']}.xlsx"
    #foodlist = f"{_thisDir}/lists/{expInfo['foodlist']}.csv"
    h_list = f"{_thisDir}/lists/{expInfo['h_list']}.csv"
    t_list = f"{_thisDir}/lists/{expInfo['t_list']}.csv"
    c_list = f"{_thisDir}/lists/{expInfo['c_list']}.csv"
    #foodList = pd.read_csv(foodlist)
    hList = pd.read_csv(h_list)
    tList = pd.read_csv(t_list)
    cList = pd.read_csv(c_list)
    df = pd.read_excel(order)
    food_dict = {}

    #########################Getting Health and Taste Ratings########################
    for i, row in df.iterrows():
        newInstruction(win, "inst1", row, keyList=['space'])
        newInstruction(win, "inst2", row, keyList=['space'])
        newInstruction(win, "inst3", row, keyList=['space'])
        foodList = hList if row['label'][0] == 'h' else tList
        start_time = core.getTime()
        for index, food in foodList.iterrows():
            food_name = food['food']
            trial_start = food['trialstart']
            if i == 0:
                food_dict[food_name] = []
            start_cross = core.getTime() - start_time
            newCross(win, wait_time=trial_start-start_cross)
            ht_image_onset = core.getTime() - start_time
            key = showImage(win, food_name, 4.0, row['rating'], zoom=0.5)
            if key is None:
                tooLate = newText(win, "tooLate", "Too late!")
                tooLate.draw()
                win.flip()
                core.wait(1.0)
                key = [['0'], None]
            food_dict[food_name].append((key[0][0], key[1], ht_image_onset))
        end_of_block = newText(win, "end_of_block", """End of Block

    Press ‘space’ to continue.""")
        end_of_block.draw()
        win.flip()
        newKey(keyList=['space'])

    #########################Getting Reference Item########################
    ref_backup = constants.REF_BACKUP
    def find_ref(a, b):
        return [food for food, ((h, _, _), (t, _, _)) in food_dict.items()
                if (h == a and t == b) or (h == b and t == a)]

    #results = [find_ref('3', x) for x in ['3', '4', '2']]
    #ref = next((x for x in results if x), ref_backup)

    ref = find_ref('3', '3')
    if not ref:
        ref = find_ref('3', '4')
    if not ref:
        ref = find_ref('3', '2')
    if not ref:
        ref = ref_backup

    def get_food_name(food):
        return ' '.join(re.findall(r'/([\w .\& .\%]+).jpg', food))

    ref = ref[0]
    #print(food_dict)
    ref_food = get_food_name(ref)
    #print(f"Reference Food: {ref_food}")

    #########################Getting Choice Ratings########################
    dummyfood = constants.DUMMYFOOD
    blueberry = constants.BLUEBERRY
    raspberry = constants.RASPBERRY

    ref_image = newImage(win, image=ref, zoom=0.5, pos=(0, -0.25))
    ref_text = newText(win, "ref_text", constants.REF_TEXT, pos=(0, 0.2))
    ref_image.draw()
    ref_text.draw()
    win.flip()
    newKey(keyList=['space'])

    row = { 'inst1': constants.C_INST1, 'inst2': constants.C_INST2 }
    #newInstruction(win, "inst1", row, keyList=['space'])
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

    #showImage(win, blueberry, keyList=['space'], constants.C_RATING, zoom = 0.5, pos=(-0.35, -0.2), ref_image=raspberry)
    newInstruction(win, "inst2", row, keyList=['space'])
    choice_dict = {}

    start_time = core.getTime()
    for _, food in cList.iterrows():
        trial_start = food['trialstart']
        food_name = food['food']
        avlist = food['available']
        if food_name == ref:
            food_name = dummyfood
            avlist = None
            choice_dict[food_name] = []
        start_cross = core.getTime() - start_time
        newCross(win, wait_time=trial_start-start_cross)
        c_image_onset = core.getTime() - start_time
        key = showImage(win, food_name, 4.0, constants.C_RATING, zoom = 0.5, pos=(0.35, 0.2), ref_image=ref)
        if key is None:
            tooLate = newText(win, "tooLate", "Too late!")
            tooLate.draw()
            win.flip()
            core.wait(1.0)
            key = [['0'], None]
        choice_dict[food_name] = (key[0][0], key[1], c_image_onset, avlist)
    end_of_block = newText(win, "end_of_block", constants.C_THANKYOU)
    end_of_block.draw()
    win.flip()
    newKey(keyList=['space'])
    #print(choice_dict)

    #########################Saving Data Files########################
    counter = 0
    with open(f"{save_output}.txt" , 'w') as f:
        for food, (choice, _, _, available) in choice_dict.items():
            if choice < '3' and available == 1:
                f.write(f"When choosing between [{ref_food}] and [{get_food_name(food)}], you chose [{ref_food}].\n")
                counter += 1
            if choice > '3' and available == 1:
                f.write(f"When choosing between [{ref_food}] and [{get_food_name(food)}], you chose [{get_food_name(food)}].\n")
                counter += 1
            if counter == 5:
                break

    columns = ['food_item', 'h_rating', 'h_rt', 't_rating', 't_rt', 'c_rating', 'c_rt', 'available', 'fat', 'hilo']
    data = {}
    lookup_fat = {}

    for _, food in hList.iterrows():
        food_name = food['food']
        lookup_fat[food_name] = food

    htcfood = list(set(list(food_dict.keys())+list(choice_dict.keys())))
    for food in htcfood:
      ht = food_dict[food] if food in food_dict else [(None, None, None), (None, None, None)]
      c = choice_dict[food] if food in choice_dict else (None, None, None, None)
      htc = [*ht]
      htc = htc[0] + htc[1]
      extras = (lookup_fat[food]['available'], lookup_fat[food]['fat'], lookup_fat[food]['hilo']) if food in lookup_fat else ()
      data[get_food_name(food)] = htc + c[:-1] + extras

    columns = ['h_rating', 'h_rt', 'himage_onset', 't_rating', 't_rt', 'timage_onset', 'c_rating', 'c_rt', 'cimage_onset', 'available', 'fat', 'hilo']
    df = pd.DataFrame.from_dict(data, orient='index', columns =columns)
    df.index.name = 'food_item'

    df.to_csv(f"{save_filename}.csv")

    with open(f"{save_output}.txt" , 'a') as f:
        f.write(f"Reference Food: {ref_food}")

    ###########################Saving Logging Files####################
    hList['food'] = hList['food'].apply(get_food_name)
    tList['food'] = tList['food'].apply(get_food_name)
    cList['food'] = cList['food'].apply(get_food_name)
    oList = pd.read_csv(f"{save_filename}.csv")
    hmerged = hList.merge(oList, left_on="food", right_on="food_item")
    tmerged = tList.merge(oList, left_on="food", right_on="food_item")
    cmerged = cList.merge(oList, left_on="food", right_on="food_item", how="outer")
    cmerged.dropna(subset=["choice_rating"], inplace=True)

    health = hmerged[["Unnamed: 0", "fat_x", "himage_onset", "h_rt", "health_rating", "available_x", "food"]].copy()
    health.columns = ["t", "fat", "trialonset", "rt", "resp", "available", "food"]
    health["t"] = health["t"] + 1

    taste = tmerged[["Unnamed: 0", "fat_x", "timage_onset", "t_rt", "taste_rating", "available_x", "food"]].copy()
    taste.columns = ["t", "fat", "trialonset", "rt", "resp", "available", "food"]
    taste["t"] = taste["t"] + 1

    choice = cmerged[["Unnamed: 0", "fat_y", "cimage_onset", "c_rt", "choice_rating", "available_y", "food_item"]].copy()
    choice.columns = ["t", "fat", "trialonset", "rt", "resp", "available", "food"]
    choice["t"] = choice["t"] + 1

    health.to_csv(f"{save_health}.csv")
    taste.to_csv(f"{save_taste}.csv")
    choice.to_csv(f"{save_choice}.csv")

    with open(f"{save_foodtask}.log", "w") as f:
    print("this is health\n" + health.to_string(index=False) +
        "\nthis is taste\n" + health.to_string(index=False) +
        "\nthis is choice\n" + health.to_string(index=False), file=f)

    #cleanup
    win.close()
    core.quit()