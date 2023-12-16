# Производители микросхем и микросхемы

Технологии:
- Python + FastAPI
- SQLite
- SQLAlchemy
- https://github.com/vinibiavatti1/TuiCss

# База
```
CREATE TABLE Circuits (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    created_at DATE,
    frequency NUMERIC(10, 3)
    manufacturer_id INT,
    FOREIGN KEY (manufacturer_id) REFERENCES Manufacturers(id)
);

CREATE TABLE circuits (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    created_at DATE,
    revenue INT
);
```
