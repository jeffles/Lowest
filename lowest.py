import json
import math
import os.path
import random
import time

from collections import defaultdict
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from pprint import pprint

# TODO - Slack interface for playing? (A- no, needs security approval)
# TODO - manual entry of people
# TODO - sort name displays

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/presentations']

PRESENTATION_ID = '1MUn3S6r8RowPUWJXot3V2JIZ9xUFOAyLEFdmfXfgWl8'

TABLE_ID = ''

OATH_SERVICE = ''


def make_charts():
    pass
    # def is_prime(n):
    #     for i in range(2, n):
    #         if (n % i) == 0:
    #             return False
    #     return True
    # odd = 0
    # even = 0
    # divisible = defaultdict(int)
    # for num in guesses:
    #     for i in range(2, num):
    #         if (num % i) == 0 and is_prime(i):
    #             divisible[i] += len(guesses[num])
    #             break
    #     if is_prime(num):
    #         if num == 2:
    #             eprime += len(guesses[num])
    #         else:
    #             prime += len(guesses[num])
    # import matplotlib.pyplot as plt
    # labels = 'Odd Non Prime guesses', 'Odd Prime Guesses', 'Even Prime Guesses (2)', 'Even Non Prime Guesses'
    # sizes = [odd, prime, eprime, even]
    # fig1, ax1 = plt.subplots()
    # ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
    #         shadow=True, startangle=90)
    # ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    # plt.show()
    #
    # plt.bar(range(len(divisible)), list(divisible.values()), align='center')
    # plt.xticks(range(len(divisible)), list(divisible.keys()))
    # plt.show()


def print_guesses(participant_guesses, winning_number):
    remaining = defaultdict(list)

    for participant in sorted(participant_guesses):
        left = 0
        for guess in participant_guesses[participant]:

            if guess > winning_number:
                left += 1

        remaining[left].append(participant)

    print('5 guesses left:', remaining[5])
    print('4 guesses left:', remaining[4])
    print('3 guesses left:', remaining[3])
    print('2 guesses left:', remaining[2])
    print('1 guesses left:', remaining[1])
    print('0 guesses left:', remaining[0])


def slide_setup():
    """Shows basic usage of the Slides API.
    Prints the number of slides and elements in a sample presentation.
    """
    global TABLE_ID
    global OATH_SERVICE
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        OATH_SERVICE = build('slides', 'v1', credentials=creds)
        presentation = OATH_SERVICE.presentations().get(
            presentationId=PRESENTATION_ID).execute()
        slide = presentation.get('slides')[2]
        TABLE_ID = slide.get('pageElements')[0].get('objectId')
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error


def delete_cell_json(row, col):
    return {'deleteText':
                {"objectId": TABLE_ID, "cellLocation": {"rowIndex": row, "columnIndex": col},
                 "textRange": {"type": "ALL"}}}


def insert_cell_json(row, col, text):
    return {'insertText': {"objectId": TABLE_ID, "cellLocation": {"rowIndex": row, "columnIndex": col}, "text": text,
                           "insertionIndex": 0}}


def determine_color(num_picks):
    # return 1, 1, 1
    if num_picks > 1:
        return 1, 0.1, 0.1
    elif num_picks == 0:
        return .4, .4, .4
    else:
        return 1, 1, 0


def update_color_json(row, col, color):
    return {
            "updateTableCellProperties": {
                "objectId": TABLE_ID,
                "tableRange": {
                    "location": {
                        "rowIndex": row,
                        "columnIndex": col
                    },
                    "rowSpan": 1,
                    "columnSpan": 1
                },
                "tableCellProperties": {
                    "tableCellBackgroundFill": {
                        "solidFill": {
                            "color": {
                                "rgbColor": {
                                    "red": color[0],
                                    "green": color[1],
                                    "blue": color[2]
                                }
                            }
                        }
                    }
                },
                "fields": "tableCellBackgroundFill.solidFill.color"
            }
        }


def get_who_string(who_picked, max_length):
    who_str = ''
    if len(who_picked) == 0:
        return 'Noone'
    who_picked.sort()
    who_str = ', '.join(who_picked)
    if len(who_str) > max_length:
        who_str = ''
        for person in who_picked:
            who_str += person.split()[0] + ', '
        who_str = who_str[:-2]
    if len(who_str) > max_length:
        wp_initials = []
        for w in who_picked:
            wp_initials.append(w.split()[0][0] + w.split()[1][0])
        wp_initials.sort()
        who_str = ', '.join(wp_initials)
#        who_str = who_str[:-1]

    # if len(who_str) > max_length:
    #     who_str = who_str[:max_length-3] + '...'
    return who_str


def get_remaining(participant_guesses, remaining_guesses):
    remaining = defaultdict(list)

    for participant in sorted(participant_guesses):
        left = 0
        for guess in participant_guesses[participant]:
            if guess in remaining_guesses:
                left += 1
        if left > 5:
            left = 5
        remaining[left].append(participant)

    remaining_strings = defaultdict(str)
    remaining_strings[0] = get_who_string(remaining[0], 90)
    remaining_strings[1] = get_who_string(remaining[1], 90)
    remaining_strings[2] = get_who_string(remaining[2], 90)
    remaining_strings[3] = get_who_string(remaining[3], 90)
    remaining_strings[4] = get_who_string(remaining[4], 90)
    remaining_strings[5] = get_who_string(remaining[5], 90)
    return remaining_strings

