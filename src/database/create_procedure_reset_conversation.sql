DELIMITER $$

CREATE PROCEDURE reset_conversation(
  IN `in_cid` VARCHAR(36)
)
BEGIN
  DECLARE `found_cid` VARCHAR(36);
  SELECT EXISTS(SELECT `conversation`.`cid`
      FROM `conversation`
      WHERE `conversation`.`cid` = `in_cid`)
      INTO `found_cid`;
        
  -- validate conversation existance. 
  IF `found_uid` = 0 THEN
      SIGNAL SQLSTATE '45000'
          SET MESSAGE_TEXT = 'Conversation does not exist.';
  END IF;
  
  DELETE FROM `message` WHERE `message`.`cid` = `in_cid`;
  DELETE FROM `graph` WHERE `graph`.`cid` = `in_cid`;
  
  COMMIT;
END $$

DELIMITER ;