class Song:
    def __init__(self, title, url, counter, date):
        self.title: str = title
        self.url: str = url
        self.counter: int = counter
        self.date: str = date  # date.today().strftime("%d/%m/%Y")