def eliminate_squares(bigger, guesses):
    requests = []
    if len(bigger) == 0:
        return
    for pick in bigger:
        col_index = (pick % 10) + 1
        row_index = math.floor(pick / 10) + 2
        num_picks = len(guesses[pick])

        requests.append(delete_cell_json(row_index, col_index))
        requests.append(insert_cell_json(row_index, col_index, str(num_picks)))
        requests.append(update_color_json(row_index, col_index, determine_color(num_picks)))

    body = {
        'requests': requests
    }

    try:
        response = OATH_SERVICE.presentations().batchUpdate(
            presentationId=PRESENTATION_ID, body=body).execute()
    except HttpError as error:
        print(f"An error occurred: {error}")
        time.sleep(62)
        response = OATH_SERVICE.presentations().batchUpdate(
            presentationId=PRESENTATION_ID, body=body).execute()



def reset_slides(participants):
    participants_str = get_who_string(participants, 90)

    requests = [
        delete_cell_json(0, 13),
        insert_cell_json(0, 13, '-'),
        # who picked
        delete_cell_json(1, 13),
        insert_cell_json(1, 13, 'Noone'),
        # Remaining guesses
        delete_cell_json(2, 13),
        insert_cell_json(2, 13, participants_str),
        delete_cell_json(4, 13),
        insert_cell_json(4, 13, 'Noone'),
        delete_cell_json(6, 13),
        insert_cell_json(6, 13, 'Noone'),
        delete_cell_json(8, 13),
        insert_cell_json(8, 13, 'Noone'),
        delete_cell_json(10, 13),
        insert_cell_json(10, 13, 'Noone'),
        delete_cell_json(12, 13),
        insert_cell_json(12, 13, 'Noone'),
        # Winner
        delete_cell_json(0, 0),
        insert_cell_json(0, 0, 'WELCOME TO LOWEST UNIQUE NUMBER!'),
    ]
    for col_index in range(1, 11):
        for row_index in range(2, 14):
            requests.append(delete_cell_json(row_index, col_index))
            requests.append(insert_cell_json(row_index, col_index, '?'))
            requests.append(update_color_json(row_index, col_index, (1, 1, 1)))
    requests.append(update_color_json(2, 1, (0, 0, 0)))
    body = {
        'requests': requests
    }
    try:
        response = OATH_SERVICE.presentations().batchUpdate(
            presentationId=PRESENTATION_ID, body=body).execute()
    except HttpError as error:
        print(f"An error occurred: {error}")
        time.sleep(62)
        response = OATH_SERVICE.presentations().batchUpdate(
            presentationId=PRESENTATION_ID, body=body).execute()


def set_square(pick, num_picks, who_picked, remaining_participant_strings, winner):
    col_index = (pick % 10) + 1
    row_index = math.floor(pick / 10) + 2


    requests = [
        delete_cell_json(row_index, col_index),
        insert_cell_json(row_index, col_index, str(num_picks)),
        update_color_json(row_index, col_index, determine_color(num_picks)),
        # Current Guess
        delete_cell_json(0, 13),
        insert_cell_json(0, 13, 'Current Guess: ' + str(pick)),
        # who picked
        delete_cell_json(1, 13),
        insert_cell_json(1, 13, get_who_string(who_picked, 30)),
        # Remaining guesses
        delete_cell_json(2, 13),
        insert_cell_json(2, 13, remaining_participant_strings[5]),
        delete_cell_json(4, 13),
        insert_cell_json(4, 13, remaining_participant_strings[4]),
        delete_cell_json(6, 13),
        insert_cell_json(6, 13, remaining_participant_strings[3]),
        delete_cell_json(8, 13),
        insert_cell_json(8, 13, remaining_participant_strings[2]),
        delete_cell_json(10, 13),
        insert_cell_json(10, 13, remaining_participant_strings[1]),
        delete_cell_json(12, 13),
        insert_cell_json(12, 13, remaining_participant_strings[0]),
        #Winner
        delete_cell_json(0, 0),
        insert_cell_json(0, 0, 'Current Winner: ' + winner),
    ]
    body = {
        'requests': requests
    }
    try:
        response = OATH_SERVICE.presentations().batchUpdate(
            presentationId=PRESENTATION_ID, body=body).execute()
    except HttpError as error:
        print(f"An error occurred: {error}")
        time.sleep(62)
        response = OATH_SERVICE.presentations().batchUpdate(
            presentationId=PRESENTATION_ID, body=body).execute()


