import re as gsub
import numpy as np
import pandas as pd
from datetime import datetime
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
import googlemaps
def remove_item_from_list(alist, item2remove):
    """
    Removing an item from a list
    :param alist: a list of items
    :param item2remove: string to remove
    :return: filtered list
    """
    new_list = []
    for item in alist:
        if item is not item2remove:
            new_list.append(item)
    return new_list

def month_abb(month_numeric):
    """
    Convert a numeric month value to a month abbreviation e.g 1 for Jan, 2 for Feb
    :param month_numeric: an integer between 1 and 12
    :return: string of month Abbreviation
    """
    month_abb = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    if month_numeric <= 12 and month_numeric > 0:
        return month_abb[month_numeric - 1]

def month_abb_to_numeric(month_abb):
    """
    Convert month abb to numeric
    :param month_abb: numeric month
    :return: integer
    """
    if month_abb == "Jan":
        return "01"
    if month_abb == "Feb":
        return "02"
    if month_abb == "Mar":
        return "03"
    if month_abb == "Apr":
        return "04"
    if month_abb == "May":
        return "05"
    if month_abb == "Jun":
        return "06"
    if month_abb == "Jul":
        return "07"
    if month_abb == "Aug":
        return "08"
    if month_abb == "Sep":
        return "09"
    if month_abb == "Oct":
        return "10"
    if month_abb == "Nov":
        return "11"
    if month_abb == "Dec":
        return "12"

def replace_special_accents(string):
    """
    :param string: a string with special accents (or none)
    This function replaces special accents especially german ones
    e.g. ä to ae, ö to oe ü to ue ß to ss
    :return: string with special accents replaced
    """
    return gsub.sub("Sainte-Marie-aux-Mines-Strasse", "Ste.-Marie-aux-Mines-Str.",
                    gsub.sub("ß", "ss",
                    gsub.sub("ü", "ue",
                             gsub.sub("ö", "oe",
                                      gsub.sub("ä", "ae",
                                               string)))))

def get_next_item(alist, item, use_first_found):
    """
    This function gets next item in a list given current item
    :param item: a string that triggers the next item
    :param alist: a list of strings
    :param use_first_found: should we use the first matching index.
    if not, the entire list of index match is returned.
    :return: string representing next item
    """
    for i in np.where(np.array(alist) == item):
        indices = i
    if use_first_found:
        return alist[indices[0] + 1]
    else:
        items = []
        for i in indices:
            if i < len(alist) - 1:
                items.append(alist[i + 1])
        return items

def make_sequence(a, b):
    """
    make a sequence given a and b as integers
    :param a:
    :param b:
    :return: a sequence between a and b where [a, b]
    """
    return list(range(a, b+1))

def unlist_list(alist):
    """
    Give a list like [[3.5, 1.5], [4.1, 5.2]], the aim here
    is to unlist it to [3.5, 1.5, 4.1, 5.2]
    :param alist: a list of items
    :return: one list of items
    """
    new_list = []
    for i in alist:
        for j in i:
            new_list.append(j)
    return new_list

def create_dict_from_alternalte_list(alist):
    """
    Give a list like ["1", "joel", "3", "Kamau", "24", "Sospeter"], we wish
    to create a dictionary of the form {"Joel": 1, "Kamau": 3, "Sospeter": 24}.
    :param alist: a list of even list
    :return: a dictionary as shown in description
    """
    keys = []
    values = []
    my_dict = {}
    for item in alist:
        try:
            values.append(float(item))
        except:
            keys.append(item)
    for i in range(len(values)):
        my_dict[keys[i]] = values[i]
    return my_dict

def create_pandas_table_frame_dictionary(dict, transpose):
    """
    The function creates a pandas dataframe from a dictionary.
    :param dict: a dictionary
    :param transpose: whether the result of table should be transposed
    :return: a pandas dataframe
    """
    if transpose:
        return pd.DataFrame(dict, index = [0]).transpose()
    return pd.DataFrame(dict, index = [0])

def get_unique_list(alist):
    """
    a function that gives back a list with unique values
    i.e. no repetitions. for example, given a list like
    [8, 8, 7, 7, 1, 2, 3], we want to return this list
    [8, 7, 1, 2, 3]
    :param alist: a list of items
    :return: a list of items with non-repeating elements
    """
    unique_list = []
    for i in alist:
        if i not in unique_list:
            unique_list.append(i)
    return unique_list


def concatenate_a_list(alist, sep):
    """
    This function concatenates a list into one string using
    a separator, sep. For example alist = ["my", "friend", "is",
    "coming", "next", "year"] becomes "myfriendiscomingnextyear"
    if sep = ""
    :param alist: list of items
    :return: a string
    """
    concatenated_list = ""
    for item in alist:
        concatenated_list = concatenated_list + item + sep
    return concatenated_list


