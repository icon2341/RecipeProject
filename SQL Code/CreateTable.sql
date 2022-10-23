CREATE TABLE "User"
(
    UID             SERIAL PRIMARY KEY,
    username        varchar(120) NOT NULL,
    email           varchar(120),
    password        varchar(120) NOT NULL,
    create_datetime date         NOT NULL,
    last_access     date         NOT NULL
);

CREATE TABLE Pantry
(
    pantry_id SERIAL PRIMARY KEY
);

CREATE TABLE Ingredient
(
    ingredient_id    SERIAL PRIMARY KEY,
    item_name        varchar(120) NOT NULL,
    quantity_bought  int          NOT NULL,
    current_quantity int,
    unit_of_measure  varchar(20),
    purchase_date    date         NOT NULL,
    expiration_date  date,
    pantry_id        int,
    user_id          int,
    FOREIGN KEY (pantry_id) REFERENCES Pantry (pantry_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (user_id) REFERENCES "User" (UID)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Recipe
(
    servings    int,
    difficulty  varchar(255),
    description varchar(65535),
    rating      int NOT NULL,
    cook_time   time,
    RUID        SERIAL,
    recipe_name varchar(255),
    category    varchar(255),
    steps       varchar(65535),
    PRIMARY KEY (RUID),
    UID         int,
    FOREIGN KEY (UID) REFERENCES "User" (UID)
        ON DELETE CASCADE ON UPDATE CASCADE
);


/*
SELECT *
FROM Pantry
INNER JOIN Ingredient R on Pantry.pantry_id = R.pantry_id
*/
/* TODO: Fix this relation and make it 1 to many*/
/*may work as is*/

CREATE TABLE Cooks
(
    UID           int,
    date_made     varchar(120),
    RUID          int,
    quantity_made int,
    portions_made int,
    PRIMARY KEY (UID, RUID),
    FOREIGN KEY (UID) REFERENCES "User" (UID)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (RUID) REFERENCES Recipe (RUID)
        ON DELETE CASCADE ON UPDATE CASCADE
);

/* TODO: we need to implement these relations */

CREATE TABLE Creates
(
    date_created varchar(120),
    uid          int,
    FOREIGN KEY (uid) REFERENCES "User" (UID)
        ON DELETE CASCADE ON UPDATE CASCADE,
    RUID         int,
    FOREIGN KEY (RUID) REFERENCES Recipe (RUID)
        ON DELETE CASCADE ON UPDATE CASCADE
);


/* SELECT * from User */


CREATE TABLE Reads
(
    uid  int,
    FOREIGN KEY (uid) REFERENCES "User" (UID)
        ON DELETE CASCADE ON UPDATE CASCADE,
    RUID int,
    FOREIGN KEY (RUID) REFERENCES Recipe (RUID)
        ON DELETE CASCADE ON UPDATE CASCADE

);

CREATE TABLE Uses
(
    uid  int,
    FOREIGN KEY (uid) REFERENCES "User" (UID)
        ON DELETE CASCADE ON UPDATE CASCADE,
    RUID int,
    FOREIGN KEY (RUID) REFERENCES Recipe (RUID)
        ON DELETE CASCADE ON UPDATE CASCADE
);