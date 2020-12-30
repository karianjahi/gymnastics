import glob
import re as gsub
import numpy as np
from utils import month_abb_to_numeric
class DailyEarnings:

    def __init__(self, day_info_directory):
        """
        initialization
        :param day_info_directory: directory containing day info files
        """
        self.day_info_directory = day_info_directory

    def are_there_any_files(self):
        """
        Checks whether there are any files in the directory
        :return: True/False
        """
        files = self.get_day_info_files()
        if len(files) > 0:
            return True
        else:
            return False

    def get_day_info_files(self):
        """
        Get the day info files
        :return: list of strings as files
        """
        return glob.glob(self.day_info_directory + "/*csv")

    def convert_month_abb_to_numeric_in_files(self):
        """
        Get month abbreviation from file strings
        :return: list of strings as month abbreviations
        """
        return [i.split("-")[0] + "-" +
                month_abb_to_numeric(i.split("-")[1]) + "-" +
                i.split("-")[2]
                for i in self.get_day_info_files()]

    def get_order_sequence_by_date_for_files(self):
        """
        Get index of each file if it were sorted by date
        :return: list of integers
        """
        return np.argsort(self.convert_month_abb_to_numeric_in_files())

    def get_files_sorted_by_date(self):
        """
        sort files by date
        :return: list of strings as files
        """
        files = self.get_day_info_files()
        indices = self.get_order_sequence_by_date_for_files()
        return [files[i] for i in indices]













obj = DailyEarnings("/home/karianjahi/gymnastics/gymnastics/day_info_tables")
# print(obj.get_order_sequence_by_date_for_files())
for file in obj.get_files_sorted_by_date():
    print(file)