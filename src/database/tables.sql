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

-- sessions
CREATE TABLE `session` (
	`created` DATETIME,
    `last_access` DATETIME,
    `death_time` DATETIME,
    `sid` VARCHAR(36) UNIQUE NOT NULL,
    `uid` VARCHAR(36) NOT NULL,
    PRIMARY KEY (`sid`),
    FOREIGN KEY (`uid`) REFERENCES `user`(`uid`)
);

-- chats
CREATE TABLE `chat` (
	`message` VARCHAR(12288),
    `role` VARCHAR(24),
    `order` INT,
    `cid` VARCHAR(36) UNIQUE NOT NULL,
    `uid`VARCHAR(36) NOT NULL,
    PRIMARY KEY (`cid`),
    FOREIGN KEY (`cid`) REFERENCES `user`(`uid`)
);