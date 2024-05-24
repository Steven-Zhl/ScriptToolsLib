DELIMITER $$

CREATE FUNCTION URL_UNQUOTE(input TEXT) RETURNS TEXT
    -- author@Steven-Zhl
    READS SQL DATA
BEGIN
    DECLARE reg_exp VARCHAR(18) DEFAULT '(%[0-9a-zA-Z]{2})+'; -- 匹配URL编码内容的正则表达式
    DECLARE substring TEXT;
    DECLARE substring_unhex TEXT;
    IF REGEXP_INSTR(input, reg_exp) = 0 THEN -- 本就不包含URL encode内容，直接返回原内容
        RETURN input;
    ELSE
        WHILE REGEXP_INSTR(input, reg_exp) != 0
            DO
                SET substring = REGEXP_SUBSTR(input, reg_exp); -- 提取URL编码内容
                SET substring_unhex = UNHEX(REPLACE(substring, '%', '')); -- 将这部分进行解码
                SET input = REPLACE(input, substring, substring_unhex); -- 替换原内容
            END WHILE;
        RETURN input;
    END IF;
END$$

DELIMITER;