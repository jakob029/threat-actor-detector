DELIMITER $$

CREATE PROCEDURE `delete_user`(
  IN `in_uid` VARCHAR(36)
)
BEGIN
  DELETE FROM `user`
    WHERE `user`.`uid` = `in_uid`;
    
  COMMIT;
END $$

DELIMITER ;