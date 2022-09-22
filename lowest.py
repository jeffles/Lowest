from collections import defaultdict
from pprint import pprint
import random


import os.path

import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/presentations']

# The ID of a sample presentation.
PRESENTATION_ID = '1MUn3S6r8RowPUWJXot3V2JIZ9xUFOAyLEFdmfXfgWl8'


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

def print_guesses2(participant_guesses, winning_number):

    odd = True
    for participant in sorted(participant_guesses):
        print("{: >25}".format(participant), end=' ')
        #print("{: >20} {: >20} {: >20}".format(*row))
        for guess in participant_guesses[participant]:
            if guess > winning_number:
                print('X', end=' ')
            else:
                print('?', end=' ')
        if odd:
            print("\t\t", end='')
            odd = False
        else:
            odd = True
            print()


def slide_setup():
    """Shows basic usage of the Slides API.
    Prints the number of slides and elements in a sample presentation.
    """
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
        service = build('slides', 'v1', credentials=creds)
        presentation = service.presentations().get(
            presentationId=PRESENTATION_ID).execute()
        slide = presentation.get('slides')[0]
        table_id = slide.get('pageElements')[0].get('objectId')
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error

    return table_id, service


def main():
    table_id, service = slide_setup()

    participants = ['Calvin Wang', 'David Altuve', 'Lauren Davis', 'Chris Reynolds', 'George Guo', 'Justin Elms',
                    'Keith Loy', 'Newell Rose', 'Omar Mujahid', 'Rob Battaglia', 'Shuaiyuan Zhou', 'Stephen Kattner',
                    'Amr Alaas', 'Brian Alexander', 'Natalie Rees', 'Stacy Chen', 'Tonaz Perez Valadez', 'Janie Clarke',
                    'Jeff Sumner', 'Jim Sigler', 'Tim Zenchenko', 'Andrew Vinas', 'Olivia Griffin', 'Sarah Johnson',
                    'Steven Boydston']
    # Not invite to game  'Alexander Mazaykin', 'Chen Yang', 'Marat Chafigouline', 'Sarah Holt',
    # 'Kurtis White', 'Ada Song', 'James Hafner', 'Susan Le'
    #  'CJ Hong']
    guesses = defaultdict(list)
    participant_guesses = defaultdict(list)
    top_range = 100


    def set_guesses(participant, nums):
        for num in nums:
            guesses[num].append(participant)
            participant_guesses[participant].append(num)


    set_guesses('Calvin Wang', [17, 19, 23, 29, 31])
    set_guesses('David Altuve', [1, 9, 15, 21, 49])
    set_guesses('Lauren Davis', [11, 13, 17, 53, 97])
    set_guesses('Chris Reynolds', [1, 2, 3, 4, 5])
    set_guesses('George Guo', [1, 2, 3, 4, 5])
    set_guesses('Justin Elms', [7, 9, 11, 13, 15])
    set_guesses('Keith Loy', [3, 6, 7, 8, 9])
    set_guesses('Newell Rose', [16, 20, 25, 30, 36])
    set_guesses('Omar Mujahid', [3, 9, 17, 22, 101])
    set_guesses('Rob Battaglia', [5, 8, 11, 13, 14])
    set_guesses('Shuaiyuan Zhou', [1, 7, 11, 29, 38])
    set_guesses('Stephen Kattner', [1, 16, 17, 18, 19])
    set_guesses('Amr Alaas', [11, 17, 23, 29, 31])
    set_guesses('Brian Alexander', [1, 17, 23, 33, 43])
    set_guesses('Natalie Rees', [13, 14, 21, 33])
    # set_guesses('Stacy Chen', random.sample(range(1, top_range), 5))
    set_guesses('Stacy Chen', [13, 68, 101, 237, 1229])
    set_guesses('Tonaz Perez Valadez', [10, 15, 16, 17, 18])
    set_guesses('Janie Clarke', [8, 13, 24, 89, 112])
    set_guesses('Jeff Sumner', [10, 15, 20, 23, 25])
    set_guesses('Jim Sigler', [1, 5, 7, 11, 13])
    set_guesses('Tim Zenchenko', [7, 11, 17, 23, 24])
    set_guesses('Andrew Vinas', [3, 132, 163, 179, 114])
    set_guesses('Olivia Griffin', [4, 11, 13, 17, 27])
    set_guesses('Sarah Johnson', [8, 14, 19, 22, 31])
    set_guesses('Steven Boydston', [1, 3, 7, 8, 9])
    set_guesses('Ignacio Martelli', [1, 3, 7, 12, 14])
    set_guesses('Marcos Mezzabotta', [5, 14, 18, 29, 53])
    set_guesses('Ruzana Nekhay', [11, 13, 17, 19, 23])
    set_guesses('Maxwell Rose', [6, 12, 14, 18, 28])

    def is_prime(n):
      for i in range(2,n):
        if (n%i) == 0:
          return False
      return True
    odd = 0
    even = 0
    prime = 0
    eprime = 0
    total = 0
    divisible = defaultdict(int)
    conflicts = defaultdict(int)
    for num in guesses:
        print(num, len(guesses[num]))
        for i in range(2, num):
            # print(i, num)
            if (num % i) == 0 and is_prime(i):
                divisible[i] += len(guesses[num])
        total += len(guesses[num])
        conflicts[len(guesses[num])] += 1
        if is_prime(num):
            if num == 2:
                eprime += len(guesses[num])
            else:
                prime += len(guesses[num])
        elif (num % 2) == 0:
            even += len(guesses[num])
        else:
            odd += len(guesses[num])

    requests = [
        {
            'deleteText': {
                "objectId": table_id,
                "cellLocation": {
                    "rowIndex": 3,
                    "columnIndex": 3
                },
                "textRange": {
                    "type": "ALL",
                }
            }
        },
        {
            'insertText': {
                "objectId": table_id,
                "cellLocation": {
                    "rowIndex": 3,
                    "columnIndex": 3
                },
                "text": 'different',
                "insertionIndex": 0
            }
        }
    ]
    body = {
        'requests': requests
    }
    response = service.presentations().batchUpdate(
        presentationId=PRESENTATION_ID, body=body).execute()

    import matplotlib.pyplot as plt
    import numpy as np
    labels = 'Odd Non Prime guesses', 'Odd Prime Guesses', 'Even Prime Guesses (2)', 'Even Non Prime Guesses'
    sizes = [odd, prime, eprime, even]
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()



    plt.bar(range(len(divisible)), list(divisible.values()), align='center')
    plt.xticks(range(len(divisible)), list(divisible.keys()))
    plt.show()


    print("Guesses")
    pprint(guesses)

    winner = None
    winning_number = 1
    while not winner:
        print(f'Guessers for {winning_number}')
        print(guesses[winning_number])
        print('Remaining tries')
        print_guesses(participant_guesses, winning_number)
        x= input()
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
