class track:
    def __init__(self, url: str, filename: str, title: str = None, thumbnail: str = None, uploader: str = None, duration: int = None):
        self.url = url
        self.filename = filename
        self.title = title
        self.thumbnail = thumbnail
        self.uploader = uploader
        self.duration = duration
