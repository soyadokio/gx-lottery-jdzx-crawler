from dataclasses import dataclass

@dataclass
class Article:
    title: str
    link: str
    date: str

    def __str__(self) -> str:
        return f'{self.date} {self.title} {self.link}'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Article):
            return self.title == obj.title and self.link == obj.link and self.date == obj.date
        return False

    def __hash__(self):
        return hash((self.title, self.link, self.date))
