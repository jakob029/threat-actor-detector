DROP PROCEDURE IF EXISTS `validate_session_token`;

DELIMITER $$
-- Procedure to validate given session token.
CREATE PROCEDURE `validate_session_token` (
    IN `in_token` VARCHAR(36),
	OUT `out_uid` VARCHAR(36)
)
BEGIN
	-- collect token.
	DECLARE `found_death_time` DATETIME;
	SELECT `session`.`death_time` 
		FROM `session`
		WHERE `session`.`token` = `in_token` 
        INTO `found_death_time`;
	
    -- validate existance.
    IF `found_death_time` = NULL THEN
		-- send error.
        SIGNAL SQLSTATE '45000'
			SET MESSAGE_TEXT = 'No valid tokens found.';
    END IF;
    
    -- validate age.
    IF `found_death_time` > now() THEN
		-- remove dead token.
		DELETE FROM `session`
			WHERE `session`.`token` = `in_token`;
		
        -- send error.
		SIGNAL SQLSTATE '45000'
			SET MESSAGE_TEXT = 'Token dead.';
    END IF;
    
    -- update last used datetime.
    UPDATE `session`
		SET `session`.`last_access` = now()
        WHERE `session`.`token` = `in_token`;
    
    -- get uid.
    SELECT `session`.`uid`
		FROM `session`
        WHERE `session`.`token` = `in_token`
        INTO `out_uid`;
	
    COMMIT;
END $$

DELIMITER ;