# -----------------------------------------------------------------------------#
# example:      立榮航空
# -----------------------------------------------------------------------------#
from script_UniAir import UniAir

# input area
# -----------------------------------------------------------------------------#
INFO = {    # FLIGHT INFO #
                        "FROM"      : "松山(TSA)",
                        "TO"        : "金門(KNH)",
                        "DATE"      : "2022-08-08", # YYYY-mm-dd
                        "PEOPLE"    : 4, # number of adults
                        "BABY"      : 0, # number of babies
                        "DEPARTURE" : "14:30",  ## HH:MM
                        # FARE TYPE #
                        "FULLPRICE"     : 1,  # 一般-全額
                        "ELDER"         : 1,  # 一般-敬老
                        "CHILDREN"      : 0,  # 一般-兒童
                        "MILITARY"      : 0,  # 一般-軍人
                        "DISABLE"       : 0,  # 一般-愛心
                        "DISABLE-COMP"  : 0,  # 一般-愛心陪同
                        "RESIDENT"      : 2,  # 居民
                        "RE-ELDER"      : 0,  # 居民-敬老
                        "RE-DISABLE"    : 0,  # 居民-愛心
                        "RE-DISABLE-COMP": 0,  # 居民-愛心陪同
                        # PASSENGER LIST #
                        #   "LASTNAME_FIRSTNAME_GENDER(先生/女士/男童/女童)_ID_BIRTHDATE(YYYY-mm-dd)"
                        #   in the order of 一般-全額 > 一般-敬老 > 一般-兒童 > 一般-軍人 > 一般-愛心 > 一般-愛心陪同 
                        #                   > 居民 > 居民-敬老 > 居民-愛心
                        "PASSENGER-LIST" : ["鍾_多多_先生_O123456789_1978-06-24",
                                            "林_小多_女士_B223456789_1935-06-24",
                                            "鍾_大多_女士_C223456789_1995-06-24",
                                            "林_多_女士_D223456789_1996-06-24",],
                                            
                        #   "DISTRICT CODE", "PHONE NUMBER", "MOBILE", "EMAIL"
                        "CONTACT-INFO" : ["0912345678","stanxxxx@gmail.com"],
                        # PAYMENT INFO #
                        "CARD-TYPE"     : "American Express",    # VISA/MasterCard/American Express/JCB
                        "CARD-NUMBER"   : "1234567812345678",
                        "DUE-MONTH"     : "06",
                        "DUE-YEAR"      : "2024",
                        "CVV"           : "123",
                    }
# script start
# -----------------------------------------------------------------------------#
UniAir().run(INFO, start_when="2022-05-25_00:00")

# -----------------------------------------------------------------------------#
# or you can
# dump require_info as REQUIRED_INFO.txt -> edit REQUIRED_INFO.txt -> read REQUIRED_INFO.txt
# -----------------------------------------------------------------------------#
# start the class obj.
crawler = UniAir()
# dump required info, helper will apear in the terminal window
crawler.dump_required_info()
# after editing the txt file, read
crawler.read_info()
# speicigy start_when time(or skip this block)
start_when = "2022-05-25_00:00"
# start
crawler.run(start_when=start_when)