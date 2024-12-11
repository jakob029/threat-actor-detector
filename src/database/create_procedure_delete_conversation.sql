DELIMITER $$

CREATE PROCEDURE `delete_conversation`(
  IN `in_cid` VARCHAR(36)
)
BEGIN
  DELETE FROM `conversation`
    WHERE `conversation`.`cid` = `in_cid`;
    
  COMMIT;
END $$

DELIMITER ;