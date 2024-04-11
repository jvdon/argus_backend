CREATE TABLE reports (
	id INT PRIMARY KEY auto_increment,
    coords VARCHAR(255) NOT NULL,
    image VARCHAR(255) NOT NULL,
);

CREATE TABLE users (
	id INT PRIMARY KEY auto_increment,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);
