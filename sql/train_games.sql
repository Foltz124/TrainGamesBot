PRAGMA foreign_keys=ON;

CREATE TABLE IF NOT EXISTS "player"(
    id INT PRIMARY KEY NOT NULL,
    username CHAR(20)
);

CREATE TABLE IF NOT EXISTS "game"(
    id INTEGER PRIMARY KEY NOT NULL,
    title CHAR(20) NOT NULL,
    description char(50),
    turn INTEGER NOT NULL,
    round CHAR(10) NOT NULL,
    current_player INTEGER NOT NULL,
    status CHAR(10) NOT NULL,
    updated_at INT,
    FOREIGN KEY(current_player) REFERENCES "player"(id)
);
