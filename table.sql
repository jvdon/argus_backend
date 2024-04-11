CREATE TABLE users (
    id INT PRIMARY KEY auto_increment,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE `reports` (
    `id` int NOT NULL AUTO_INCREMENT,
    `coords` varchar(255) NOT NULL,
    `image` varchar(255) NOT NULL,
    `userId` int DEFAULT NULL,
    PRIMARY KEY (`id`),
    KEY `userid_idx` (`userId`),
    CONSTRAINT `userid` FOREIGN KEY (`userId`) REFERENCES `users` (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;
