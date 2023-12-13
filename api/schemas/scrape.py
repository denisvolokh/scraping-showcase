from marshmallow import Schema, fields


class ScrapeSchema(Schema):
    """Schema to represent a scrape result"""

    app_name = fields.Str()
    app_version = fields.Str()
    app_description = fields.Str()
    no_downloads = fields.Str()
    app_url = fields.Str()
    app_release_date = fields.Str()


class ScrapeResultSchema(Schema):
    """Schema to represent a result of a scrape request"""

    target_url = fields.Str()
    result = fields.Nested(ScrapeSchema)
    error = fields.Str()


class AsyncScrapeResultSchema(ScrapeResultSchema):
    """Schema to represent a result of an asynchronous scrape request"""

    task_id = fields.Str()
    status = fields.Str()
