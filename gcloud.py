import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

class SheetHandler :
    """ 
    Class responsible for loading into memory the sheet from Google Spreadsheets,
    and update it.

    ...
    Attributes:
        service_account (gspread.Client) : Client object for authentication.
        sheet (gspread.models.Spreadsheet): Sheet object of the manipulated spreadsheet.
        resources (dict) : Dictionary of resources useful to this class.
    """

    service_account = None
    sheet = None
    resources = {
            'sheet_name' : "engenharia_de_software",
            'credential_file_path' : "credencial.json",
            'sheet_url' : 'https://docs.google.com/spreadsheets/d/1L6m6HIJV3rjxMTVjjAQlilGBG3kUSWuU8QSN2Bb5Rec/edit?usp=sharing'
            }

    def __init__(self):
        """
        Constructs a SheetHandler using the class' resources.
        """
        print("Fetching sheet from google drive")
        self.service_account = gspread.service_account(filename=self.resources['credential_file_path'])
        self.sheet = self.service_account.open_by_url(self.resources['sheet_url'])


    def get_sheet_as_dataframe(self):
        """
        Transform this Spreadsheet object into a Pandas.DataFrame object.
        """
        print("Transforming sheet into a pandas' dataframe")
        sheet_vals = self.sheet.worksheet(self.resources['sheet_name']).get_all_values()
        sheet_as_dataframe = pd.DataFrame(sheet_vals[3:], columns=sheet_vals[2])
        cols_types_dict = {
                'Matricula' : 'int32',
                'Aluno' : 'string',
                'Faltas' : 'float32',
                'P1' : 'float32',
                'P2' : 'float32',
                'P3' : 'float32',
                }
        sheet_as_dataframe = sheet_as_dataframe.astype(cols_types_dict)
        return sheet_as_dataframe


    def get_lectures_number(self):
        """
        Extracts the number of lectures on a semester from the class' sheet
        """
        print("Retrieving total number of lectures per semester")
        sheet_vals = self.sheet.worksheet("engenharia_de_software").get_all_values()
        second_line = sheet_vals[1]
        lectures_text = second_line[0]
        lectures_quant = lectures_text.split(" ")[-1]
        return lectures_quant


    def update_cells(self, column_cells_range, new_values):
        """
        Updates cells on column_cells_range from class' spreadsheet with new_values   
        """
        worksheet = self.sheet.worksheet(self.resources['sheet_name']) 
        cells = worksheet.range(column_cells_range)
        for ind, new_value in enumerate(new_values):
            cells[ind].value = new_value
        worksheet.update_cells(cells)


    def update_status_column(self, new_statuses):
        """
        Update "Situação" column from class' spreadsheet with 
        new_statuses as new values
        """
        print("Updating values of column \"Situação\"")
        cells = 'G4:G27'
        self.update_cells(cells, new_statuses)


    def update_marks_approval_column(self, new_marks):
        """
        Update "Nota para Aprovação Final" column from class' spreadsheet 
        with new_marks as new values
        """
        print("Updating values of column \"Nota para Aprovação Final\"")
        cells = 'H4:H27'
        self.update_cells(cells, new_marks)
