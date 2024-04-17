CREATE TABLE users (
    user_id INT PRIMARY KEY auto_increment,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE `reports` (
    `report_id` int NOT NULL AUTO_INCREMENT,
    `lat` DOUBLE NOT NULL,
    `lng` DOUBLE NOT NULL,
    `file_path` varchar(255) NOT NULL,
    `user_id` int DEFAULT NULL,
    PRIMARY KEY (`report_id`),
    KEY `userid_idx` (`user_id`),
    CONSTRAINT `user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;
