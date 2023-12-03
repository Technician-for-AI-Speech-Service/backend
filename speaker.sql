select user();
show databases;

drop schema Insa4_IOTB_final_3;
create schema Insa4_IOTB_final_3;
use Insa4_IOTB_final_3;
show schemas;
show tables;
select * from t_User;
select schema();

-- -- 테이블 순서는 관계를 고려하여 한 번에 실행해도 에러가 발생하지 않게 정렬되었습니다.

-- -- TTS Table Create SQL
-- -- 테이블 생성 SQL - TTS
-- CREATE TABLE t_TTS
-- (
--     `user_Id`        VARCHAR(50)    NOT NULL    COMMENT 'user_Id', 
--     `speak_Id`       INT UNSIGNED   NOT NULL    COMMENT 'speak_Id', 
--     `text_Id`        INT UNSIGNEd   NOT NULL    AUTO_INCREMENT COMMENT 'text_Id', 
-- 	`text_Content`   VARCHAR(2000)  NULL    COMMENT 'text_Content', 
--      PRIMARY KEY (text_Id)
-- );

-- -- 테이블 Comment 설정 SQL - TTS
-- ALTER TABLE t_TTS COMMENT 'TTS';


-- -- Speech Table Create SQL
-- -- 테이블 생성 SQL - Speech
-- CREATE TABLE t_Speech
-- (
--     `user_Id`        VARCHAR(50)    NOT NULL    COMMENT 'user_Id', 
--     `speak_Id`       INT UNSIGNED   NOT NULL    AUTO_INCREMENT COMMENT 'speak_Id', 
--     `speak_Content`  VARCHAR(50)    NULL        COMMENT 'speak_Content', 
--      PRIMARY KEY (speak_Id),
--      UNIQUE (user_Id)
-- );

-- -- 테이블 Comment 설정 SQL - Speech
-- ALTER TABLE t_Speech COMMENT 'Speech';

-- -- Foreign Key 설정 SQL - Speech(speak_Id) -> TTS(speak_Id)
-- ALTER TABLE t_TTS
--     ADD CONSTRAINT FK_Speech_speak_Id_TTS_speak_Id FOREIGN KEY (speak_Id)
--         REFERENCES t_Speech (speak_Id) ON DELETE RESTRICT ON UPDATE RESTRICT;
        

-- -- Foreign Key 삭제 SQL - Speech(speak_Id)
-- -- ALTER TABLE Speech
-- -- DROP FOREIGN KEY FK_Speech_speak_Id_TTS_speak_Id;


-- -- User Table Create SQL
-- -- 테이블 생성 SQL - User
-- CREATE TABLE t_User
-- (
--     `user_Name`        VARCHAR(50)    NOT NULL    COMMENT 'user_Name', 
--     `user_Id`          VARCHAR(50)    NOT NULL    COMMENT 'user_Id', 
--     `user_Phone`	   VARCHAR(50)    NOT NULL    COMMENT 'user_Phone',
--     `user_Pwd`         VARCHAR(50)    NOT NULL    COMMENT 'user_Pwd', 
--     `user_Gender`      VARCHAR(50)    NOT NULL    COMMENT 'user_Gender', 
--     `user_Disability`  VARCHAR(50)    NOT NULL    COMMENT 'user_Disability', 
--     `user_Year`        INT            NOT NULL    COMMENT 'user_Year', 
--     `user_Region`      VARCHAR(50)    NOT NULL    COMMENT 'user_Region', 
--     `user_Phone1`      VARCHAR(50)    NOT NULL    COMMENT 'user_Phone1', 
--     `user_Phone2`      VARCHAR(50)    NOT NULL    COMMENT 'user_Phone2', 
-- 	`user_Phone3`      VARCHAR(50)    NOT NULL    COMMENT 'user_Phone3', 
--     `user_Date`		   DATE			  NOT NULL	  COMMENT 'user_Date',
-- 	`user_PostNumber`  VARCHAR(50)    NOT NULL    COMMENT 'user_PostNumber',
--     `user_Address`	   VARCHAR(200)   NOT NULL    COMMENT 'user_Address',
--     `user_Details`     VARCHAR(200)   NOT NULL    COMMENT 'user_Details',
--      PRIMARY KEY (user_Id)
-- );

-- -- 테이블 Comment 설정 SQL - User
-- ALTER TABLE t_User COMMENT 'User';

-- -- Foreign Key 설정 SQL - User(user_Id) -> Speech(user_Id)
-- ALTER TABLE t_Speech
--     ADD CONSTRAINT FK_User_user_Id_Speech_user_Id FOREIGN KEY (user_Id)
--         REFERENCES t_User (user_Id) ON DELETE RESTRICT ON UPDATE RESTRICT;



