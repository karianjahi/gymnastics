from morgengold_01_extract_text_from_pdf_file import ExtractMorgenGoldContents
from utils import append_dataframes_by_row, \
    create_pandas_table_frame_dictionary, \
    extract_single_column_from_table, \
    make_continuous_pairwise_list, \
    calculate_distance_between_two_places, \
    join_list_to_dataframe_as_column, \
    save_table_to_file
import glob
class DayDeliveryFile:

    def __init__(self, file, home_street, house_no, plz, city, google_api_key, directory):
        """
        All initial conditions here
        :param file: string: ausfahrliste file
        :param home_street: string: street name of logistic partner
        :param house_no: string: house no of logistic partner
        :param plz: string: Postleitzahl of logistic partner
        :param city: string: city of logistic partner
        :param google_api_key: string: api key to access google location services
        :param directory: directory where to save day information table
        """
        self.file = file
        self.home_street = home_street
        self.house_no = house_no
        self.plz = plz
        self.city = city
        self.google_api_key = google_api_key
        self.directory = directory

    def create_extract_object(self):
        """
        Create morgengold extract object
        :return: object
        """
        return ExtractMorgenGoldContents(self.file)

    def query_no_of_pages(self):
        """
        Identify no. of pages in the pdf
        :return: integer
        """
        return self.create_extract_object().get_no_of_pages()

    def list_of_page_tables(self):
        """
        Create day table for each delivery
        :return: pandas table
        """
        list_of_tables = []
        for page in range(self.query_no_of_pages()):
            page += 1
            list_of_tables.append(self.create_extract_object().create_table_for_customer_details(page))
        return list_of_tables

    def create_one_table_per_delivery(self):
        """
        We need to create one table per delivery
        :return: pandas table
        """
        return append_dataframes_by_row(self.list_of_page_tables())

    def add_departure_address_to_table(self):
        """
        Add departure address to table
        :return: pandas table
        """
        delivery_table = self.create_one_table_per_delivery()
        departure_address = self.create_extract_object().get_departure_full_address(1)
        split_address = departure_address.split(" ")
        name = split_address[0].split(".")[0] + \
               ", " + split_address[len(split_address)-1]

        date = delivery_table.loc[:, "date"].tolist()[0]
        pieces = 0
        adict = {"date": date,
                "name": name,
                "address": departure_address,
                "pieces": pieces}
        return append_dataframes_by_row(
            [
                create_pandas_table_frame_dictionary(adict, transpose=False),
                delivery_table
            ]
        )

    def add_home_address_to_table(self):
        """
        Add home address and name
        :return: pandas table
        """
        page_number = 1
        delivery_table = self.add_departure_address_to_table()
        logistic_partner = self.create_extract_object().capture_logistic_partner(
            page_number
        )
        date = delivery_table.loc[:, "date"].tolist()[0]
        pieces = 0
        adict = {"date": date,
                 "name": logistic_partner,
                 "address": self.home_street +
                            self.house_no +
                            " " +
                            self.plz +
                            " " +
                            self.city,
                 "pieces": pieces
                 }
        return append_dataframes_by_row(
            [
                delivery_table,
                create_pandas_table_frame_dictionary(adict, transpose=False)
            ]
                                        )

    def get_full_day_delivery_table(self):
        """
        get full table. This function is a replica
        of the add_home_address_to_table
        :return: pandas table
        """
        return self.add_home_address_to_table()

    def get_list_of_addresses(self):
        """
        extract list of addresses from pandas table
        :return: list of strings
        """
        return extract_single_column_from_table(
            table=self.get_full_day_delivery_table(),
            column_name="address"
        )

    def get_address_pairs_sequentially(self):
        """
        Address pairs list in a sequential fashion
        :return: list of lists
        """
        return make_continuous_pairwise_list(self.get_list_of_addresses())

    def get_distances_per_pair(self):
        """
        Calculate distances per pair of addresses using google
        :return: list of floats as distances
        """
        distances = [0.0]
        address_pairs = self.get_address_pairs_sequentially()
        for address_pair in address_pairs:
            distance = calculate_distance_between_two_places(self.google_api_key,
                                                             address_pair[0],
                                                             address_pair[1])
            print("Distance between " +
                  address_pair[0] +
                  " and " +
                  address_pair[1] +
                  " = " +
                  str(distance) +
                  " km" + ". ===================================> Date = " + self.create_extract_object().capture_date_nice_format(page_number=1))

            distances.append(distance)
        return distances

    def add_distance_to_table(self):
        """
        We add distance to the full table
        :return: a pandas table
        """
        return join_list_to_dataframe_as_column(df = self.get_full_day_delivery_table(),
                                                alist = self.get_distances_per_pair(),
                                                column_name="distance")

    def save_day_file(self):
        """
        Here we save day files to directory as 'date'_table.csv
        :return: nothing
        """
        filename = self.create_extract_object().capture_date_nice_format(page_number=1) + \
                   "_table.csv"
        full_filenames_in_folder = glob.glob(self.directory + "/*csv")
        filenames_in_folder = [i.split("/")[-1] for i in full_filenames_in_folder]
        if filename not in filenames_in_folder:
            save_table_to_file(table=self.add_distance_to_table(),
                               filename=self.directory + "/" + filename)
        else:
            # print("file " + filename + " already exists!")
            "Do Nothing"
