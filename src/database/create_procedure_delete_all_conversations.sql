DELIMITER $$

CREATE PROCEDURE `delete_all_conversations`(
  IN `in_uid` VARCHAR(36)
)
BEGIN
  DELETE FROM `conversation`
    WHERE `conversation`.`uid` = `in_uid`;
    
  COMMIT;
END $$

DELIMITER ;