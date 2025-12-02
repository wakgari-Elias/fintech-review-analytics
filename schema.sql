-- SQLBook: Code
CREATE TABLE banks (
    bank_id SERIAL PRIMARY KEY,
    bank_name VARCHAR(100) NOT NULL,
    app_name VARCHAR(100)
);

CREATE TABLE reviews (
    review_id SERIAL PRIMARY KEY,
    bank_id INT REFERENCES banks(bank_id),
    review_text TEXT,
    rating INT,
    review_date DATE,
    sentiment_label VARCHAR(20),
    sentiment_score FLOAT,
    source VARCHAR(50)
);
INSERT INTO banks (bank_name, app_name)
VALUES 
('Commercial Bank of Ethiopia', 'CBE Mobile Banking'),
('Bank of Abyssinia', 'BOA Mobile Banking'),
('Dashen Bank', 'Dashen Mobile Banking');

ALTER TABLE banks
ADD CONSTRAINT unique_bank_name UNIQUE (bank_name);

SELECT bank_id, COUNT(*) 
FROM reviews 
GROUP BY bank_id;

SELECT COUNT(*) FROM reviews;
SELECT bank_id, COUNT(*) FROM reviews GROUP BY bank_id;

SELECT * FROM banks;

SELECT * FROM reviews LIMIT 10;
--Count number of reviews per bank
SELECT b.bank_name, COUNT(r.review_id) AS total_reviews
FROM banks b
LEFT JOIN reviews r ON b.bank_id = r.bank_id
GROUP BY b.bank_name
ORDER BY total_reviews DESC;

--Average rating per bank
SELECT b.bank_name, ROUND(AVG(r.rating), 2) AS avg_rating
FROM banks b
LEFT JOIN reviews r ON b.bank_id = r.bank_id
GROUP BY b.bank_name;


--Count of positive, negative, and neutral sentiments per bank
SELECT b.bank_name, r.sentiment_label, COUNT(*) AS sentiment_count
FROM banks b
LEFT JOIN reviews r ON b.bank_id = r.bank_id
GROUP BY b.bank_name, r.sentiment_label
ORDER BY b.bank_name, sentiment_count DESC;


--Check for missing review text or ratings
SELECT *
FROM reviews
WHERE review_text IS NULL OR rating IS NULL;

--Count reviews by source
SELECT source, COUNT(*) AS total_reviews
FROM reviews
GROUP BY source;

--Check for duplicate reviews
SELECT review_text, COUNT(*) AS dup_count
FROM reviews
GROUP BY review_text
HAVING COUNT(*) > 1;
--Check for duplicate reviews
SELECT review_text, COUNT(*) AS dup_count
FROM reviews
GROUP BY review_text
HAVING COUNT(*) > 2;


