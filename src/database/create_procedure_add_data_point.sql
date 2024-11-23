DELIMITER $$

CREATE PROCEDURE add_data_point(
  IN `in_cid` VARCHAR(36),
  IN `in_name` VARCHAR(100),
  IN `in_value` INT
) 
BEGIN
  DECLARE `cid_found` VARCHAR(36);

  SELECT EXISTS(SELECT `conversation`.`cid`
      FROM `conversation`
      WHERE `conversation`.`cid` = `in_cid`)
      INTO `cid_found`;
      
  -- validate conversation existance. 
  IF `cid_found` = 0 THEN
      SIGNAL SQLSTATE '45000'
          SET MESSAGE_TEXT = 'Conversation does not exist.';
  END IF;
  
  -- add to table
  INSERT INTO `graph`
    VALUES (`in_cid`, `in_name`, `in_value`);
    
  COMMIT;
END $$

DELIMITER ;