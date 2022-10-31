import os
import subprocess

def create_protocol(trial, PATH_SCRIPT, PATH_OUT):

    # parameter definition
    # body
    body_red   = trial.suggest_int("body_red",   0, 150)
    body_green = trial.suggest_int("body_green", 0, 150 - body_red)
    body_blue_vol = 150 - body_red - body_green
    body_blue  = trial.suggest_int("body_blue", body_blue_vol, body_blue_vol)

    # mouth
    #mouth_red   = trial.suggest_int("mouth_red",   0, 150)
    #mouth_green = trial.suggest_int("mouth_green", 0, 150 - mouth_red)
    #mouth_blue_vol = 150 - mouth_red - mouth_green
    #mouth_blue  = trial.suggest_int("mouth_blue", mouth_blue_vol, mouth_blue_vol)

    # eye
    #eye_red   = trial.suggest_int("eye_red",   0, 150)
    #eye_green = trial.suggest_int("eye_green", 0, 150 - eye_red)
    #eye_blue_vol = 150 - eye_red - eye_green
    #eye_blue  = trial.suggest_int("eye_blue", eye_blue_vol, eye_blue_vol)


    # execute create_protocol.py
    #command  = ['python', f'{PATH_SCRIPT}/create_protocol.py', f'{trial.number}', PATH_OUT, f'{body_red}', f'{body_green}', f'{body_blue}',f'{mouth_red}', f'{mouth_green}', f'{mouth_blue}',f'{eye_red}', f'{eye_green}', f'{eye_blue}',]
    command  = ['python', f'{PATH_SCRIPT}/create_protocol.py', f'{trial.number}', PATH_OUT, f'{body_red}', f'{body_green}', f'{body_blue}']
    subprocess.run(command)


def evaluate(trial, PATH_SCRIPT, PATH_OUT):
    command  = ['python', f'{PATH_SCRIPT}/evaluate.py', f'{trial.number}', PATH_SCRIPT, PATH_OUT]
    score    = subprocess.check_output(command)
    return score