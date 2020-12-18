"""
This class takes a pdf ausfahrliste file and extracts all information about customers: names, addresses, breads and
date/time when the orders were made
"""
from utils import remove_item_from_list, \
    month_abb, replace_special_accents, \
    get_next_item, make_sequence, \
    unlist_list,create_dict_from_alternalte_list, \
    create_pandas_table_frame_dictionary, \
    get_unique_list, \
    get_all_succeding_items_starting_from_here, \
    unlist_a_list, unlist_single_item_list, \
    calculate_sum_list, \
    make_dataframe_from_dict, \
    unnest_list, \
    get_sequence_between_two_numbers

import pdftotext as read_pdf
class MorgenGold:

    def __init__(self, aufahrliste_file):
        """
        Initializing the required inputs
        :param aufahrliste_file: a pdf file containing the order for all customers
        """
        self.ausfahrliste_file = aufahrliste_file

    def get_pdf_object(self):
        """
        We need to obtain the object that contains all text
        """
        with open(self.ausfahrliste_file, "rb") as file:
            return read_pdf.PDF(file)

    def get_no_of_pages(self):
        """
        Count the number of pages in this document
        :return: integer of number of pages
        """
        return len(self.get_pdf_object())

    def get_text_for_all_pages(self):
        """
        Extract text from all pages
        :return: a dictionary of strings with pages as key
        """
        page_count = 1
        page_text = {}
        for page in self.get_pdf_object():
            page_text["page_" + str(page_count)] = page
            page_count += 1
        return page_text

    def get_text_for_single_page(self, page_number):
        """
        We need to get text for a single page
        :param page_number: integer specifying the page
        :return: list of strings for a page
        """
        return self.get_text_for_all_pages()["page_" + str(page_number)]
    
    def convert_page_to_lines(self, page_number):
        """
        convert the whole string for a page and create a list of lines
        :param page_number: page number
        :return: a list of strings each string representing a line
        """
        return self.get_text_for_single_page(page_number).split("\n")

    def remove_spaces_from_page(self, page_number):
        """
        remove unnecessary spaces
        :param page_number: integer for a page
        :return: page text as list of string without spaces
        """
        new_lines = []
        lines = self.convert_page_to_lines(page_number)
        for line in lines:
            new_lines.append(remove_item_from_list(line.split(" "), ""))
        return new_lines

    def get_page_contents_in_english_characters_only(self, page_number):
        """
        We need to drop all special accents e.g ä, ö, ü and ß and replace
        them with their corresponding english accents of ae, oe, ue and ss.
        :param page_number: integer for a page
        :return: list of strings
        """
        new_list = []
        for line_of_list in self.remove_spaces_from_page(page_number):
            new_line_of_list = []
            for content in line_of_list:
                new_line_of_list.append(replace_special_accents(content))
            new_list.append(new_line_of_list)
        return new_list

    def capture_date_string(self, page_number):
        """
        search and capture the date from the a page
        :param page_number: page number to search
        :return: date string
        """
        date_position_in_the_list = 6
        for alist in self.get_page_contents_in_english_characters_only(page_number):
            if any([i == "AUSFAHRLISTE" for i in alist]):
                return alist[date_position_in_the_list]

    def capture_date_nice_format(self, page_number):
        """
        Format date in a nice way. YYYY-Mon-Day
        :param page_number: page number where the date is located
        :return: a string of date in a nice format
        """
        date_split = self.capture_date_string(page_number).split(".")
        year = "20" + date_split[2]
        month = str(month_abb(int(date_split[1])))
        day = date_split[0]
        return year + "-" + month + "-" + day

    def capture_meta_info(self, page_number, meta_text):
        """
        capture the meta information e.g tour route and partner name
        :param meta_text: a string of the meta to capture e.g route, partner
        :param page_number: integer for the page
        :return: string representing the meta_info to capture
        """
        for line in self.get_page_contents_in_english_characters_only(page_number):
            for content in line:
                if content == meta_text:
                   return get_next_item(alist=line, item=meta_text, use_first_found=True)
    
    def capture_tour(self, page_number):
        """
        capture the tour route
        :param page_number: integer for the page
        :return: string representing the route
        """
        return self.capture_meta_info(page_number, "Tour:")

    def capture_logistic_partner(self, page_number):
        """
        Capture the name of the contractor involved
        :param page_number: integer for number of pages
        :return: string representing logistic partner
        """
        title = self.capture_meta_info(page_number, "Logistikpartner:")
        return title + " " + self.capture_meta_info(page_number, title)

    def capture_number_of_kilometers_travelled(self, page_number):
        """
        Capture the number of kilometers travelled from a page
        :param page_number: integer for the page number
        :return: float for number of kilometers travelled
        """
        logistic_partner_title = self.capture_meta_info(page_number, "Logistikpartner:")
        logistic_partner_name = self.capture_meta_info(page_number, logistic_partner_title)
        return float(self.capture_meta_info(page_number, logistic_partner_name))

    def remove_empty_lines(self, page_number):
        """
        Remove empty lists in lines
        :param page_number: integer for the page number
        :return: list of lists for all content
        """
        return [i for i in self.get_page_contents_in_english_characters_only(page_number) if i != []]
    
    def remove_all_preceding_items_in_lines_list_until_float_found(self, page_number):
        """
        We need to remove items in lines which don't start with a float
        upto the point when a float is found. Once a float is found, we
        consider every other item in that line. This way
        we rid of additional information about a customer e.g. where the
        house/apartment is located but retain addresses and breads.
        :param page_number: integer for page number
        :return: lines which start with a float
        """
        new_lines = []
        for line in self.remove_empty_lines(page_number):
            line_items = []
            for item in line:
                try:
                    float(item)
                    line_items.append(get_all_succeding_items_starting_from_here(alist=line, start=item))
                    break
                except:
                    "Do nothing"
            new_lines.append(line_items)
        return unlist_a_list(new_lines)

    def get_departure_street_name(self, page_number):
        """
        we need to get the address of the collection center.
        The center address is to be found on top of
        first page.
        :param page_number: integer for the page number
        :return: integer
        """
        counter = 0
        if page_number == 1:
            line = self.remove_empty_lines(page_number)[2]
            print(line)
            for item in line:
                try:
                    float(item)
                    break
                except:
                    "Do nothing"
                counter += 1
            return line[counter - 1] + "" + line[counter]
        raise ValueError("Function applies to page one only!")



    def get_indices_of_regional_code_and_name(self, page_number):
        """
        We want to get the index of the region and code. Note that
        a region code has 5 characters which are float-convertible.
        This is what we are supposed to test.
        alist[0] ensures we are testing the first item only.
        This excludes the departure center.
        :param page_number: integer for the page number
        :return: integer representing index of region and code
        """
        region_code_name_indices = []
        counter = 0
        for alist in self.remove_all_preceding_items_in_lines_list_until_float_found(page_number):
            print(alist)
            if len(alist[0]) == 5:
                try:
                    float(alist[0])
                    region_code_name_indices.append(counter)
                except:
                    "Do nothing at this point"
            counter += 1
        return region_code_name_indices

    def get_lines_of_regional_code_and_name(self, page_number):
        """
        Now that we have indices of lines with region code
        and number, it is time to extract these lines
        :param page_number: integer for the page number
        :return: a list of strings
        """
        all_lines = self.remove_all_preceding_items_in_lines_list_until_float_found(page_number)
        indices = self.get_indices_of_regional_code_and_name(page_number)
        return [all_lines[i] for i in indices]


    def get_index_of_first_region_code(self, page_number):
        """
        We need to obtain the index of the very first region code
        from the list of lines on page.
        This can only be for the first page.
        :param page_number: integer of the page number
        :return: integer of first index where region code appears
        """
        first_member_position_of_region_code = 0
        if page_number == 1:
            return self.get_indices_of_regional_code_and_name(page_number)[first_member_position_of_region_code]
        raise ValueError("first index of regional code only applies to the first page")

    def get_index_of_Kommissionierzone(self, page_number):
        """
        Get the index of the string "Kommissionierzone"
        :param page_number: integer for the page number
        :return: integer
        """
        counter = 0
        for item in self.get_first_item_in_lines_list(page_number):
            if item == "Kommissionierzone:":
               break
            counter += 1
        return counter

    def get_indices_of_bread_type_and_total(self, page_number):
        """
        We want to entrap information about bread type and total for each type
        located specifically on the first page. Any other page is therefore
        invalid. The entrapping is by way of indices (first and last)
        :param page_number: integer for the page number in question
        :return: list of integers
        """
        if page_number == 1:
            return make_sequence(self.get_index_of_Kommissionierzone(page_number) + 1,
                                 self.get_index_of_first_region_code(page_number) - 2)
        raise ValueError("Only valid for page number 1")

    def get_lines_entrapping_bread_type_and_total(self, page_number):
        """
        We need to extract the lines that enclose the information about bread type
        and the corresponding totals. This only applies to the first page
        :param page_number: an integer for the page number
        :return: list of lists of lines with only information about the summary of bread type and totals
        """
        if page_number == 1:
            return [self.remove_empty_lines(page_number)[i] for i in self.get_indices_of_bread_type_and_total(page_number)]
        raise ValueError("Function only applies to the first page")

    def get_bread_summary(self, page_number):
        """
        Here, we extract bread types/totals available in this delivery
        :param page_number: integer corresponding to the page
        :return: a dictionary with key as bread type and value as total
        """
        alist = unlist_list(self.get_lines_entrapping_bread_type_and_total(page_number))
        return create_dict_from_alternalte_list(alist)

    def create_bread_summary_table(self, page_number):
        """
        This function creates a summary table for bread type and totals
        :param page_number: integer for page number
        :return: a pandas dataframe
        """
        return create_pandas_table_frame_dictionary(self.get_bread_summary(page_number), transpose = True)

    def get_indices_of_lines_with_a_comma(self, page_number):
        """
        This function isolates the indices of lines with a comma.
        This is a deliberate move to isolate lines with addresses in
        another function
        :param page_number: integer of page number
        :return: a list of integers as indices of lines which have a comma
        """
        indices = []
        count = 0
        for i in self.remove_empty_lines(page_number):
            for j in i:
                for k in j:
                    if k == ",":
                        indices.append(count)
            count += 1
        return indices

    def get_lines_with_a_comma(self, page_number):
        """
        This function isolates lines in the given page which have
        a comma at any point
        :param page_number: integer for the page number
        :return: list of strings with commas
        """
        lines = self.remove_empty_lines(page_number)
        indices = self.get_indices_of_lines_with_a_comma(page_number)
        return [lines[i] for i in indices]

    def get_indices_of_lines_with_a_comma_starting_with_an_integer(self, page_number):
        """
        This function is exactly the same as
        get_indices_of_lines_with_a_comma
        but only selects indices of lines which
        have an integer at the beginning
        :param page_number: an integer for the page number
        :return: a list of integers as indices of lines with a
        comma but starting with an integer
        """
        possible_indices_of_addresses = self.get_indices_of_lines_with_a_comma(page_number)
        addresses = [self.remove_empty_lines(page_number)[i] for i in possible_indices_of_addresses]
        count = 0
        indices = []
        for address in addresses:
            try:
                float(address[0])
                indices.append(possible_indices_of_addresses[count])
            except:
                "Do nothing"
            count += 1
        return indices

    def get_unique_indices_of_customer_lines_with_a_comma_starting_with_an_integer(self, page_number):
        """
        This function is exactly the same as get_indices_of_lines_with_a_comma_starting_with_an_integer
        but only returns a unique list of indices
        :param page_number: integer for the page number
        :return: a list of items
        """
        return get_unique_list(self.get_indices_of_lines_with_a_comma_starting_with_an_integer(page_number))

    def get_lines_of_customer_addresses(self,page_number):
        """
        This function gets customer addresses given unique indices of lines
        that start with an integer
        :param page_number: an integer for the page number
        """
        return [
            self.remove_empty_lines(page_number)[i]
                for i in
            self.get_unique_indices_of_customer_lines_with_a_comma_starting_with_an_integer(page_number)
        ]

    def get_customer_lines_without_additional_info(self, page_number):
        """
        This function returns the lines of customer info but drops
        additional info e.g. PRO, RKL, NEU etc which are always in
        capital letters. We are therefore targeting capital letters
        :param page_number: an integer for the page number
        :return: a list of lines with customer info and address without
        additional information
        """
        customer_lines = []
        for customer_info in self.get_lines_of_customer_addresses(page_number):
            items = []
            for item in customer_info:
                if item.isupper():
                    "Do nothing"
                else:
                    items.append(item)
            customer_lines.append(items)
        return customer_lines

    def get_customer_names(self, page_number):
        """
        Customer names only. We achieve by selecting the last two
        items in get_customer_lines_without_additional_info function
        :param page_number: an integer for the page number
        :return: a list customer names
        """
        customer_names = []
        for line in self.get_customer_lines_without_additional_info(page_number):
            customer_names.append(line[len(line) - 2] + " " + line[len(line) - 1])
        return customer_names

    def get_customer_addresses_without_region_code_and_name(self, page_number):
        """
        Get a list of customer addresses without region code and name
        We achieve this by selecting everything between the second and last
        but two items in get_customer_lines_without_additional_info
        first item has index 1 and last item but 2 has index len() - 2
        :param page_number: an integer for the page number
        :return:
        """
        customer_addresses = []
        for line in self.get_customer_lines_without_additional_info(page_number):
            address_list = [line[i] for i in range(1, len(line)-2)]
            address = ""
            for item in address_list:
                address = address + " " + item
            customer_addresses.append(address)
        return customer_addresses

    def get_lines_containing_region_code_and_name_for_any_given_page(self, page_number):
        """
        This function is similar to the get_indices_of_region_code_and_name but doesn't
        assume that the code is the first item on the line and also returns list of lines.
        It is reasonable expectation to assume that, the number of list members for a line
        whose address is being sought is less than 9 not unless we are interested with the
        very first line containing Kommissionerzone
        :param page_number: integer for the page number
        :return: a list of lines where regional code exists
        """
        region_code_lines = []
        for line in self.remove_all_preceding_items_in_lines_list_until_float_found(page_number):
            for item in line:
                if len(item) == 5 and len(line) < 7: # to avoid the header line which has more than 6 items
                    try:
                        float(item)
                        region_code_lines.append(line)
                    except:
                        "Do nothing"
        return region_code_lines

    def get_indices_of_lines_containing_code_and_region(self, page_number):
        """
        We need the indices of containing region codes and names
        :param page_number: integer for the page number
        :return: a list of integers as indices representing lines containing code and region
        """
        code_and_region_list = self.get_lines_containing_region_code_and_name_for_any_given_page(page_number)
        count = 0
        region_indices = []
        for line in self.remove_all_preceding_items_in_lines_list_until_float_found(page_number):
            if line in code_and_region_list:
                region_indices.append(count)
            count += 1
        return region_indices

    def get_region_codes(self, page_number):
        """
        This function grabs the lines containing region code and name
        among other list members and returns a list of
        region codes
        :param page_number: an integer for the page number
        :return: a list of strings representing the region codes
        """
        region_codes = []
        for line in self.get_lines_containing_region_code_and_name_for_any_given_page(page_number):
            for item in line:
                if len(item) == 5:
                    try:
                        float(item)
                        region_codes.append(item)
                    except:
                        "Do nothing"
        return region_codes

    def get_region_names(self, page_number):
        """
        This function returns a list of region names in a page given
        a region code
        :param page_number: an integer for the page number
        :return: a list of region names
        """
        count = 0
        region_names = []
        for region_code in self.get_region_codes(page_number):
            region_names.append(get_next_item(alist=self.get_lines_containing_region_code_and_name_for_any_given_page(page_number)[count],
                                        item=region_code,
                                        use_first_found=True))
            count += 1
        return region_names

    def get_full_customer_address(self, page_number):
        """
        This function captures the entire customer address by
        adding region code and name to the customer addresses
        :param page_number: an integer for the page number
        :return: list of
        """
        full_address = []
        partial_addresses = self.get_customer_addresses_without_region_code_and_name(page_number)
        region_codes = self.get_region_codes(page_number)
        region_names = self.get_region_names(page_number)
        for i in range(len(partial_addresses)):
            full_address.append(partial_addresses[i] + " " + region_codes[i] + " " + region_names[i])
        return full_address

    def get_bread_indices_per_customer(self,page_number):
        """
        We need to capture the indices of bread lines which are entrapped
        between region code and next one intention being that
        every code and region is followed by breads.
        That means only indices which are entrapped but not including the
        boundaries. Since we have indices of region code and name, we need to
        be smart to capture the next line for the first region code and the previous
        line for the next region code
        :param page_number: an integer for the page number
        :return: a dictionary of lists with each key representing indices enclosing breads per
        customer
        """
        lines_between_dict = {}
        regional_code_indices = self.get_indices_of_lines_containing_code_and_region(page_number)
        after_float_lines = self.remove_all_preceding_items_in_lines_list_until_float_found(page_number)
        for index in range(len(regional_code_indices)):

            if index < (len(regional_code_indices)-1):
                lines_between_dict[index] = [regional_code_indices[index] + 1, regional_code_indices[index + 1] - 2]

            if index == len(regional_code_indices)-1:
                lines_between_dict[index] = [regional_code_indices[index] + 1, len(after_float_lines)-1]
        return lines_between_dict

    def get_unique_lists_of_bread_indices(self, page_number):
        """
        For the dictionary of bread indices, we need to get unique
        items per list. e.g. [[2.2, 4.2], [12.3, 12.3], [4], [6]]
        changes to [[2.2, 4.2], 12.3, 4, 6]
        :param page_number: integer for page number
        :return: a list of unique values
        """
        unique_values = []
        for values in self.get_bread_indices_per_customer(page_number).values():
            unique_values.append(unlist_single_item_list(get_unique_list(values)))
        return unique_values

    def select_lines_given_unique_lists_of_bread_indices(self, page_number):
        """
        We need to select the lines corresponding to the indices
        given by the preceding function
        :param page_number: an integer for the page number
        :return: list of strings as lines
        """
        selected_lines = []
        lines = self.remove_all_preceding_items_in_lines_list_until_float_found(page_number)
        for alist in self.get_unique_lists_of_bread_indices(page_number):

            if type(alist) == list:
                # print(get_sequence_between_two_numbers(alist))
                selected_lines.append([lines[i] for i in get_sequence_between_two_numbers(alist)])

            if type(alist) == int:
                selected_lines.append(lines[alist])
        return unnest_list(selected_lines)

    def get_list_of_breads_per_customer(self, page_number):
        """
        This function returns the lines of bread delivered for each customer
        :param page_number: an integer for the page number in question
        :return: a dictionary of lists
        """
        return self.select_lines_given_unique_lists_of_bread_indices(page_number)

    def extract_bread_type(self, page_number, by_number):
        """
        extracting each bread type number/name per customer
        :param page_number: integer for the page number
        :param by_number: logical if number of each bread type
        is desired.
        :return: list of number of bread types
        """
        bread_number = []
        bread_name = []
        for alist in self.get_list_of_breads_per_customer(page_number):
            number = []
            name = []
            for item in alist:
                try:
                    float(item)
                    number.append(item)
                except:
                    name.append(item)
            bread_number.append(number)
            bread_name.append(name)
        if by_number:
            return bread_number
        return bread_name

    def calculate_total_number_of_breads_delivered_per_customer(self, page_number):
        """
        we need to calculate the total number of breads per customer
        :param page_number: integer for the page number
        :return: list of total number of breads
        """
        summations = []
        for alist in self.extract_bread_type(page_number, by_number=True):
            summations.append(calculate_sum_list([float(i) for i in alist]))
        return summations

    def create_a_table_for_customer_details(self, page_number):
        """
        We wish to create a table for customer name, address,
        and the number of breads delivered
        :param page_number: an integer for the page number
        :return: a pandas dataframe
        """
        return make_dataframe_from_dict({"date": self.capture_date_nice_format(page_number),
                                         "name": self.get_customer_names(page_number),
                                         "address": self.get_full_customer_address(page_number),
                                         "pieces": self.calculate_total_number_of_breads_delivered_per_customer(page_number)})



my_file = "/home/karianjahi/gymnastics/delivery_files/2020-12-05_Ausfahrliste.pdf"
obj = MorgenGold(my_file)
print(obj.get_departure_street_name(1))

# for text in obj.get_index_of_departure_address_line(1):
#     print(text)