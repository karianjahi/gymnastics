import glob
from morgengold_02_day_delivery_tables import DayDeliveryFile
from morgengold_01_extract_text_from_pdf_file import ExtractMorgenGoldContents

# ===== Required initial parameters =========
home_street="Elsa-Braendstroem-Str."
house_no="15a"
plz="76228"
city="Karlsruhe"
google_api_key=""
save_directory="/home/karianjahi/gymnastics/gymnastics/day_info_tables"
# ====== End of required parameters ===========


print("====================== Extracting and saving day file itineray ======================")
ausfahrliste_directory = "/home/karianjahi/gymnastics/gymnastics/delivery_files"
ausfahrliste_files = sorted(glob.glob(ausfahrliste_directory + "/*pdf"))
for file in ausfahrliste_files:
    DayDeliveryFile(file=file,
                    home_street=home_street,
                    house_no=house_no,
                    plz=plz,
                    google_api_key=google_api_key,
                    city=city,
                    directory=save_directory).save_day_file()
