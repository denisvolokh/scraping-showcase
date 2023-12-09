from marshmallow import Schema, fields


class ResultItemSchema(Schema):
    app_name = fields.Str()
    app_version = fields.Str()
    app_description = fields.Str()
    no_downloads = fields.Int()
    app_url = fields.Str()
    app_release_date = fields.Str()


class SearchResultSchema(Schema):
    query = fields.Str()
    results = fields.List(fields.Nested(ResultItemSchema))
    error = fields.Str()
