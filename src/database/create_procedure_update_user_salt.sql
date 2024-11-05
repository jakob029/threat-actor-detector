DROP PROCEDURE IF EXISTS `update_user_salt`;

DELIMITER $$

-- update salt on login.
CREATE PROCEDURE `update_user_salt` (
	IN `in_uid` VARCHAR(36),
    IN `in_salt` VARCHAR(16)
) BEGIN
	UPDATE `user`
		SET `user`.`salt` = `in_salt`, `user`.`last_login` = now()
        WHERE `user`.`uid` = `in_uid`;
end $$

DELIMITER ;