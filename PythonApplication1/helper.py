#helper.py
#part of the PwndMondersBotClient program
#maily use to help interface between the bot and the text files
import os
import datetime
from dictionaries import ign_d
from dictionaries import d_ign
b_file = 'balances.txt'
l_file = 'changelog.txt'

#function to add points to a user
#ctx context object
#user is discord user tag '<@346523452345>'
#points is int points to be added (neg for subtract)
def add_points(ctx, user, points):
    if points == 0:
        return(f'Did not add or modify any points. Point value 0.')
    name = grab_user_name(ctx, user)
    if name == '-1':
        return(f'Could not locate username {user} in the guild. Nothing changed.')
    #check to see if user exists
    if user_exist(name):
        old_points=0
        with open(b_file,'r') as file:
            lines = file.readlines() # read in file lines
        newLines=[]
        for l in lines:
            if name in l:
                x = l.split(',')
                old_points = float(x[1])
                new_points = old_points+points
                newLines.append(f'{name},{new_points}\n') #overwrite correct line with new point value
            else:
                newLines.append(l)
        with open(b_file,'w') as file:
            file.writelines(newLines) #rewrite the new values and old values to file
        return (log(f'Successfully added {points} to {name}. Old value {old_points}, new value {new_points}'))
    else:
        #add user and points to end of the file
        with open(b_file,'a') as file:
            file.write(f'{name},{points}\n')
        return (log(f'Successfully added new user {name} with initial point value {points}'))
    return (log(f'Failed to add points. Should not get here. {user} {points}'))

# returns the entire balances.txt file as a string
def display_points_all():
    output = ''
    with open(b_file,'r') as f:
        for line in f.readlines():
            name = line.replace('\n','').split(',')[0]
            point = line.replace('\n','').split(',')[1]
            ign = swap_discord_name_for_ign(name)
            output = output + (f'{ign} has {point} points.\n')
        return output

# returns a specific users points value
def display_points(ctx, user):
    name = grab_user_name(ctx, user)
    with open(b_file) as f:
         for line in f.readlines():
             if name in line:
                 ign = swap_discord_name_for_ign(name)
                 point = line.replace('\n','').split(',')[1]
                 return f'{ign} has {point} points.'
    return (f'Could not find {name} in the balances file.')

#display lines number of lines from the change log
def display_log(lines):
    if lines < 100:
        with open(l_file) as f:
            last_lines = f.read().splitlines()[-lines:]
            return '\n'.join(last_lines)
    else:
        return (f'Too many lines requested. Must be under 100.')

#display lines number of lines from the change log, only for specified user
def display_log_user(ctx, user, lines):
    name = grab_user_name(ctx, user)
    if name == '-1':
        return(f'Could not locate username {user} in the guild. Nothing changed.')
    
    output = []
    if lines < 100:
        with open(l_file) as f:
            flines = f.read().splitlines()
            flines.reverse()
            for l in flines:
                if name in l:
                    output.append(l)
                    lines = lines -1
                    if lines == 0:
                        output.reverse()
                        return '\n'.join(output) #once we hit requested number of lines, return
            output.reverse()
            return '\n'.join(output)#if we get to the end, return with what we have
    else:
        return (f'Too many lines requested. Must be under 100.')

#helper function to record to log file and return same string recorded to output
def log(msg):
    now = datetime.datetime.now()
    with open(l_file, 'a') as f:
        f.write(f'{now}, {msg}\n')
    return msg


#helper function to check and see if a user exists in the Balances file
#user is user NAME not the discord tag number
def user_exist(user):
    with open(b_file) as f:
        if user in f.read():
            return True # found the name, it exists
    return False # name does not exist

#helper function to grab the user's NAME from the context using the discord tag
def grab_user_name(ctx, user):
    for m in ctx.guild.members:
        if str(m.id) in user:
            return m.name
    return '-1'

#helper function to switch from the discord name to the in game name
#if it cannot find the name in the dictionary, just returns the discord name back
def swap_discord_name_for_ign(discord_name):
    ign = d_ign[discord_name]
    if ign ==  '':
        ign = discord_name #if we cant find in game name, replace with name
    return ign

#helper function to switch from the in game name to the discord PING name 
#if it cannot find the name in the dictionary, does nothing
def swap_ign_for_discord_ping(ign):
    ping = ign_d[ign]
    if ping ==  '':
        ping = ign #if we cant find it, do nothing
    return ping