def main():
    slide_setup()

    guesses = defaultdict(list)
    participant_guesses = defaultdict(list)
    top_range = 90



    def set_guesses(participant, nums):
        for n in nums:
            guesses[n].append(participant)
            participant_guesses[participant].append(n)

    participants = ['Calvin Wang', 'David Altuve', 'Lauren Davis', 'Chris Reynolds', 'George Guo', 'Justin Elms',
                    'Keith Loy', 'Newell Rose', 'Omar Mujahid', 'Rob Battaglia', 'Shuaiyuan Zhou', 'Stephen Kattner',
                    'Amr Alaas', 'Brian Alexander', 'Natalie Rees', 'Stacy Chen', 'Tonaz Perez Valadez', 'Janie Clarke',
                    'Jeff Sumner', 'Jim Sigler', 'Tim Zenchenko', 'Andrew Vinas', 'Olivia Griffin', 'Sarah Johnson',
                    'Steven Boydston', 'Stewart Sumner', 'Juliet Sumner', 'Sarah Sumner']
    for guest in participants:
        set_guesses(guest, random.sample(range(1, top_range), 5))
    print(participant_guesses['Stewart Sumner'])
    # set_guesses('Calvin Wang', [17, 19, 23, 29, 31])
    # set_guesses('David Altuve', [1, 9, 15, 21, 49])
    # set_guesses('Lauren Davis', [11, 13, 17, 53, 97])
    # set_guesses('Chris Reynolds', [1, 2, 3, 4, 5])
    # set_guesses('George Guo', [1, 2, 3, 4, 5])
    # set_guesses('Justin Elms', [7, 9, 11, 13, 15])
    # set_guesses('Keith Loy', [3, 6, 7, 8, 9])
    # set_guesses('Newell Rose', [16, 20, 25, 30, 36])
    #
    # set_guesses('Omar Mujahid', [3, 9, 17, 22, 101])
    # set_guesses('Rob Battaglia', [5, 8, 11, 13, 14])
    # set_guesses('Shuaiyuan Zhou', [1, 7, 11, 29, 38])
    # set_guesses('Stephen Kattner', [1, 16, 17, 18, 19])
    # set_guesses('Amr Alaas', [11, 17, 23, 29, 31])
    # set_guesses('Brian Alexander', [1, 17, 23, 33, 43])
    # set_guesses('Natalie Rees', [13, 14, 21, 33])
    # # set_guesses('Stacy Chen', random.sample(range(1, top_range), 5))
    # set_guesses('Stacy Chen', [13, 68, 101, 237, 1229])
    # set_guesses('Tonaz Perez Valadez', [10, 15, 16, 17, 18])
    # set_guesses('Janie Clarke', [8, 13, 24, 89, 112])
    # set_guesses('Jeff Sumner', [10, 15, 20, 23, 25])
    # set_guesses('Jim Sigler', [1, 5, 7, 11, 13])
    # set_guesses('Tim Zenchenko', [7, 11, 17, 23, 24])
    # set_guesses('Andrew Vinas', [3, 132, 163, 179, 114])
    # set_guesses('Olivia Griffin', [4, 11, 13, 17, 27])
    # set_guesses('Sarah Johnson', [8, 14, 19, 22, 31])
    # set_guesses('Steven Boydston', [1, 3, 7, 8, 9])
    # set_guesses('Ignacio Martelli', [1, 3, 7, 12, 14])
    # set_guesses('Marcos Mezzabotta', [5, 14, 18, 29, 53])
    # set_guesses('Ruzana Nekhay', [11, 13, 17, 19, 23])
    # set_guesses('Maxwell Rose', [6, 12, 14, 18, 28])

    conflicts = defaultdict(int)
    for num in guesses:
        conflicts[len(guesses[num])] += 1

    reset_slides(participants)
    remaining_guesses = list(range(1, 120))
    winner = 'Noone'
    while len(remaining_guesses) > 0:
        print("Pick a number - enter for random pick>")
        my_pick = input()
        if my_pick == '':
            pick = remaining_guesses.pop(random.randrange(len(remaining_guesses)))
            print(f'I picked {pick} for you.')
        else:
            pick = int(my_pick)
            if pick not in remaining_guesses:
                print('Not a valid pick. Try again')
            else:
                remaining_guesses.remove(pick)

        if len(guesses[pick]) == 1:
            winner = guesses[pick][0] + " with guess of " + str(pick)
            bigger = [x for x in remaining_guesses if x > pick]
            remaining_guesses = [x for x in remaining_guesses if x < pick]
            eliminate_squares(bigger, guesses)

        remaining_participants_strings = get_remaining(participant_guesses, remaining_guesses)
        set_square(pick, len(guesses[pick]), guesses[pick], remaining_participants_strings, winner)
    exit()

    print("Guesses")
    pprint(guesses)


    winning_number = 1
    while not winner:
        print(f'Guessers for {winning_number}')
        print(guesses[winning_number])
        print('Remaining tries')
        print_guesses(participant_guesses, winning_number)
        input()
        if len(guesses[winning_number]) == 1:
            pass
            # winner = guesses[winning_number][0]
            # break
        if winning_number > top_range:
            winner = 'NOONE'
            break
        winning_number += 1

    print(f"Give {winner} a prize for guessing: {winning_number}")




if __name__ == '__main__':
    main()
