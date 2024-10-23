CREATE projects(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id INTEGER NOT NULL,
    lsp_name TEXT NOT NULL,
    account_name TEXT NOT NULL,
    project_name TEXT NOT NULL,
    date_time TIMESTAMP NOT NULL,
    task_type TEXT NOT NULL,
    new_words INTEGER NOT NULL,
    high_fuzzy INTEGER NOT NULL,
    low_fuzzy INTEGER NOT NULL,
    hundred_percent INTEGER NOT NULL,
    hourlywork INTEGER NOT NULL,
    weighted_words INTEGER NOT NULL,
    completed INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (lsp_name) REFERENCES lsps(lsp_name),
    FOREIGN KEY (account_name) REFERENCES accounts(account_name)
);