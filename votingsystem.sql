CREATE DATABASE voting_system;

USE voting_system;

CREATE TABLE votes (
    candidate_name VARCHAR(50) PRIMARY KEY,
    vote_count INT DEFAULT 0
);

INSERT INTO votes (candidate_name) VALUES ('Ashu 1'), ('anjali 2'), ('anisha 3');

