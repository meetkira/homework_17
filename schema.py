from marshmallow import Schema, fields


class DirectorShema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


class GenreShema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


class MovieShema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    genre_id = fields.Int()
    genre = fields.Nested(GenreShema)
    director_id = fields.Int()
    director = fields.Nested(DirectorShema)
