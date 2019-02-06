-- DELETE FROM Children;
-- DELETE FROM Toys;

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS Children;
DROP TABLE IF EXISTS Toys;

-- Create table Children
CREATE TABLE `Children`(
  `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  `name` TEXT NOT NULL
);

INSERT INTO Children VALUES(null, 'Sebastian');
INSERT INTO Children VALUES(null, 'Austin');
INSERT INTO Children VALUES(null, 'Elyse');
INSERT INTO Children VALUES(null, 'Rachel');

-- Create table Toys
CREATE TABLE `Toys`(
  `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  `toy_name` TEXT NOT NULL,
  `delivered` INTEGER NOT NULL DEFAULT 0 CHECK (Delivered between 0 AND 1),
  `child_id` INTEGER NOT NULL,
  FOREIGN KEY(`child_id`)
  REFERENCES `Children`(`id`)
  ON DELETE CASCADE
);

INSERT INTO Toys VALUES(null, 'art supplies', 0, 1);
INSERT INTO Toys VALUES(null, 'hammock', 0, 2);
INSERT INTO Toys VALUES(null, 'VR Headset', 1, 3);
INSERT INTO Toys VALUES(null, 'doll', 1, 4);
