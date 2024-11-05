import csv
from io import StringIO

from flask import Flask, jsonify, render_template, request, redirect, url_for, Response
from flask_migrate import Migrate

from models import db, Transformer
from config import Config
from commands import populate_database, delete_duplicates


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()

app.cli.add_command(populate_database)
app.cli.add_command(delete_duplicates)


# API Endpoints
@app.route("/api/transformers/<name>")
def get_transformer(name):
    decoded_name = name.replace("%20", " ")
    transformer = (
        db.session.execute(db.select(Transformer).filter_by(name=decoded_name))
        .scalars()
        .first()
    )
    if transformer:
        return jsonify(
            {
                "name": transformer.name,
                "affiliation": transformer.affiliation,
                "abilities": transformer.abilities,
                "transformation_mode": transformer.transformation_mode,
                "image_url": transformer.image_url,
                "description": transformer.description,
                "quote": transformer.quote,
                "id": transformer.id,
            }
        )
    else:
        return jsonify({"error": "Transformer not found"}), 404


@app.route("/api/transformers", methods=["GET"])
def get_transformers():
    """
    Retrieve a paginated list of Transformers (filter by name or affiliation)
    """
    name = request.args.get("name")
    affiliation = request.args.get("affiliation")
    page = request.args.get("page", 1, type=int)

    query = Transformer.query
    if name:
        query = query.filter(Transformer.name.ilike(f"%{name}%"))
    if affiliation:
        query = query.filter(Transformer.affiliation.ilike(f"%{affiliation}%"))

    transformers = query.paginate(page=page)

    return jsonify(
        {
            "transformers": [
                {
                    "name": bot.name,
                    "affiliation": bot.affiliation,
                    "abilities": bot.abilities,
                    "transformation_mode": bot.transformation_mode,
                    "image_url": bot.image_url,
                    "description": bot.description,
                    "quote": bot.quote,
                    "id": bot.id,
                }
                for bot in transformers.items
            ],
            "total_pages": transformers.pages,
            "page": transformers.page,
        }
    )


@app.route("/api/transformers/no-image", methods=["GET"])
def get_transformers_without_images():
    """Retrieve a list of transformers without images"""

    transformers = Transformer.query.filter(
        (Transformer.image_url == None) | (Transformer.image_url == "")
    ).all()

    return jsonify(
        {
            "transformers": [
                {
                    "name": bot.name,
                    "affiliation": bot.affiliation,
                    "abilities": bot.abilities,
                    "transformation_mode": bot.transformation_mode,
                    "description": bot.description,
                    "quote": bot.quote,
                    "id": bot.id,
                }
                for bot in transformers
            ]
        }
    )


@app.route("/api/transformers/export", methods=["GET"])
def export_transformers():
    transformers = Transformer.query.all()
    str_io = StringIO()
    csv_writer = csv.writer(str_io)

    # Write CSV header
    csv_writer.writerow(
        [
            "Name",
            "Affiliation",
            "Abilities",
            "Transformation/Alternate Mode",
            "Image URL",
            "Description",
            "Quote",
        ]
    )

    for transformer in transformers:
        csv_writer.writerow(
            [
                transformer.name,
                transformer.affiliation,
                transformer.abilities,
                transformer.transformation_mode,
                transformer.image_url,
                transformer.description,
                transformer.quote,
            ]
        )

    str_io.seek(0)

    # Create response
    response = Response(str_io.getvalue(), mimetype="text/csv")
    response.headers["Content-Disposition"] = (
        "attachment; filename=transformers_export.csv"
    )
    return response


# HTML Views (User Facing Pages)


@app.route("/")
def list_all_transformers():
    """
    View Paginated list of Transformers
    """
    return render_template("index.html")


@app.route("/transformers/<name>")
def view_transformer(name):
    """
    View details of a Transformer using its name
    """
    return render_template("view.html", name=name)


@app.route("/transformers/edit/<int:id>", methods=["GET", "POST"])
def edit_transformer(id):
    transformer = Transformer.query.get_or_404(id)
    if request.method == "POST":
        transformer.name = request.form["name"]
        transformer.affiliation = request.form["affiliation"]
        transformer.abilities = request.form["abilities"]
        transformer.transformation_mode = request.form["transformation_mode"]
        transformer.image_url = request.form["image_url"]
        transformer.description = request.form["description"]
        transformer.quote = request.form["quote"]
        db.session.commit()
        return redirect(url_for("list_all_transformers"))
    return render_template("edit.html", transformer=transformer)


if __name__ == "__main__":
    app.run(debug=True)
