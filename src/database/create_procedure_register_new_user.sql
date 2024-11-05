DROP PROCEDURE IF EXISTS `register_new_user`;

DELIMITER $$
-- Procedure to register a new user
CREATE PROCEDURE `register_new_user` (
	IN `in_username` VARCHAR(40),
    IN `in_password_hash` VARCHAR(100),
    IN `in_salt` VARCHAR(16)
)
BEGIN
	-- generate 36 char uid
	DECLARE `uid` VARCHAR(36);
	SELECT uuid() INTO `uid`;
    
    -- insert into database
    INSERT INTO `user` (`username`, `password_hash`, `salt`, `uid`, `created`, `last_login`)
		VALUE (in_username, in_password_hash, in_salt, uid, now(), 0);
	
    COMMIT;
END $$

DELIMITER ;