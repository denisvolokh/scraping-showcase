import falcon
from falcon import Request, Response


class StaticFileHandler:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def on_get(self, req: Request, resp: Response) -> None:
        resp.content_type = falcon.MEDIA_TEXT  # Set appropriate content type
        with open(self.file_path, "rb") as f:
            resp.body = f.read()
