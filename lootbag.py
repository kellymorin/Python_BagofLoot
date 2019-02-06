import sys
import sqlite3

main_db = '/Users/kellymorin/workspace/server-side/orientation/advanced/exercises/bag_of_loot/data.db'

class LootBag:
    def __init__(self, db=main_db):
        self.db = db

    def add_toy(self, toy_name, child):
        """Adds a toy to the database.

        Arguments:
            toy {str} -- The name of the toy
            child {str} -- The name of the child
        Returns:
            toy {int} -- The ID of the newly created toy-child relationship
        """

        # Check to see if the child is currently in the database, if so return the instance of the child, if not create the child
        child_id = self.find_child(child)

        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO Toys VALUES (?, ?, ?, ?)
            """, (None, toy_name, 0, child_id))

            return cursor.lastrowid

    def find_child(self, child):
        """Queries the Children table to see if a child exists.

        Arguments:
            child {str} -- Name of Child
        Returns:
            child_id {int} --- ID of child
        """

        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()

            # Search the database for the child
            cursor.execute(f"""
                SELECT id
                FROM Children
                WHERE name LIKE "{child}"
            """)

            child_id = cursor.fetchone()

            if child_id != None:
                return child_id[0]
            else:
                return self.create_child(child)

    def create_child(self, child):
        """Creates a new child in the database

        Arguments:
            child {str} -- Name of Child
        Returns:
            child_id {int} --- ID of child
        """

        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO Children VALUES (?, ?)
            """, (None, child))

            return cursor.lastrowid

    def remove_toy(self, child, toy_name):
        """Removes a child's toy before it's delivered

        Arguments:
            child {str} -- Name of Child
            toy_name {str} -- Name of Toy
        """

        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()

            try:
                cursor.execute(f"""
                    DELETE FROM Toys
                    WHERE child_id IN (
                        SELECT child_id FROM Toys
                        INNER JOIN Children on Children.id = Toys.child_id
                        WHERE Children.name LIKE "{child}"
                    ) AND Toys.toy_name LIKE "{toy_name}"
                """)
            except sqlite3.OperationalError as error:
                print("Error:", error)

    def find_toy(self, child, toy_name):
        """Find a child's toy

        Arguments:
            child_name {str} -- Name of Child
            toy_name {str} -- Name of Toy
        """

        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()

            cursor.execute(f"""
                SELECT id
                FROM Toys
                WHERE child_id IN(
                    SELECT child_id from Toys
                    INNER JOIN Children ON Children.id = Toys.child_id
                    WHERE Children.name LIKE "{child}"
            ) AND Toys.toy_name LIKE "{toy_name}"
            """)

            toy = cursor.fetchone()

            # returns tuple with ID, or None if not found
            return toy

    def list_gifts(self):
        """Lists all of the gifts that have not yet been delivered and their assigned children
        """
        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT name, group_concat(toy_name, ', ') as toys
                FROM Children
                JOIN Toys ON child_id = children.id
                WHERE Toys.delivered == 0
                GROUP BY Children.name
            """)

            results= cursor.fetchall()

            if len(results) > 0:
                print("======== Gifts to be Delivered ========")
                for row in results:
                    print(row[0], ": ")
                    print(row[1], "\n")
            else:
                print("There are no gifts to be delivered")

    def list_gifts_single(self, child):
        """Lists the gifts assigned to a specific child

        Arguments:
            child {str} -- Name of Child
        """

        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()

            cursor.execute(f"""
                SELECT Children.name, group_concat(Toys.toy_name, ', ') as toys
                FROM Children
                JOIN Toys ON Toys.child_id = Children.id
                WHERE Toys.delivered == 0 AND Children.name LIKE "{child}"
            """)

            result = cursor.fetchone()

            if result[0] is None:
                print("Child not found")
            else:
                print(f"{result[0]}'s gifts: {result[1]}'")

    def deliver_gifts(self, child):
        """Marks a specific child's toys as delivered and prints a message

        Arguments:
            child {str} -- Name of the Child
        """

        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()

            cursor.execute(f"""
                SELECT Children.name, group_concat(Toys.toy_name, ', ') as toys
                FROM Children
                JOIN Toys ON Toys.child_id = Children.id
                WHERE Toys.delivered == 0 AND Children.name LIKE "{child}"
            """)

            have_gifts = cursor.fetchone()

            if have_gifts[0] is None:
                return print(f"Something went wrong. Either {child} has no gifts, already recieved their gifts or doesn't exist.")

            cursor.execute(f"""
                UPDATE Toys
                SET delivered=1
                WHERE child_id IN (
                    SELECT child_id
                    FROM Toys
                    JOIN Children ON Children.id = Toys.child_id
                    WHERE Children.name LIKE "{child}"
                )
            """)

            cursor.execute(f"""
                SELECT Children.name, group_concat(Toys.toy_name, ', ') as toys
                FROM Children
                JOIN Toys ON Toys.child_id = Children.id
                WHERE Toys.delivered == 1 AND Children.name LIKE "{child}"
            """)

            result = cursor.fetchone()

            if result[1] is not None:
                return print(f"{child}'s gifts were delivered!")

            elif result[1] is None:
                return print(f"Something went wrong. Either {child} doesn't exist or they have no gifts to deliver.")

if __name__ == "__main__":
    lb = LootBag()
    if len(sys.argv) > 1:

        if sys.argv[1] == 'add':
            print("Add gift")
            toy_name = sys.argv[2]
            child_name = sys.argv[3]
            lb.add_toy(toy_name, child_name)
            print(f"{toy_name} added for {child_name}")

        elif sys.argv[1] == 'remove':
            print("remove")
            child_name = sys.argv[2]
            toy_name = sys.argv[3]
            lb.remove_toy(child_name, toy_name)

        elif sys.argv[1] == 'ls':
            if(len(sys.argv)== 2):
                lb.list_gifts()
            else:
                lb.list_gifts_single(sys.argv[2])

        elif sys.argv[1] == 'deliver':
            if sys.argv[2]:
                lb.deliver_gifts(sys.argv[2])
            else:
                print("Missing child name argument")

        elif sys.argv[1] == 'help':
            print('help')

        else:
            print("You cannot do that! Type help")

    else:
        print("Not enough arguments")