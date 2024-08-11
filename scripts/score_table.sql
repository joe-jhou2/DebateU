CREATE TABLE scores (
    university1 VARCHAR(255),
    university2 VARCHAR(255),
    topic VARCHAR(255),
    score1 INT,
    score2 INT
);

CREATE INDEX idx_topic_name ON scores(topic);
CREATE INDEX idx_university_name ON university(name);
CREATE INDEX idx_keyword_name ON keyword(name);
ALTER TABLE scores ADD FOREIGN KEY (university1) REFERENCES university(name);
ALTER TABLE scores ADD FOREIGN KEY (university2) REFERENCES university(name);
ALTER TABLE scores ADD FOREIGN KEY (topic) REFERENCES keyword(name);
