# Bag o' Loot

This exercise requires the use of [command line parameters](http://www.pythonforbeginners.com/argv/more-fun-with-sys-argv).
It also touches on many of the things you've learned up to this point in Python and SQL. It's  good measure of your comfort level with the server-side concepts you'll need to understand before we move on to building applications with Django

## Setup

```
mkdir -p ~/workspace/python/exercises/cli && cd $_
touch lootbag.py
```

## Instructions

You have an acquaintance whose job is to, once a year, delivery presents to the best kids around the world. They have a problem, though. There are so many good boys and girls in the world now, that their old paper accounting systems just don't cut it anymore. They want you to write a program that will let them do the following tasks.

1. Add a toy to the bag o' loot, and label it with the child's name who will receive it. The first argument must be the word `add`. The second argument is the gift to be delivered. The third argument is the name of the child.

    ```bash
    python lootbag.py add kite suzy
    python lootbag.py add baseball michael
    ```

1. Remove a toy from the bag o' loot in case a child's status changes before delivery starts.

    ```bash
    python lootbag.py remove suzy kite
    python lootbag.py remove michael baseball
    ```

1. Produce a list of children currently receiving presents.

    ```bash
    python lootbag.py ls
    ```

1. List toys in the bag o' loot for a specific child.

    ```bash
    python lootbag.py ls suzy
    ```

1. Specify when a child's toys have been delivered.

    ```bash
    python lootbag.py delivered suzy
    ```


## Requirements

### Testing
Each feature of the app must be tested. Use Python's unittest module to create test coverage for the following app requirements

1. Items can be added to bag, and assigned to a child.
1. Items can be removed from bag, per child. Removing `ball` from the bag should not be allowed. A child's name must be specified.
1. Must be able to list all children who are getting a toy.
1. Must be able to list all toys for a given child's name.
1. Must be able to set the *delivered* property of a child's toys -- which defaults to `false`-- to `true`.


## Bonus Features

1. Write a response for the argument `python lootbag.py help` that lists all of the possible arguments, and what they do.
1. Create a shortcut combination of arguments that can remove *all* toys from the bag for a child who has been deemed naughty.

## Persistent Storage

You must persist the data to disk, so that you can use it between executions of the application. You will need to write the data to an sqlite db using the sqlite3 module.
Create a quick ERD that represents the two types of data in this application. Then use that ERD to inform the tables you'll create in a `.sql` file that, when executed, will build your db tables.