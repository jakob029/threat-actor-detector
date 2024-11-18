DROP PROCEDURE IF EXISTS `create_session_token`;

DELIMITER $$
-- Procedure to validate given session token.
CREATE PROCEDURE `create_session_token` (
	IN `in_uid` VARCHAR(36),
    OUT `out_token` VARCHAR(36)
)
BEGIN
	DECLARE `found_uid` VARCHAR(36);
    SELECT EXISTS(SELECT `user`.`uid`
		FROM `user`
        WHERE `user`.`uid` = `in_uid`)
        INTO `found_uid`;
        
	-- validate usser existance. 
	IF `found_uid` = 0 THEN
		SIGNAL SQLSTATE '45000'
			SET MESSAGE_TEXT = 'User does not exist.';
	END IF;
    
    -- add token.
    INSERT INTO `session` (`created`, `last_access`, `death_time`, `token`, `uid`)
		VALUES (now(), now(), date_add(now(), INTERVAL 24 HOUR), uuid(), `in_uid`);
        
	COMMIT;
END $$

DELIMITER ; 