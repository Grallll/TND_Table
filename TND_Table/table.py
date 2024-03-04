from typing import List, Tuple

from PIL import Image, ImageDraw, ImageFont


class Table():
    def __init__(self,
                 table: List[list],
                 size: int,
                 font: str = None,
                 distance: Tuple[int, int, int, int] = (0,)*4,
                 lining_size: int = 1) -> None:
        """
        Args:
            table (List[list]): Two-dimensional array from which
                                the image will be made.
            size (int): Font size.
            font (str, optional): Font by .ttf file.
            distance (Tuple[int, int, int, int]): Distance to lining.
                                                  Defaults to (0, 0, 0, 0)
        """
        self.table = table
        self.size = size
        self.font = ImageFont.truetype(font=font,
                                       size=size)
        self.distance = distance
        self.lining_size = lining_size
        self.colors = []

        self.__all_to_string()

        self.__set_size()

        width = int(sum(self.columns))
        hight = sum(self.rows)

        self.img = Image.new(
            mode='RGB',
            size=(width, hight),
            color='white')

    def __all_to_string(self) -> None:
        for row in range(len(self.table)):
            for column in range(len(self.table[row])):
                self.table[row][column] = str(self.table[row][column])

    def __set_width(self,
                    row: int,
                    column: int) -> None:
        """
        EXPLANATION: This method need For better code readability.
        Adjusts the width for a given row.
        """
        max_width_text = max(self.table[row][column].split('\n'),
                             key=len)
        font_size = self.font.getlength(max_width_text)
        real_font_size = font_size + self.distance[2] + self.distance[3]
        if real_font_size > self.columns[column]:
            self.columns[column] = real_font_size

    def __set_hight(self,
                    row: int) -> None:
        """
        EXPLANATION: This method need For better code readability.
        Adjusts the hight for a given column.
        """
        max_hight = max(self.table[row],
                        key=lambda string: string.count('\n'))
        font_size = (max_hight.count('\n')+1)*self.__font_hight
        self.rows[row] = font_size + self.distance[0] + self.distance[1]

    def __set_size(self) -> None:
        """
        Sets the photo dimensions.
        """
        self.__font_hight = sum(self.font.getmetrics())

        num_rows = len(self.table)
        num_columns = len(max(self.table,
                              key=len))

        self.rows = [0,]*num_rows
        self.columns = [0.0,]*num_columns

        for row in range(len(self.table)):
            self.__set_hight(row)
            for column in range(len(self.table[row])):
                # EXPLANATION: For better code readability
                self.__set_width(row, column)

    def __texting(self) -> None:
        """
        Creates text in cells.
        """
        step = [self.distance[0], self.distance[2]]
        for row in range(len(self.table)):
            step[1] = self.distance[2]
            for column in range(len(self.table[row])):
                ImageDraw.Draw(self.img).text(
                    (step[1], step[0]),
                    text=str(self.table[row][column]),
                    fill="Black",
                    font=self.font)
                step[1] += self.columns[column]
            step[0] += self.rows[row]

    def __lining(self) -> None:
        """
        Creates lines for cells.
        """
        step = 0
        for row in self.rows:
            ImageDraw.Draw(self.img).line(
                ((0, step), (self.img.width, step)),
                fill="Black",
                width=self.lining_size)
            step += row
        step = 0
        for column in self.columns:
            ImageDraw.Draw(self.img).line(
                ((step, 0), (step, self.img.height)),
                fill="Black",
                width=self.lining_size)
            step += column

    def colorize_row(self,
                     color: Tuple[int, int, int],
                     row: int) -> None:
        """
        Sets color for any row.

        Args:
            color (Tuple[int, int, int]): (Red, Green, Blue)
            row (int): Row to be colored.
        """
        if len(self.rows) > row > -1:
            self.colors.append((0, color, row))

    def colorize_column(self,
                        color: tuple,
                        column: int) -> None:
        """
        Sets color for any column.

        Args:
            color (tuple(int, int, int)): (Red, Green, Blue)
            row (int): Column to be colored.
        """
        if len(self.columns) > column > -1:
            self.colors.append((1, color, column))

    def colorize_cells(self,
                       color: tuple,
                       cells: Tuple[tuple]) -> None:
        """
        Sets color for any cells.

        Args:
            color (tuple): (Red, Green, Blue)
            cells (Tuple[tuple]): Tuple of cells to be colored.
                                For any cell need write (X, Y) coordinates.
                                EXAMPLE: ((0, 0), (1, 1), (2, 2))
        """
        for cell in cells:
            if ((len(self.columns) > cell[1] > -1) and
               (len(self.rows) > cell[0] > -1)):
                self.colors.append((2, color, (cell[0], cell[1])))
            else:
                print(cell, len(self.columns))

    def __colorize_row(self,
                       color: Tuple[int, int, int],
                       row: int) -> None:
        line = sum(self.rows[:row])
        ImageDraw.Draw(self.img).rectangle(
            ((0, line),
                (self.img.width, line + self.rows[row])),
            fill=color)

    def __colorize_column(self,
                          color: tuple,
                          column: int) -> None:
        line = sum(self.columns[:column])
        ImageDraw.Draw(self.img).rectangle(
            ((line, 0),
                (line + self.columns[column], self.img.height)),
            fill=color)

    def __colorize_cells(self,
                         color: tuple,
                         cell: Tuple[tuple]) -> None:
        column = sum(self.columns[:cell[1]])
        row = sum(self.rows[:cell[0]])
        left_top = (column, row)
        right_bottom = (column + self.columns[cell[1]],
                        row+self.rows[cell[0]])
        ImageDraw.Draw(self.img).rectangle(
            (left_top, right_bottom),
            fill=color)

    def get_PIL_img(self,
                    lining: bool = True) -> Image:
        """
        Get current image (PIL.Image.Image).

        Args:
            lining (bool, optional): Sets the markup. Defaults to True.
        """
        colorize = {
            0: self.__colorize_row,
            1: self.__colorize_column,
            2: self.__colorize_cells
        }
        for color in self.colors:
            colorize[color[0]](color[1], color[2])

        self.__texting()
        if lining:
            self.__lining()
        return self.img

    def get_img(self,
                way: str = 'Table_by_TND.png') -> None:
        """
        Makes .png file.

        Args:
            way (str, optional): Way to .png file.
                                 Defaults to 'Table_by_TND.png'.
        """
        self.get_PIL_img().save(way)
