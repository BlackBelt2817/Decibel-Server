BEGIN TRANSACTION;



CREATE TABLE IF NOT EXISTS users (
	`_ID`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`email`	TEXT,
	`username`	TEXT,
	`password`	TEXT,
	`admin`	INTEGER DEFAULT 0
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

CREATE TABLE IF NOT EXISTS settings (
	_ID INTEGER PRIMARY KEY AUTOINCREMENT,
	setting_key TEXT,
	setting_value TEXT
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



COMMIT;
