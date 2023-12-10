from marshmallow import Schema, fields


class ScrapeSchema(Schema):
    app_name = fields.Str()
    app_version = fields.Str()
    app_description = fields.Str()
    no_downloads = fields.Str()
    app_url = fields.Str()
    app_release_date = fields.Str()


class ScrapeResultSchema(Schema):
    target_url = fields.Str()
    result = fields.Nested(ScrapeSchema)
    error = fields.Str()
