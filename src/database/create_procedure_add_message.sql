DROP PROCEDURE add_message;

DELIMITER $$

CREATE PROCEDURE `add_message` (
    IN `in_message` VARCHAR(12288),
    IN `in_role` VARCHAR(24),
    IN `in_cid` VARCHAR(36)
)
BEGIN
	DECLARE `validator` VARCHAR(36);
	DECLARE `count` INT;
    
    SELECT EXISTS(SELECT `conversation`.`cid`
		FROM `conversation`
        WHERE `conversation`.`cid` = `in_cid`)
        INTO `validator`;
        
	-- validate user-chat combo exist. 
	IF `validator` = 0 THEN
		SIGNAL SQLSTATE '45000'
			SET MESSAGE_TEXT = 'Conversation does not exist.';
	END IF;

    SELECT count(*)
		FROM `message`
        WHERE `message`.`cid` = `in_cid`
        INTO `count`;
  
    -- continue conversation.
    INSERT INTO `message`
		VALUES (`in_cid`, `count`, `in_role`, `in_message`);

    COMMIT;
END $$

DELIMITER ;