/*
 Navicat Premium Data Transfer

 Source Server         : 本地数据库
 Source Server Type    : MySQL
 Source Server Version : 80020 (8.0.20)
 Source Host           : localhost:3306
 Source Schema         : booksale

 Target Server Type    : MySQL
 Target Server Version : 80020 (8.0.20)
 File Encoding         : 65001

 Date: 24/12/2024 18:59:38
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for book_shop
-- ----------------------------
DROP TABLE IF EXISTS `book_shop`;
CREATE TABLE `book_shop`  (
  `book_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `price` int NOT NULL COMMENT '价格',
  `m_sale_v` int NOT NULL COMMENT '库存',
  PRIMARY KEY (`book_name`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of book_shop
-- ----------------------------
INSERT INTO `book_shop` VALUES ('C语言程序设计', 20, 100);
INSERT INTO `book_shop` VALUES ('人工智能导论', 10, 100);
INSERT INTO `book_shop` VALUES ('大学物理', 15, 100);
INSERT INTO `book_shop` VALUES ('大学生职业生涯规划', 5, 100);
INSERT INTO `book_shop` VALUES ('数学建模理论与方法', 8, 100);
INSERT INTO `book_shop` VALUES ('机器学习', 20, 100);
INSERT INTO `book_shop` VALUES ('深度学习的数学', 10, 100);
INSERT INTO `book_shop` VALUES ('离散数学', 10, 100);
INSERT INTO `book_shop` VALUES ('计算机网络', 15, 100);
INSERT INTO `book_shop` VALUES ('高等数学(上)', 10, 100);
INSERT INTO `book_shop` VALUES ('高等数学(下)', 10, 100);

-- ----------------------------
-- Table structure for dispatcher
-- ----------------------------
DROP TABLE IF EXISTS `dispatcher`;
CREATE TABLE `dispatcher`  (
  `dispatcher_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `dispatcher_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `dispatcher_phone` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`dispatcher_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of dispatcher
-- ----------------------------
INSERT INTO `dispatcher` VALUES ('010100', '1', '13365789765');
INSERT INTO `dispatcher` VALUES ('010101', '2', '15826432363');
INSERT INTO `dispatcher` VALUES ('010102', '小黑', '19926432361');
INSERT INTO `dispatcher` VALUES ('010103', '小白', '19926432363');
INSERT INTO `dispatcher` VALUES ('010104', '小绿', '19926432365');

-- ----------------------------
-- Table structure for oorder
-- ----------------------------
DROP TABLE IF EXISTS `oorder`;
CREATE TABLE `oorder`  (
  `order_id` int NOT NULL AUTO_INCREMENT,
  `book_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `order_way` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `cons_phone` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `cons_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `cons_addre` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `checked` int NULL DEFAULT 0,
  `create_time` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`order_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of oorder
-- ----------------------------
INSERT INTO `oorder` VALUES (1, '大学物理', '自提', '15826432361', 'dsw', 'cqDWEVG', 2, '2024-12-23 20:17:10');
INSERT INTO `oorder` VALUES (2, '机器学习', '配送', '15826432361', 'dsw', 'zrhzezt', 2, '2024-12-23 20:18:19');
INSERT INTO `oorder` VALUES (3, '离散数学', '配送', '15826432361', 'd\'d', 'awuvciser', 1, '2024-12-23 21:55:44');
INSERT INTO `oorder` VALUES (4, '计算机网络', '自提', '15826432361', 'djw', '明志苑1舍', 1, '2024-12-23 22:04:59');
INSERT INTO `oorder` VALUES (5, '机器学习', '配送', '15826432361', '3333', '1223', 1, '2024-12-23 23:01:00');
INSERT INTO `oorder` VALUES (6, '人工智能导论', '自提', '15826432361', 'd', 'acVfz', 1, '2024-12-23 23:28:16');
INSERT INTO `oorder` VALUES (7, '深度学习的数学', '自提', '15826432361', 'd\'d\'f', 'vdaebrgtw', 1, '2024-12-23 23:31:41');

-- ----------------------------
-- Table structure for orderway
-- ----------------------------
DROP TABLE IF EXISTS `orderway`;
CREATE TABLE `orderway`  (
  `orderway_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `count` int NOT NULL,
  PRIMARY KEY (`orderway_name`) USING BTREE,
  UNIQUE INDEX `orderway_name`(`orderway_name` ASC) USING BTREE,
  INDEX `count`(`count` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of orderway
-- ----------------------------
INSERT INTO `orderway` VALUES ('自提', 9);
INSERT INTO `orderway` VALUES ('配送', 10);

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `username` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `password` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `telephone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `role` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES (1, 'dsw', '123456', '15826432361', 0);
INSERT INTO `user` VALUES (2, 'djw', '123456', '15826432362', 1);

-- ----------------------------
-- Table structure for user_msg
-- ----------------------------
DROP TABLE IF EXISTS `user_msg`;
CREATE TABLE `user_msg`  (
  `id` int UNSIGNED NOT NULL,
  `real_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `sex` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `age` int NOT NULL,
  `mail` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `phone` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `user_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`phone`) USING BTREE,
  INDEX `userid`(`id` ASC) USING BTREE,
  CONSTRAINT `userid` FOREIGN KEY (`id`) REFERENCES `user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user_msg
-- ----------------------------
INSERT INTO `user_msg` VALUES (1, 'dsw', '女', 20, '2499157529@qq.com', '15826432361', 'dsw');
INSERT INTO `user_msg` VALUES (2, 'djw', '女', 20, '2499157528@qq.com', '15826432362', 'djw');

-- ----------------------------
-- Table structure for wuliu
-- ----------------------------
DROP TABLE IF EXISTS `wuliu`;
CREATE TABLE `wuliu`  (
  `order_id` int NOT NULL,
  `cons_phone` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `disp_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `deliver_time` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `ended` int NOT NULL DEFAULT 0,
  PRIMARY KEY (`order_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of wuliu
-- ----------------------------
INSERT INTO `wuliu` VALUES (1, '15826432361', '010100', '20分钟', 1);
INSERT INTO `wuliu` VALUES (2, '15826432361', '010100', '18分', 1);
INSERT INTO `wuliu` VALUES (3, '15826432361', '010100', '22', 0);
INSERT INTO `wuliu` VALUES (4, '15826432361', '010101', '23', 0);
INSERT INTO `wuliu` VALUES (5, '15826432361', '010102', '16分钟', 0);
INSERT INTO `wuliu` VALUES (6, '15826432361', '010103', '26', 0);
INSERT INTO `wuliu` VALUES (7, '15826432361', '010103', '28', 0);

-- ----------------------------
-- View structure for sended_order
-- ----------------------------
DROP VIEW IF EXISTS `sended_order`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `sended_order` AS select `oorder`.`order_id` AS `order_id`,`oorder`.`book_name` AS `book_name`,`oorder`.`order_way` AS `order_way`,`oorder`.`cons_phone` AS `cons_phone`,`oorder`.`cons_name` AS `cons_name`,`oorder`.`cons_addre` AS `cons_addre`,`wuliu`.`disp_id` AS `disp_id`,`wuliu`.`deliver_time` AS `deliver_time`,`dispatcher`.`dispatcher_phone` AS `dispatcher_phone` from ((`oorder` join `wuliu` on((`oorder`.`order_id` = `wuliu`.`order_id`))) join `dispatcher` on((`wuliu`.`disp_id` = `dispatcher`.`dispatcher_id`))) where (`oorder`.`checked` = 2);

-- ----------------------------
-- View structure for sending_order
-- ----------------------------
DROP VIEW IF EXISTS `sending_order`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `sending_order` AS select `oorder`.`order_id` AS `order_id`,`oorder`.`book_name` AS `book_name`,`oorder`.`order_way` AS `order_way`,`oorder`.`cons_phone` AS `cons_phone`,`oorder`.`cons_name` AS `cons_name`,`oorder`.`cons_addre` AS `cons_addre`,`wuliu`.`disp_id` AS `disp_id`,`wuliu`.`deliver_time` AS `deliver_time`,`dispatcher`.`dispatcher_phone` AS `dispatcher_phone` from ((`oorder` join `wuliu` on((`oorder`.`order_id` = `wuliu`.`order_id`))) join `dispatcher` on((`wuliu`.`disp_id` = `dispatcher`.`dispatcher_id`))) where (`oorder`.`checked` = 1);

SET FOREIGN_KEY_CHECKS = 1;
