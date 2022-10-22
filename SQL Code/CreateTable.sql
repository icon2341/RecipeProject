CREATE TABLE User (
    id int,
    username varchar(120) NOT NULL,
    email varchar(120),
    password varchar(120) NOT NULL,
    create_datetime datetime NOT NULL,
    last_access datetime NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE Ingredient(
    ingredient_id int,
    item_name varchar(120) NOT NULL,
    quantity_bought int NOT NULL,
    current_quantity int,
    unit_of_measure varchar(20),
    purchase_date datetime NOT NULL,
    expiration_date datetime,
    PRIMARY KEY(ingredient_id)
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
    
    PRIMARY KEY(RUID),
);

CREATE TABLE Pantry(
   pantry_id int,
    
);