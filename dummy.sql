INSERT INTO "person" ("Brukernavn", "Passord", "Ansatt")
VALUES ('Geralt', 'hesterbest', 0),
('Yennefer', 'qwerty', 0),
('Roach', 'pizza', 0),
('Jaskier', 'nyttpassord', 1);


INSERT INTO "burger" ("Navn")
VALUES ('Whopper Queen'),
('Triple Cheesy Princess'),
('Kingdom Fries');


INSERT INTO "ordre" ("Hvem", "Hva", "Produsert", "personID", "burgerID")
VALUES ('Geralt', 'Whopper Queen', 1, 21, 1),
('Geralt', 'Whopper Queen', 0, 21, 1),
('Jaskier', 'Triple Cheesy Princess', 0, 24, 2),
('Roach', 'Whopper Queen', 0, 23, 1);





INSERT INTO "ingrediens" ("Navn", "Antall")
VALUES ("Burgerbrød", 9001),
("Burgerkjøtt", 10),
("Salat", 8008),
("Tomat", 1337),
("Ost", 42),
("Agurk", 666),
("Potet", 420);


INSERT INTO "burgerIngrediens" ("burgerID", "ingrediensID") VALUES (1, 1);
INSERT INTO "burgerIngrediens" ("burgerID", "ingrediensID") VALUES (1, 2);
INSERT INTO "burgerIngrediens" ("burgerID", "ingrediensID") VALUES (1, 3);
INSERT INTO "burgerIngrediens" ("burgerID", "ingrediensID") VALUES (1, 4);

INSERT INTO "burgerIngrediens" ("burgerID", "ingrediensID") VALUES (2, 1);
INSERT INTO "burgerIngrediens" ("burgerID", "ingrediensID") VALUES (2, 2);
INSERT INTO "burgerIngrediens" ("burgerID", "ingrediensID") VALUES (2, 3);
INSERT INTO "burgerIngrediens" ("burgerID", "ingrediensID") VALUES (2, 4);
INSERT INTO "burgerIngrediens" ("burgerID", "ingrediensID") VALUES (2, 5);

INSERT INTO "burgerIngrediens" ("burgerID", "ingrediensID") VALUES (3, 7);