-- -- Foreign Key 삭제 SQL - User(user_Id)
-- -- ALTER TABLE User
-- -- DROP FOREIGN KEY FK_User_user_Id_Speech_user_Id;

-- INSERT INTO t_User (user_Name, user_Id, user_Phone, user_Pwd, user_Gender, user_Disability, user_Year, user_Region, user_Phone1, user_Phone2, user_Phone3, user_Date, user_PostNumber, user_Address, user_Details) 
-- VALUES ('김창렬', 'user_Id1', '01034567890', '1234', '남', '언어/청각장애', 1998, '부산', '010', '3456', '7890', '1998-03-01', '12345', '주소', '상세주소');

-- INSERT INTO t_User (user_Name, user_Id, user_Phone, user_Pwd, user_Gender, user_Disability, user_Year, user_Region, user_Phone1, user_Phone2, user_Phone3, user_Date, user_PostNumber, user_Address, user_Details) 
-- VALUES ('홍길동', 'user_Id2', '01012345678', '1234', '남', '언어/청각장애', 1997, '경북', '010', '1234', '5678', '1997-03-01', '12345', '주소', '상세주소');

-- INSERT INTO t_User (user_Name, user_Id, user_Phone, user_Pwd, user_Gender, user_Disability, user_Year, user_Region, user_Phone1, user_Phone2, user_Phone3, user_Date, user_PostNumber, user_Address, user_Details) 
-- VALUES ('김길동', 'user_Id3', '0102345678', '1234', '남', '언어/청각장애', 1998, '광주', '010', '2345', '6789', '1998-03-01', '12345', '주소', '상세주소');

-- INSERT INTO t_User (user_Name, user_Id, user_Phone, user_Pwd, user_Gender, user_Disability, user_Year, user_Region, user_Phone1, user_Phone2, user_Phone3, user_Date, user_PostNumber, user_Address, user_Details) 
-- VALUES ('장첸', 'jang', '01023231212', SHA('1234'), '남', '언어/청각장애', 1992, '광주', '010', '2323', '1212', '1992-02-22', '12312', '주소', '상세주소');


-- INSERT INTO t_Speech (user_Id, speak_Id) VALUES ('user_Id1', speak_Id);
-- INSERT INTO t_Speech (user_Id, speak_Id) VALUES ('user_Id2', speak_Id);

-- INSERT INTO t_TTS (user_Id, speak_Id) VALUES ('user_Id1', 2);


-- select * from t_User;
-- select * from t_Speech;
-- select * from t_TTS;


-- -- 비밀번호 암호화 : AES / MD5 / SHA / SHA2 

-- SELECT MD5('1234');        # 32글자 81dc9bdb52d04dc20036dbd8313ed055

-- SELECT SHA('1234');        # 40글자 7110eda4d09e062aa5e4a390b0a572ac0d2c0220

-- SELECT SHA2('1234', 224);  # 56글자 99fb2f48c6af4761f904fc85f95eb56190e5d40b1f44ec3a9c1fa319

-- SELECT SHA2('1234', 256);  # 64 글자 03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4

-- SELECT SHA2('1234', 384);  # 96글자 504f008c8fcf8b2ed5dfcde752fc5464ab8ba064215d9c5b5fc486af3d9ab8c81b14785180d2ad7cee1ab792ad44798c

-- SELECT SHA2('1234', 512);  # 128글자 d404559f602eab6fd602ac7680dacbfaadd13630335e951f097af3900e9de176b6db28512f2e000b9d04fba5133e8b1c6e8df59db3a8ab9d60be4b97cc9e81db

-- 테이블 순서는 관계를 고려하여 한 번에 실행해도 에러가 발생하지 않게 정렬되었습니다.

-- t_User Table Create SQL
-- 테이블 생성 SQL - t_User
CREATE TABLE t_User
(
    `user_Name`        VARCHAR(50)     NOT NULL    COMMENT 'user_Name', 
    `user_Id`          VARCHAR(50)     NOT NULL    COMMENT 'user_Id', 
    `user_Phone`       VARCHAR(50)     NOT NULL    COMMENT 'user_Phone', 
    `user_Pwd`         VARCHAR(50)     NOT NULL    COMMENT 'user_Pwd', 
    `user_Gender`      VARCHAR(50)     NOT NULL    COMMENT 'user_Gender', 
    `user_Disability`  VARCHAR(50)     NOT NULL    COMMENT 'user_Disability', 
    `user_Year`        INT             NOT NULL    COMMENT 'user_Year', 
    `user_Region`      VARCHAR(50)     NOT NULL    COMMENT 'user_Region', 
    `user_Phone1`      VARCHAR(50)     NOT NULL    COMMENT 'user_Phone1', 
    `user_Phone2`      VARCHAR(50)     NOT NULL    COMMENT 'user_Phone2', 
    `user_Phone3`      VARCHAR(50)     NOT NULL    COMMENT 'user_Phone3', 
    `user_Date`        DATE            NOT NULL    COMMENT 'user_Date', 
    `user_PostNumber`  VARCHAR(50)     NOT NULL    COMMENT 'user_PostNumber', 
    `user_Address`     VARCHAR(200)    NOT NULL    COMMENT 'user_Address', 
    `user_Details`     VARCHAR(200)    NOT NULL    COMMENT 'user_Details', 
     PRIMARY KEY (user_Id)
);

