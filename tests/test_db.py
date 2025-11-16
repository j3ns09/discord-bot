# This test aims at creating the database, inserting dummy data, and deleting it.

import os
import sys

# Get the parent directory of this file (project_root)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

# Creation of the database using create_db.py and create_db.sql
from cogs.events.db.create_db import initialize_db
from cogs.events.logger import Logger
from cogs.events.storage import Storage

# creates the db
initialize_db()


# checks its existence
db_dir = os.path.join("cogs", "events", "db", "alexandre.db")


def check_existence():
    assert os.path.isfile(db_dir)


# user data
# has to be (name, birthday)
user1 = (123, "alice", "2000-01-01")
user2 = (456, "bob", "2002-11-21")
user3 = (789, "jeff", "2006-08-12")

# role data
# has to be (name)
role1 = "small"
role2 = "medium"
role3 = "big"

# log data
# has to be (user id, method, channel name, population)

# alice was the first to join, population is now 1
log1 = (123, Storage.methods.JOIN, "channel1", 1)
# then comes bob
log2 = (456, Storage.methods.JOIN, "channel1", 2)
# and then jeff
log3 = (789, Storage.methods.JOIN, "channel1", 3)
# bob leaves
log4 = (456, Storage.methods.QUIT, "channel1", 2)
# jeff mutes
log5 = (789, Storage.methods.MUTE, "channel1", 2)
# alice leaves
log6 = (123, Storage.methods.QUIT, "channel1", 1)
# jeff unmutes
log7 = (789, Storage.methods.UNMUTE, "channel1", 1)
# jeff leaves
log8 = (789, Storage.methods.QUIT, "channel1", 0)

logs = (log1, log2, log3, log4, log5, log6, log7, log8)

# creates object storage that links with db
storage = Storage()

# creates object logger for log in db
logger = Logger()


# insert data (user, role, logs, champion)
def insert_data():
    # user
    storage.add_user(*user1)
    storage.add_user(*user2)
    storage.add_user(*user3)

    # role
    storage.add_role(role1)
    storage.add_role(role2)
    storage.add_role(role3)

    # logs
    for log in logs:
        storage.add_log(*log)

    # alice is champ (big) with a time of 20 hours
    storage.add_champion(123, 3, 20)

    # alice is champ (small) with a time of 1 hour
    storage.add_champion(456, 1, 1)


# gets the user data
def get_data():
    assert len(storage.get_users()) == 3
    assert storage.get_user(123)["name"] == "alice"
    assert storage.get_user(456)["name"] == "bob"
    assert storage.get_user(789)["name"] == "jeff"

    # gets roles
    assert len(storage.get_roles()) == 3

    # gets logs / yield
    assert len(storage.get_logs()) == len(logs)
    # put them in a file
    for log in storage.yield_logs():
        logger.write_logs(log)
    # check if log file exists
    assert os.path.isfile(logger.filename)

    print(storage.get_champions())
    assert len(storage.get_champions()) == 2


# cleanup
def cleanup():
    # clear the log using logger
    logger.clean()
    # checks if log file was indeed removed
    assert not os.path.isfile(logger.filename)

    os.remove(db_dir)
    os.rmdir(logger.dir)


def main():
    try:
        check_existence()
        insert_data()
        get_data()
    finally:
        pass
        # cleanup()


if __name__ == "__main__":
    main()
