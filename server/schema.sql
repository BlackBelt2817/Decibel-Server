BEGIN TRANSACTION;

CREATE TABLE IF NOT EXISTS chats (
	_ID INTEGER PRIMARY KEY AUTOINCREMENT,
	user_ids TEXT NOT NULL,
	messages TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS comments (
	_ID	INTEGER PRIMARY KEY AUTOINCREMENT,
	parent_id	INTEGER,
	post_id	INTEGER NOT NULL,
	author_id	INTEGER NOT NULL,
	content	TEXT NOT NULL,
	likes	TEXT NOT NULL,
	dislikes	TEXT NOT NULL,
	tagged_friend_ids	TEXT NOT NULL,
	time_stamp	TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS cooljugator (
	_ID	INTEGER PRIMARY KEY AUTOINCREMENT,
	language_abbreviation	TEXT NOT NULL,
	infinitive_foreign	TEXT NOT NULL,
	infinitive_english	TEXT NOT NULL,
	translation_tables	TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS games (
	_ID	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	chat_id	INTEGER,
	game_name	TEXT NOT NULL,
	game_data	TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS groups (
	_ID	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	name	TEXT NOT NULL,
	user_ids	TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS playlists (
	_ID INTEGER PRIMARY KEY AUTOINCREMENT,
	username TEXT,
	song_id TEXT,
	artist TEXT,
	title TEXT,
	album TEXT,
	lyrics TEXT,
	extension TEXT,
	track TEXT
);

CREATE TABLE IF NOT EXISTS posts (
	_ID INTEGER PRIMARY KEY AUTOINCREMENT,
	author_id	INTEGER NOT NULL,
	post_content	TEXT NOT NULL,
	tagged_friend_ids	TEXT NOT NULL,
	likes	TEXT NOT NULL,
	dislikes	TEXT NOT NULL,
	time_stamp	TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS settings (
	_ID INTEGER PRIMARY KEY AUTOINCREMENT,
	setting_key TEXT,
	setting_value TEXT
);

CREATE TABLE IF NOT EXISTS songs (
	_ID INTEGER PRIMARY KEY AUTOINCREMENT,
	song_id TEXT,
	artist TEXT,
	title TEXT,
	album TEXT,
	lyrics TEXT,
	extension TEXT,
	track TEXT,
	file_downloaded INTEGER DEFAULT 0,
	record_verified INTEGER DEFAULT 0,
	lyrics_link TEXT);
	
CREATE TABLE IF NOT EXISTS trivia_questions (
	_ID INTEGER PRIMARY KEY AUTOINCREMENT,
	question_id TEXT,
	category TEXT,
	question TEXT,
	correct_answer TEXT,
	incorrect_answers TEXT,
	tags TEXT,
	question_type TEXT,
	difficulty TEXT,
	regions TEXT,
	is_niche INTEGER);

CREATE TABLE IF NOT EXISTS users (
	`_ID`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`email`	TEXT NOT NULL,
	`username`	TEXT NOT NULL,
	`password`	TEXT NOT NULL,
	`admin`	INTEGER DEFAULT 0,
	`first_name`	TEXT NOT NULL,
	`last_name`	TEXT NOT NULL,
	--`birth_year`	INTEGER NOT NULL DEFAULT 0,
	--`birth_month`	INTEGER NOT NULL DEFAULT 0,
	--`birth_day`	INTEGER NOT NULL DEFAULT 0,
	`friend_requests_outgoing`	TEXT NOT NULL,
	`friend_requests_incoming`	TEXT NOT NULL,
	`friends`	TEXT NOT NULL
);

COMMIT;
