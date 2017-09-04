from random import choice, randint
import sqlite3

from faker import Faker


def create_tables(connection):
    # players table
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE player (
            _id INTEGER PRIMARY KEY,
            first_name TEXT(30) NOT NULL,
            last_name TEXT(30) NOT NULL,
            height_ft INTEGER NOT NULL,
            height_in INTEGER NOT NULL
        )
    ''')

    # match
    cursor.execute('''
        CREATE TABLE match (
            _id INTEGER PRIMARY KEY,
            opponent TEXT(30) NOT NULL,
            our_score INTEGER NOT NULL,
            their_score INTEGER NOT NULL,
            year INTEGER NOT NULL
        )
    ''')

    # 
    cursor.execute('''
        CREATE TABLE attack_statistics (
            _id INTEGER PRIMARY KEY,
            player_id INTEGER NOT NULL,
            match_id INTEGER NOT NULL,
            shot_attempts INTEGER NOT NULL,
            goals INTEGER NOT NULL,
            assists INTEGER NOT NULL,

            FOREIGN KEY(player_id) REFERENCES player(_id),
            FOREIGN KEY(match_id) REFERENCES match(_id)
        )
    ''')

    #
    connection.commit()


def populate(connection):
    cursor = connection.cursor()
    fake = Faker()
    roster_size = 23
    opponents = [
        'Locomotives', 'Jets', 'Hot Rods',
        'Braves', 'Nationals', 'Pioneers',
        'Mustangs', 'Wolves', 'Thunderbirds',
        'Pink Flamingos', 'Dead Rabbits']

    # create players
    for _id in range(23):
        player_id = _id + 1
        first_name = fake.first_name()
        last_name = fake.last_name()
        height_ft = choice([5,5,5,5,5,5,5,6,6,6,6])
        height_in = choice([0,1,2,3,3,3,4,4,4,5,6,6,6,7,8,8,8,9,10,10,10,11,12])
        stmt = '''
            INSERT INTO player
            VALUES (%d, '%s', '%s', %d, %d)
        ''' % (player_id, first_name, last_name, height_ft, height_in)
        cursor.execute(stmt)

    # matches
    for _id, team in enumerate(opponents):
        match_id = _id + 1
        our_score = randint(0, 5)
        their_score = randint(0, 5)
        stmt = '''
            INSERT INTO match
            VALUES (%d, '%s', %d, %d, %d)
        ''' % (match_id, team, our_score, their_score, 2017)
        cursor.execute(stmt)
        print('Match: USA vs %s (%d : %d)' % (team, our_score, their_score))

        # 
        active_players = randint(1, 15)
        roster = set()
        total_goals = our_score
        while len(roster) < active_players:
            random_player_id = randint(1, roster_size)

            if random_player_id not in roster:
                roster.add(random_player_id)
                shot_attempts = randint(0, 12)
                assists = choice([0,0,0,randint(0, our_score)])
                goals = 0

                stmt = '''
                    INSERT INTO attack_statistics
                    (player_id, match_id, shot_attempts, goals, assists)
                    VALUES (%d, %d, %d, %d, %d)
                ''' % (random_player_id, match_id, shot_attempts, goals, assists)
                cursor.execute(stmt)

        # update goals
        for g in range(our_score):
            random_player_id = choice(list(roster))
            goal_query_stmt = '''
                SELECT a.goals
                FROM attack_statistics AS a
                WHERE a.match_id=%d AND a.player_id=%d
            ''' % (match_id, random_player_id)
            cursor.execute(goal_query_stmt)
            goals = cursor.fetchone()[0]

            goal_update_stmt = '''
                UPDATE attack_statistics
                SET goals=%d
                WHERE player_id=%d
            ''' % (goals+1, random_player_id)
            cursor.execute(goal_update_stmt)
            print('  > Player %d scored' % (random_player_id))

    # commit
    connection.commit()


def main():
    conn = sqlite3.connect('sportsteam.sqlite')
    try:
        create_tables(conn)
        populate(conn)
    finally:
        conn.close()


main()
