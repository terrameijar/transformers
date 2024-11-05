import csv
from flask import Flask
from flask.cli import with_appcontext
import click
from models import Transformer, db

# csv_file_path = 'data/transformers-with-descriptions-cleaned.csv'
csv_file_path = "data/transformers.csv"


@click.command(name="populate_db")
@with_appcontext
def populate_database():
    with open(csv_file_path, mode="r", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            transformer = Transformer(
                name=row["Name"],
                affiliation=row["Affiliation"],
                abilities=row["Abilities"],
                transformation_mode=row["Transformation/Alternate Mode"],
                image_url=row["Image URL"],
                description=row["Description"],
                quote=row["Quote"],
            )
            db.session.add(transformer)
        db.session.commit()

    print("Transformers data populated into database")


@click.command(name="delete_duplicates")
@with_appcontext
def delete_duplicates():
    # Step 1: Identify duplicates
    duplicates = (
        db.session.query(Transformer.name, db.func.count(Transformer.id).label("count"))
        .group_by(Transformer.name)
        .having(db.func.count(Transformer.id) > 1)
        .all()
    )

    # Step 2: Delete duplicates
    for name, count in duplicates:
        transformers = Transformer.query.filter_by(name=name).all()
        # Keep the first entry and delete the rest
        for transformer in transformers[1:]:
            print(f"Deleting {transformer}")
            db.session.delete(transformer)

    db.session.commit()
    print("Duplicates deleted successfully.")


# Add the command to the CLI