def get_all_succeding_items_starting_from_here(alist, start):
    """
    Given a list like ["John", "Samson", "Tom", "Joel", "Karani"] we
    wish to get all items from Tom as ["Tom", "Joel", "Karani"]
    :param alist: list containing all items
    :param start: item where to start collecting all succeeding items
    :return: a list of a subset of alist
    """
    index = 0
    for item in alist:
        if item == start:
            break
        index += 1
    return [alist[i] for i in range(index, len(alist))]

def unlist_a_list(alist):
    """
    Given a list of lists like [["eulenweg", "rieslingweg", "Dr wohnlich"],
    ["berliner", "eichenweg", "am krottbach"], ["machinistr", "mozartweg"]]
    we can unlist it to have a one nested list as
    ["eulenweg", "rieslingweg", "Dr wohnlich", "berliner", "eichenweg",
    "am krottbach", "machinistr", "mozartweg"]
    i.e. all elements become individual members of one list
    :param alist: a list of list of items
    :return: one list of items
    """
    flattened_list = []
    for item in alist:
        if type(item) == list:
            for subitem in item:
                flattened_list.append(subitem)
        else:
            flattened_list.append(item)
    return flattened_list

def unlist_single_item_list(alist):
    """
    Given a list like [5], we want the
    single item to be just an item outside
    a list i.e. 5
    :param alist: a list of one item
    :return: a single item
    """
    my_list = unlist_a_list(alist)
    if len(my_list) > 1:
        return my_list
    return alist[0]

def calculate_sum_list(alist):
    """
    Calculate the sum of a list of floats
    :param alist: a list of floats
    :return: a single float
    """
    return np.sum(alist)

def make_dataframe_from_dict(dict):
    """
    From a dictionary, we wish to make a pandas table
    :param dict: a dictionary of lists
    :return: a pandas table
    """
    return pd.DataFrame.from_dict(dict)

def create_a_sequence_starting_from_one(length):
    """
    create a sequence starting from one for length
    :param length: length of sequence
    :return: a list of integers
    """
    return [i+1 for i in range(length)]

def unnest_list(nested_list):
    """
    unnesting a nested list
    :param nested_list: a nested list
    :return: list of lists
    """
    new_list = []
    for i in nested_list:
        new_list.append(unlist_a_list(i))
    return new_list

def append_dataframes_by_row(list_of_dataframes):
    """
    Given a list of dataframes with similar structure,
    the aim here is to append them to each other by row
    :param list_of_dataframes: a list of dataframes
    :return: a pandas dataframe
    """
    df = pd.concat(list_of_dataframes)
    df.index = create_a_sequence_starting_from_one(len(df.iloc[:, 0]))
    return df

def extract_single_column_from_table(table, column_name):
    """
    Extract a column from a pandas table and have it as a list
    :param table: pandas dataframe
    :param column_name: name of the desired column
    :return: list of items
    """
    return table.loc[:, column_name].tolist()

def make_continuous_pairwise_list(alist):
    """
    Given a list like [5, 10, 20, 25] the wish is to
    have a pairwise list as follows: 
    [[5, 10], [10, 20], [20, 25]]
    :param alist: a list of items
    :return: list of lists
    """
    chunks = []
    for i in range(len(alist)):
        if i > 0:
            chunks.append([alist[i-1], alist[i]])
    return chunks

def join_list_to_dataframe_as_column(df, alist, column_name):
    """
    Given a list of values, we need to append the list
    to a given dataframe given the number of rows of df
    is equal to the length of the alist
    :param df: pandas table
    :param column_name: name of the tobeadded column
    :param alist: a list of items whose length is equal to
    the number of rows in the dataframe
    :return: a pandas dataframe
    """
    list2df = pd.DataFrame.from_dict({column_name: alist})
    list2df.index = [i+1 for i in range(len(list2df.index))]
    return df.join(list2df)

def calculate_distance_between_two_places(google_api_key, departure_address, destination_address):
    """
    This function calculates the distance between two places given
    addresses
    :param google_api_key: a google api key for access
    :param departure_address: string for departing address in full
    :param destination_address: string for destination address
    :return: float representing distance in km
    """
    google_client = googlemaps.Client(google_api_key)
    distance_matrix = google_client.distance_matrix(departure_address,
                                                    destination_address)
    distance_and_time_info = distance_matrix["rows"][0]["elements"][0]
    distance_with_units = distance_and_time_info["distance"]["text"].split(" ")
    #duration = distance_and_time_info["duration"]["text"]
    # print(distance_and_time_info["distance"])
    if distance_with_units[1] == "m":
        return float(distance_with_units[0])/1000
    return float(distance_with_units[0])


def name_rows_of_tables_starting_at_one(table):
    """
    This function names rows of tables starting from one
    to the length of the rows
    :param table: a pandas dataframe
    :return: a pandas dataframe
    """
    table.index = [i+1 for i in range(len(table.index))]
    return table

