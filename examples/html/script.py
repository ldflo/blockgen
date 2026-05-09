import blockgen
import csv
from functools import cache
import html

class HtmlUtils:
    @cache
    def read_csv(self) -> tuple[list[str], list[list[str]]]:
        with open("./data.csv") as f:
            reader = csv.reader(f)
            rows = list(reader)
        return rows[0], rows[1:] # headers, data_rows

    @blockgen.callback("headers")
    def headers_callback(self):
        # Step 1: Read the CSV file
        headers, _ = self.read_csv()

        # Step 2: Generate the <th> elements
        result = ""
        for h in headers:
            result += f"<th>{html.escape(h)}</th>\n"
        return result[:-1] # Strip trailing newline

    @blockgen.callback("rows")
    def rows_callback(self):
        # Step 1: Read the CSV file
        _, data_rows = self.read_csv()

        # Step 2: Generate the <tr> elements
        result = ""
        for row in data_rows:
            cells = "".join(f"<td>{html.escape(cell)}</td>" for cell in row)
            result += f"<tr>{cells}</tr>\n"
        return result[:-1] # Strip trailing newline

blocks = {"*": HtmlUtils()}
blockgen.file.set_blocks("./preview.html", blocks)
