DELIMITER $$

CREATE PROCEDURE `create_conversation` (
	IN `in_uid` VARCHAR(36),
    IN `in_title` VARCHAR(64),
    OUT `out_cid` VARCHAR(36)
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
    SELECT uuid() INTO `out_cid`;
    -- create new chat.
    INSERT INTO `conversation`
		VALUES (`out_cid`, `in_uid`, `in_title`);
        
	COMMIT;
END $$

DELIMITER ;