def save_table_to_file(table, filename):
    """
    Intention here being to save table under filename
    :param table: pandas dataframe
    :param filename: file to save table to
    :return: nothing
    """
    table.to_csv(filename, sep = ",", index = False)

def add_column_to_the_left_of_table(table, column_name):
    """
    Adding a column to the left of table
    :param table: pandas dataframe
    :param column_name: name of the column
    :return: a pandas dataframe
    """
    if table.index.tolist()[0] == 0:
        indices = [i + 1 for i in table.index.tolist()]
    else:
        indices = table.index.tolist()
    table.index = indices
    first_df = make_dataframe_from_dict({column_name: indices})
    first_df.index = indices
    return first_df.join(table)

def read_table(file):
    """
    read a file to a pandas table
    :param file: path to the file
    :return: pandas table
    """
    return pd.read_csv(file, sep = ",")

def convert_dates_to_datetime(alist, is_sorted):
    """
    :param alist: list of strings with each item in the
    format YYYY-bb-dd
    :param is_sorted: whether to sort by date or not
    :return: list of dates
    """
    if is_sorted:
        return sorted([datetime.strptime(i, "%Y-%b-%d") for i in alist])
    return [datetime.strptime(i, "%Y-%b-%d") for i in alist]

def convert_datetime_to_string(alist):
    """
    convert datetime to nicely formatted strings as follows:
    2020-May-14 etc.
    :param alist: a list of datetime objects
    :return: list of strings
    """
    return [i.strftime("%Y-%b-%d") for i in alist]

def complement_of_a_and_b_where_a_is_benchmark(list_a, list_b):
    """
    We evaluate the complement of A and B. Specifically,
    we need items in B which are not in A
    :return: a list of items
    """
    complement = []
    for item in list_b:
        if item not in list_a:
            complement.append(item)
    return complement

def make_empty_data_frame():
    return pd.DataFrame()

def sum_list(alist):
    """
    sum of a list of floats/integers
    :param alist: a list of floats or integers
    :return: float
    """
    return np.sum(alist)

def sort_table_by_column(table, column_name):
    """
    This function sorts a dataframe by a column given
    column name
    :param table: a pandas table
    :return: a pandas table
    """
    return table.sort_values(by=[column_name])

def extract_values_from_dict(dict):
    """
    This function takes a dictionary and extracts the values
    to create a list of these values
    :param dict: a dictionary
    """
    my_list = []
    for key in dict.keys():
        my_list.append(dict[key])
    return my_list

def sum_two_columns(table, name_a, name_b):
    """
    calculate sum of two columns and have the result in a list
    :param table: a pandas table
    :param name_a: string for name of column
    :param name_b: string for name of colum
    :return: a list
    """
    list_a = table.loc[:, name_a].tolist()
    list_b = table.loc[:, name_b].tolist()
    summations = []
    for i in range(len(table.index)):
        summations.append(list_a[i] + list_b[i])
    return summations


def extract_ausfahrliste_file(full_path):
    """
    Get the name of ausfahrliste file without path
    :param full_path: entire path of file
    :return: string
    """
    splits = full_path.split("/")
    return splits[len(splits)-1]

def uppercase_first_char_and_lower_the_rest(string):
    """
    We uppercase first character and make the rest lower
    :param string: a string
    :return: a string
    """
    return string[0].upper() + string[1:len(string)].lower()

def convert_month_numeric_to_abbrev(value):
    """
    convert a month value to abbreviation
    :param value: month value
    :return: a string as abbreviation bbb
    """
    try:
        value = int(value)
        if value > 12 or value < 1:
            raise ValueError("month must be between 1 and 12")
        if value == 1:
            month = "Jan"
        if value == 2:
            month = "Feb"
        if value == 3:
            month = "Mar"
        if value == 4:
            month = "Apr"
        if value == 5:
            month = "May"
        if value == 6:
            month = "Jun"
        if value == 7:
            month = "Jul"
        if value == 8:
            month = "Aug"
        if value == 9:
            month = "Sep"
        if value == 10:
            month = "Oct"
        if value == 11:
            month = "Nov"
        if value == 12:
            month = "Dec"
        return month
    except:
        month = uppercase_first_char_and_lower_the_rest(value)[0:3]
        if month in ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug",
                  "Sep", "Oct", "Nov", "Dec"]:
            return month
        raise ValueError(value + " not recognised as a valid month")

def get_sequence_between_two_numbers(alist):
    """
    Given 2 numbers [a, b] we need to get all numbers 
    between a and b. e.g given [3, 6] we need to get the 
    numbers 3, 4, 5, 6
    :param alist: a list of two numbers 
    :return: a list 
    """
    return [i for i in range(alist[0], alist[1]+1)]