-- 테이블 Comment 설정 SQL - t_User
ALTER TABLE t_User COMMENT 'User';


-- t_Speech Table Create SQL
-- 테이블 생성 SQL - t_Speech
CREATE TABLE t_Speech
(
    `user_Id`        VARCHAR(50)     NOT NULL    COMMENT 'user_Id', 
    `speak_Id`       INT UNSIGNED    NOT NULL    AUTO_INCREMENT COMMENT 'speak_Id', 
    `speak_Content`  VARCHAR(50)     NULL        COMMENT 'speak_Content', 
     PRIMARY KEY (speak_Id)
);

-- 테이블 Comment 설정 SQL - t_Speech
ALTER TABLE t_Speech COMMENT 'Speech';

-- Foreign Key 설정 SQL - t_Speech(user_Id) -> t_User(user_Id)
ALTER TABLE t_Speech
    ADD CONSTRAINT FK_t_Speech_user_Id_t_User_user_Id FOREIGN KEY (user_Id)
        REFERENCES t_User (user_Id) ON DELETE RESTRICT ON UPDATE RESTRICT;

-- Foreign Key 삭제 SQL - t_Speech(user_Id)
-- ALTER TABLE t_Speech
-- DROP FOREIGN KEY FK_t_Speech_user_Id_t_User_user_Id;


-- t_TTS Table Create SQL
-- 테이블 생성 SQL - t_TTS
CREATE TABLE t_TTS
(
    `user_Id`       VARCHAR(50)      NOT NULL    COMMENT 'user_Id', 
    `speak_Id`      INT UNSIGNED     NOT NULL    COMMENT 'speak_Id', 
    `text_Id`       INT UNSIGNEd     NOT NULL    AUTO_INCREMENT COMMENT 'text_Id', 
    `text_Content`  VARCHAR(2000)    NULL        COMMENT 'text_Content', 
     PRIMARY KEY (text_Id)
);

-- 테이블 Comment 설정 SQL - t_TTS
ALTER TABLE t_TTS COMMENT 'TTS';

-- Foreign Key 설정 SQL - t_TTS(user_Id) -> t_User(user_Id)
ALTER TABLE t_TTS
    ADD CONSTRAINT FK_t_TTS_user_Id_t_User_user_Id FOREIGN KEY (user_Id)
        REFERENCES t_User (user_Id) ON DELETE RESTRICT ON UPDATE RESTRICT;

-- Foreign Key 삭제 SQL - t_TTS(user_Id)
-- ALTER TABLE t_TTS
-- DROP FOREIGN KEY FK_t_TTS_user_Id_t_User_user_Id;







INSERT INTO t_User (user_Name, user_Id, user_Phone, user_Pwd, user_Gender, user_Disability, user_Year, user_Region, user_Phone1, user_Phone2, user_Phone3, user_Date, user_PostNumber, user_Address, user_Details) 
VALUES ('김창렬', 'user_Id1', '01034567890', '1234', '남', '언어/청각장애', 1998, '부산', '010', '3456', '7890', '1998-03-01', '12345', '주소', '상세주소');

INSERT INTO t_User (user_Name, user_Id, user_Phone, user_Pwd, user_Gender, user_Disability, user_Year, user_Region, user_Phone1, user_Phone2, user_Phone3, user_Date, user_PostNumber, user_Address, user_Details) 
VALUES ('홍길동', 'user_Id2', '01012345678', '1234', '남', '언어/청각장애', 1997, '경북', '010', '1234', '5678', '1997-03-01', '12345', '주소', '상세주소');

INSERT INTO t_User (user_Name, user_Id, user_Phone, user_Pwd, user_Gender, user_Disability, user_Year, user_Region, user_Phone1, user_Phone2, user_Phone3, user_Date, user_PostNumber, user_Address, user_Details) 
VALUES ('김길동', 'user_Id3', '0102345678', '1234', '남', '언어/청각장애', 1998, '광주', '010', '2345', '6789', '1998-03-01', '12345', '주소', '상세주소');

insert INTO t_Speech(user_Id , speak_Content) values("user_Id1","adwkaodkawodawkd");

INSERT INTO t_TTS (user_Id, speak_Id, text_Content) VALUES ("user_Id1",5,"awdawdawd");

select * from t_User;
select * from t_Speech;
select * from t_TTS;