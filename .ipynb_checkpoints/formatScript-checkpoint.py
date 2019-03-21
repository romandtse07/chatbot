#needs refactor to be way shorter and more readable
import re
import numpy as np

def makeDialogue(script_text):
    num_breaks_regex = getNormalLineBreaks(script_text)
    script1 = re.sub('([A-Z]+\)*)\n', '\\1:\n', script_text)
    script1 = re.sub(num_breaks_regex, '#', script1)#.replace('  ', ' ')
    #replaces those stage direction aside stuffs
    script1 = re.sub('\([a-z].*\)', '', script1).split('\n')
    #not sure this is actually important try pulling the first line another way
    script_split = [lineType(line) for line in script1]
    
    dialogues = []
    dialogue = []
    current_type = 'none'
    current_speaker = 'none'
    first_spoken_line = np.where([line=='@speak' for line in script_split])[0][0]

    for line in script1[first_spoken_line:]:
        previous_type = current_type
        current_type = lineType(line)

        if previous_type == '@setting' and current_type == '@scene' and dialogue:
            dialogues.append(dialogue)
            dialogue = []
            current_speaker = 'none'

        #at some point u should refactor so that u take care of (cont.) and justify the existence of the if statement
        #also take out the check try except
        if current_type == '@speak':
            try:
                name_break = line.index(':#')
                previous_speaker = current_speaker
                current_speaker = line[:name_break]
                current_line = line[name_break+2:]
                if previous_speaker in current_speaker:
                    dialogue[-1] = dialogue[-1] + ' ' + current_line
                else:
                    dialogue.append(current_line)
            except:
                #print(line)
                pass
    
    interactions = []
    for dialogue in dialogues:
        if len(dialogue) > 1:
            interactions.extend([(prompt.replace('#', ' '), response.replace('#', ' ')) for prompt, response in zip(dialogue[:-1], dialogue[1:])])
    interactions = [(getWords(prompt), getWords(response)) for prompt, response in interactions]
    
    return interactions

def lineType(line):
    if re.search('^[^a-z]*:[^a-z]*$', line):
        return '@setting'
    if re.match('^[A-Z.,\'\ ]+:', line):
        return '@speak'
    else:
        return '@scene'

def getNormalLineBreaks(script_text):
    current_lines = len(re.findall('(?<=[^\n])\n{1}(?=[^\n])', script_text))
    #this will work for the small sample i've seen but maybe consider changing break condition
    for lines_for_break in range(1, 10) :
        expression = r'(?<=[^\n])\n{' + str(lines_for_break+1) + r'}(?=[^\n])'
        next_lines = len(re.findall(expression, script_text))
        if (current_lines - next_lines) > 200 and current_lines > 1000 and next_lines > 1000:
            regex_return = '(?<=[^\n])\n{' + str(lines_for_break) + '}'
            return regex_return
        current_lines = next_lines
    raise RuntimeError('Could not find difference between dialogue line breaks')
            
def getWords(line):
    result = re.sub('[^a-z^A-Z\s]', '', line).lower()
    result = re.sub('\s+', ' ', result)
    result = result[:-1].split() # all of these end in new line, this gets rid of the last space
    return ['BOS'] + result + ['EOS']