DROP PROCEDURE IF EXISTS `update_user_auth`;

DELIMITER $$

-- update salt on login.
CREATE PROCEDURE `update_user_auth` (
	IN `in_uid` VARCHAR(36),
    IN `in_password_hash` VARCHAR(100),
    IN `in_salt` VARCHAR(16)
) BEGIN
	UPDATE `user`
		SET `user`.`password_hash` = `in_password_hash`, `user`.`salt` = `in_salt`, `user`.`last_login` = now()
        WHERE `user`.`uid` = `in_uid`;
	
    COMMIT;
end $$

DELIMITER ;