CREATE TABLE `scoringsystem_business` (
`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, 
`business_id` varchar(22) NOT NULL UNIQUE, 
`business_name` varchar(100) NOT NULL, 
`business_address` varchar(100) NOT NULL, 
`business_city` varchar(100) NOT NULL, 
`business_state` varchar(100) NOT NULL, 
`business_postal_code` varchar(20)NOT NULL, 
`business_lat` double precision NOT NULL, 
`business_long` double precision NOT NULL, 
`business_stars` double precision NOT NULL, 
`business_review_count` integer NOT NULL, 
`business_mon` varchar(20) NOT NULL, 
`business_tue` varchar(20) NOT NULL, 
`business_wed` varchar(20) NOT NULL, 
`business_thu` varchar(20) NOT NULL, 
`business_fri` varchar(20) NOT NULL, 
`business_sat` varchar(20) NOT NULL, 
`business_sun` varchar(20) NOT NULL);


CREATE TABLE `scoringsystem_review` (
`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, 
`review_stars` double precision NOT NULL, 
`review_text` longtext NOT NULL, 
`review_date` datetime(6) NOT NULL, 
`review_useful_vote` integer NOT NULL, 
`review_funny_vote` integer NOT NULL, 
`review_cool_vote` integer NOT NULL, 
`review_business_id_id` integer NOT NULL, 
`review_user_id_id` integer NOT NULL);


CREATE TABLE `scoringsystem_vote` (
`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, 
`vote_option` integer NOT NULL, 
`vote_review_id` integer NOT NULL, 
`vote_user_id` integer NOT NULL);

CREATE TABLE `scoringsystem_tip` (
`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, 
`tip_text` varchar(100) NOT NULL, 
`tip_date` date NOT NULL, 
`tip_business_id_id` integer NOT NULL, 
`tip_user_id_id` integer NOT NULL);

CREATE TABLE `scoringsystem_photo` (
`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, 
`photo_caption` varchar(100) NOT NULL, 
`photo_label` varchar(100) NOT NULL, 
`photo_image` varchar(250) NOT NULL, 
`photo_business_id_id` integer NOT NULL);

ALTER TABLE `scoringsystem_review` ADD CONSTRAINT `scoringsystem_review_review_business_id_i_d140ea9a_fk_scoringsy` FOREIGN KEY (`review_business_id_id`) REFERENCE
S `scoringsystem_business` (`id`);
ALTER TABLE `scoringsystem_review` ADD CONSTRAINT `scoringsystem_review_review_user_id_id_e4d104a2_fk_login_use` FOREIGN KEY (`review_user_id_id`) REFERENCES `logi
n_userprofile` (`id`);
ALTER TABLE `scoringsystem_vote` ADD CONSTRAINT `scoringsystem_vote_vote_review_id_99c24bd6_fk_scoringsy` FOREIGN KEY (`vote_review_id`) REFERENCES `scoringsystem_
review` (`id`);
ALTER TABLE `scoringsystem_vote` ADD CONSTRAINT `scoringsystem_vote_vote_user_id_2adb2b85_fk_login_userprofile_id` FOREIGN KEY (`vote_user_id`) REFERENCES `login_u
serprofile` (`id`);
ALTER TABLE `scoringsystem_tip` ADD CONSTRAINT `scoringsystem_tip_tip_business_id_id_0e36de7e_fk_scoringsy` FOREIGN KEY (`tip_business_id_id`) REFERENCES `scorings
ystem_business` (`id`);
ALTER TABLE `scoringsystem_tip` ADD CONSTRAINT `scoringsystem_tip_tip_user_id_id_cc48fb53_fk_login_use` FOREIGN KEY (`tip_user_id_id`) REFERENCES `login_userprofil
e` (`id`);
ALTER TABLE `scoringsystem_photo` ADD CONSTRAINT `scoringsystem_photo_photo_business_id_id_6b30974c_fk_scoringsy` FOREIGN KEY (`photo_business_id_id`) REFERENCES `scoringsystem_business` (`id`);