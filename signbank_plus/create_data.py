"""This is a utility file to extract the data from the database and create csv files for the data."""
import os
import csv
from pathlib import Path

import psycopg2
from dotenv import load_dotenv
from signwriting.formats.swu_to_fsw import swu2fsw

load_dotenv()

connection = psycopg2.connect(
    dbname=os.environ.get("DB_NAME"),
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASS"),
    host=os.environ.get("DB_HOST"),
    port=os.environ.get("DB_PORT"),
)
cursor = connection.cursor()


def query(sql):
    cursor.execute(sql)
    columns = list(cursor.description)
    columns = [c.name for c in columns]

    rows = [{c: v for c, v in zip(columns, instance)} for instance in cursor.fetchall()]
    return rows


def save_data_csv(name: str, sql: str, process=None):
    print("Saving", name)
    rows = query(sql)
    columns = list(rows[0].keys())
    if "sign_writing_swu" in columns:
        columns[columns.index("sign_writing_swu")] = "sign_writing"
    print("Rows:", len(rows), columns)

    csv_path = Path(__file__).parent.parent / "data" / f"{name}.csv"
    with open(csv_path, "w", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(columns)
        for row in rows:
            if "sign_writing_swu" in row:
                row["sign_writing"] = swu2fsw(row["sign_writing_swu"])
                del row["sign_writing_swu"]

            if process is not None:
                process(row)

            for key in columns:
                # join lists to strings
                if isinstance(row[key], list):
                    row[key] = "᛫".join(row[key])
                if isinstance(row[key], str):
                    row[key] = row[key].replace("\n", "\\n")  # Replacing newlines with \n escape sequence
            writer.writerow([row[key] for key in columns])


def captions_sql(dataset_id: str, country: str):
    return f"""
    SELECT c1."videoLanguage" as sign_language,
        c1.language as spoken_language,
        '{country}' as country_code,
        c1.text as texts,
    string_agg(c2.text, ' ' ORDER BY c2.start) as sign_writing_swu
    FROM captions c1 INNER JOIN captions c2
        ON c1."videoId" = c2."videoId" AND c1.language != 'Sgnw' AND c2.language = 'Sgnw'
    WHERE c2.start <= c1.end
        AND c2.end >= c1.start
        AND c1."videoId" LIKE '{dataset_id}%'
    GROUP BY c1."videoId", c1."videoLanguage", c1.language, c1.text
    """


def capitalize_texts(row):
    row["texts"] = row["texts"].capitalize()


if __name__ == "__main__":
    save_data_csv("benchmark", "SELECT * FROM signbank_prompting ORDER BY puddle_id")

    save_data_csv("raw", """
        SELECT puddle_id, example_id, spoken_language, country_code, sign_language,
    user, created_date, modified_date, sign_writing, texts FROM signbank
    ORDER BY puddle_id, example_id
    """)

    save_data_csv("manually-cleaned", """
    SELECT puddle_id, example_id, gold_texts as annotated_texts
    FROM signbank WHERE gold_texts IS NOT NULL AND puddle_id NOT IN (151, 152)
    ORDER BY puddle_id, example_id
    """)

    save_data_csv("bible", """
    SELECT puddle_id, example_id, gold_texts as annotated_texts
    FROM signbank WHERE gold_texts IS NOT NULL AND puddle_id IN (151, 152)
    ORDER BY puddle_id, example_id
    """)

    save_data_csv("gpt-3.5-cleaned", """
    SELECT puddle_id, example_id, pred_general_specific_5 as annotated_texts
    FROM signbank WHERE pred_general_specific_5 IS NOT NULL
    ORDER BY puddle_id, example_id
    """)

    save_data_csv("gpt-3.5-expanded", """
    SELECT puddle_id, example_id, expanded_texts as annotated_texts
    FROM signbank WHERE expanded_texts IS NOT NULL
    ORDER BY puddle_id, example_id
    """)

    save_data_csv("gpt-3.5-expanded.en", """
    SELECT puddle_id, example_id, 'en' as spoken_language, country_code, sign_language,
           sign_writing, expanded_texts_en as annotated_texts
    FROM signbank WHERE expanded_texts_en IS NOT NULL AND array_length(expanded_texts_en, 1) > 0
    ORDER BY puddle_id, example_id
    """)

    save_data_csv("sign2mint", captions_sql("s2m", "de"))
    save_data_csv("signsuisse", captions_sql("ss", "ch"), process=capitalize_texts)
