import pandas as pd
import numpy as np
from pathlib import Path

from src.exceptions import CannotLoadCharacterError
from src.inspiration_message import messages

# Define and create a folder in the user's folder
storage_folder = Path().home() / '.youdied'
# simple death count .txt file folder
death_count_folder = storage_folder / 'deathCount'

# define files to store statistics
session_file = storage_folder / 'sessions.csv'  # Store character names (and session durations?)
death_file = storage_folder / 'deaths.csv'  # Long format of character deaths
message_file = storage_folder / 'messages.csv'


def initialize_storage():
    # define column names for dataframes
    session_columns = ['Character', 'Started']
    death_columns = ['Character', 'TimeOfDeath']
    message_columns = ['Message', 'Used']

    # create folders if not existing
    storage_folder.mkdir(parents=True, exist_ok=True)
    death_count_folder.mkdir(parents=True, exist_ok=True)

    # create files if not existing
    if not session_file.exists():
        session_df = pd.DataFrame(columns=session_columns)
        session_df.to_csv(session_file)
    if not death_file.exists():
        death_df = pd.DataFrame(columns=death_columns)
        death_df.to_csv(death_file)
    if not message_file.exists():
        message_df = pd.DataFrame(((p, 0) for p in messages), columns=message_columns)
        message_df.to_csv(message_file, encoding='utf8')

    session_df = pd.read_csv(session_file, index_col=0)
    death_df = pd.read_csv(death_file, index_col=0)
    message_df = pd.read_csv(message_file, index_col=0)
    return session_df, death_df, message_df


session_df, death_df, message_df = initialize_storage()


def get_death_count_file(character):
    death_count_file = death_count_folder / f'{character}.txt'
    if not death_count_file.exists():
        death_count_file.touch()
        death_count_file.write_text('0')
    return death_count_file


def get_death_count(character):
    return death_df[death_df.Character == character].shape[0]


def write_death_count(character):
    # Write the updated death count to a file in the death_count_folder
    #  with the character name as file name
    n_deaths = get_death_count(character)
    get_death_count_file(character).write_text(str(n_deaths), encoding='utf8')


def initialize_death_file(character):
    get_death_count_file(character)


def add_death(character):
    new_index = death_df.shape[0]
    # add new row
    death_df.loc[new_index] = (character, pd.Timestamp('now'))
    # save file
    death_df.to_csv(death_file, encoding='utf8')
    # update death count file
    write_death_count(character)


def add_session(character):
    new_index = session_df.shape[0]
    session_df.loc[new_index] = (character, pd.Timestamp('now'))
    session_df.to_csv(session_file, encoding='utf8')


def create_inspiration_message():
    # create candidates from the least used messages
    candidates = message_df[message_df.Used == message_df.Used.min()]
    # pick a random candidate row
    new_message_ix = np.random.choice(candidates.index)
    # update use count and save to file
    message_df.loc[new_message_ix, 'Used'] += 1
    message_df.to_csv(message_file)
    # get message string
    message = message_df.loc[new_message_ix].Message
    return message


def process_death(character, score):
    add_death(character)
    inspiration_message = create_inspiration_message()
    print(f'Death # {get_death_count(character)} ({score*100:03.2f}%)', end='\t')
    #print(f'But, someone else in your shoes has said something like:\n')
    print(f'{inspiration_message}\n')


def get_previous_character():
    try:
        return session_df.iloc[-1].Character
    except IndexError:
        raise CannotLoadCharacterError()


def get_all_characters():
    # list of all unique characters
    characters = session_df.Character.unique().tolist()
    # get last start time for each character
    df_data = [
        (
            session_df[session_df.Character == c].Started.max(),
            c,
            death_df[death_df.Character == c].shape[0]
        )
        for c in characters
    ]
    df = pd.DataFrame(df_data, columns=['Started last', 'Character', 'Death count'])
    return df.sort_values(by='Started last', ascending=False)


def print_previous_character():
    try:
        print('Previous character used:')
        print(session_df[-1:].to_string(index=False, col_space=20))
    except IndexError:
        raise CannotLoadCharacterError()


def print_all_characters():
    print('All characters, in descending order by last session start:')
    all_characters_df = get_all_characters()
    if all_characters_df.shape[0] > 0:
        print(all_characters_df.to_string(index=False, col_space=20))
    else:
        print('There are no characters in storage.')
