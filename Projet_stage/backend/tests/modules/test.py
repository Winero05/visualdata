# import os
# import json
# import sqlite3
# import yaml
# import pandas as pd
# import numpy as np
# from pathlib import Path
# from packages.modules.loading import DataLoader  # <- votre fichier où la classe est définie

# def test_csv(tmp_path):
#     file = tmp_path / "data.csv"
#     file.write_text("col1;col2\n1;2\n3;4")
#     loader = DataLoader()
#     df = loader.load_file(file)
#     assert isinstance(df, pd.DataFrame)
#     assert list(df.columns) == ["col1", "col2"]

# def test_excel(tmp_path):
#     file = tmp_path / "data.xlsx"
#     df = pd.DataFrame({"a":[1,2], "b":[3,4]})
#     df.to_excel(file, index=False)
#     loader = DataLoader()
#     out = loader.load_file(file)
#     assert out.equals(df)

# def test_json(tmp_path):
#     file = tmp_path / "data.json"
#     data = [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]
#     file.write_text(json.dumps(data))
#     loader = DataLoader()
#     df = loader.load_file(file)
#     assert "name" in df.columns and "age" in df.columns

# def test_yaml(tmp_path):
#     file = tmp_path / "data.yaml"
#     data = {"users": [{"name": "Alice"}, {"name": "Bob"}]}
#     file.write_text(yaml.dump(data))
#     loader = DataLoader()
#     df = loader.load_file(file)
#     assert "users" in df.columns or "name" in df.columns

# def test_parquet(tmp_path):
#     file = tmp_path / "data.parquet"
#     df = pd.DataFrame({"x": [1,2,3]})
#     df.to_parquet(file)
#     loader = DataLoader()
#     out = loader.load_file(file)
#     assert out.equals(df)

# def test_sql(tmp_path):
#     db = tmp_path / "test.db"
#     with sqlite3.connect(db) as conn:
#         conn.execute("CREATE TABLE users(id INTEGER, name TEXT);")
#         conn.execute("INSERT INTO users VALUES (1, 'Alice'), (2, 'Bob');")
#     loader = DataLoader()
#     df = loader.load_file("fake.sql", file_type="sql", db_path=db, sql_query="SELECT * FROM users")
#     assert list(df.columns) == ["id", "name"]

# def test_image(tmp_path):
#     from PIL import Image
#     file = tmp_path / "test.png"
#     img = Image.new("RGB", (2,2), color=(255,0,0))
#     img.save(file)
#     loader = DataLoader()
#     df = loader.load_file(file, image_as_dataframe=True)
#     assert "R" in df.columns and "G" in df.columns and "B" in df.columns

# def test_text(tmp_path):
#     file = tmp_path / "doc.txt"
#     file.write_text("Hello world")
#     loader = DataLoader()
#     text = loader.load_file(file)
#     assert isinstance(text, str)
#     assert "Hello" in text
