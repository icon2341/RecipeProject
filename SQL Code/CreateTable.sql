CREATE TABLE "User" (
    UID int,
    username varchar(120) NOT NULL,
    email varchar(120),
    password varchar(120) NOT NULL,
    create_datetime date NOT NULL,
    last_access date NOT NULL,
    PRIMARY KEY(uid)
);

CREATE TABLE Pantry(
   pantry_id int,
   PRIMARY KEY (pantry_id)
);

CREATE TABLE Ingredient(
    ingredient_id int,
    item_name varchar(120) NOT NULL,
    quantity_bought int NOT NULL,
    current_quantity int,
    unit_of_measure varchar(20),
    purchase_date date NOT NULL,
    expiration_date date,
    PRIMARY KEY(ingredient_id),
    pantry_id int,
    user_id int,
    FOREIGN KEY (pantry_id) REFERENCES Pantry(pantry_id)
                       ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (user_id) REFERENCES "User"(id)
                       ON DELETE CASCADE ON UPDATE CASCADE
    );

CREATE TABLE Recipe(
    servings int,
    difficulty varchar(255),
    description varchar(65535),
    rating int NOT NULL,
    cook_time time,
    RUID int,
    recipe_name varchar(255),
    category varchar(255),
    steps varchar(65535),
    PRIMARY KEY(RUID),
    UID int,
    FOREIGN KEY (UID) REFERENCES "User"(id)
                       ON DELETE CASCADE ON UPDATE CASCADE
);


/*
SELECT *
FROM Pantry
INNER JOIN Ingredient R on Pantry.pantry_id = R.pantry_id
*/
/* TODO: Fix this relation and make it 1 to many*/
/*may work as is*/

CREATE TABLE Cooks(
    UID int,
    date_made datetime,
    RUID int,
    quantity_made int,
    portions_made int,
    PRIMARY KEY (UID, RUID),
    FOREIGN KEY (UID) REFERENCES "User"(UID)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (RUID) REFERENCES Recipe(RUID)
        ON DELETE CASCADE ON UPDATE CASCADE
);

/* TODO: we need to implement these relations */

CREATE TABLE Creates
(
    date_created datetime,
    uid          varchar(250),
    FOREIGN KEY (uid) REFERENCES "User" (UID)
        ON DELETE CASCADE ON UPDATE CASCADE,
    RUID         varchar(25),
    FOREIGN KEY (RUID) REFERENCES Recipe (RUID)
        ON DELETE CASCADE ON UPDATE CASCADE
);


/* SELECT * from User */


CREATE TABLE Reads(
    uid          varchar(250),
    FOREIGN KEY (uid) REFERENCES "User" (UID)
        ON DELETE CASCADE ON UPDATE CASCADE,
    RUID         varchar(25),
    FOREIGN KEY (RUID) REFERENCES Recipe (RUID)
        ON DELETE CASCADE ON UPDATE CASCADE

);

CREATE TABLE Uses(
    uid          varchar(250),
    FOREIGN KEY (uid) REFERENCES "User" (UID)
        ON DELETE CASCADE ON UPDATE CASCADE,
    RUID         varchar(25),
    FOREIGN KEY (RUID) REFERENCES Recipe (RUID)
        ON DELETE CASCADE ON UPDATE CASCADE
);


/*
#Purchase:
SELECT * FROM User
INNER JOIN Ingredient I on User.id = I.user_id*/