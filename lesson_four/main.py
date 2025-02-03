
class Book:
    def __init__(self, title, author, year,):
        self.title = title
        self.autgor = author
        self.year = year

    def __repr__(self) -> str:
        return f"Book (title={self.title}, author={self.autgor}, year={self.year})"




