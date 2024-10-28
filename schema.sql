CREATE TABLE users
(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
username TEXT NOT NULL,
hash TEXT NOT NULL
);

CREATE TABLE lsps
(user_id INTEGER,
lsp_name TEXT,
PRIMARY KEY (user_id, lsp_name),
FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE accounts
(user_id INTEGER,
account_name TEXT,
PRIMARY KEY (user_id, account_name),
FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE projects
(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
user_id INTEGER,
lsp_name TEXT,
account_name TEXT,
project_name TEXT,
date_time TIMESTAMP,
task_type TEXT,
new_words INTEGER,
high_fuzzy INTEGER,
low_fuzzy INTEGER,
hundred_percent INTEGER,
hourlywork INTEGER,
weighted_words INTEGER,
completed INTEGER NOT NULL,
FOREIGN KEY (user_id) REFERENCES users(id),
FOREIGN KEY (user_id, lsp_name) REFERENCES lsps(user_id, lsp_name),
FOREIGN KEY (user_id, account_name) REFERENCES accounts(user_id, account_name)
);