-- Generic user data.
CREATE TABLE `user` (
    `created` DATETIME,
    `last_login` DATETIME,
	`username` VARCHAR(40) UNIQUE NOT NULL,
    `password_hash` VARCHAR(100) NOT NULL,
    `salt` VARCHAR(16) NOT NULL,
    `uid` VARCHAR(36) UNIQUE NOT NULL,
    PRIMARY KEY (`uid`)
);
