-- tinkoff_game."_location" definition

-- Drop table

-- DROP TABLE tinkoff_game."_location";

CREATE TABLE tinkoff_game."_location" (
	location_rk int4 NULL,
	partner_rk int4 NULL,
	city_nm text NULL,
	metro_nm text NULL
);


-- tinkoff_game.account definition

-- Drop table

-- DROP TABLE tinkoff_game.account;

CREATE TABLE tinkoff_game.account (
	account_rk int4 NULL,
	client_rk int4 NULL,
	registration_dttm time NULL,
	login text NULL,
	"password" text NULL,
	email text NULL
);


-- tinkoff_game.application definition

-- Drop table

-- DROP TABLE tinkoff_game.application;

CREATE TABLE tinkoff_game.application (
	application_rk int4 NULL,
	account_rk int4 NULL,
	game_rk int4 NULL,
	application_dttm time NULL
);


-- tinkoff_game.client definition

-- Drop table

-- DROP TABLE tinkoff_game.client;

CREATE TABLE tinkoff_game.client (
	client_rk int4 NULL,
	first_name text NULL,
	last_name text NULL,
	phone_num text NULL,
	visit_dttm timestamp NULL
);


-- tinkoff_game.employee definition

-- Drop table

-- DROP TABLE tinkoff_game.employee;

CREATE TABLE tinkoff_game.employee (
	employee_rk int4 NULL,
	first_name text NULL,
	last_name text NULL,
	gender_cd varchar(1) NULL
);


-- tinkoff_game.game definition

-- Drop table

-- DROP TABLE tinkoff_game.game;

CREATE TABLE tinkoff_game.game (
	game_rk int4 NULL,
	quest_rk int4 NULL,
	employee_rk int4 NULL,
	game_dttm time NULL,
	price float4 NULL,
	game_flg int4 NULL,
	finish_flg int4 NULL,
	"time" time NULL
);


-- tinkoff_game.legend definition

-- Drop table

-- DROP TABLE tinkoff_game.legend;

CREATE TABLE tinkoff_game.legend (
	legend_rk int4 NULL,
	partner_rk int4 NULL,
	legend_nm text NULL,
	complexity int4 NULL
);


-- tinkoff_game.partner definition

-- Drop table

-- DROP TABLE tinkoff_game.partner;

CREATE TABLE tinkoff_game.partner (
	partner_rk int4 NULL,
	partner_nm text NULL
);


-- tinkoff_game.quest definition

-- Drop table

-- DROP TABLE tinkoff_game.quest;

CREATE TABLE tinkoff_game.quest (
	quest_rk int4 NULL,
	legend_rk int4 NULL,
	location_rk int4 NULL,
	quest_nm text NULL
);