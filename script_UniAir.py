from dependencies.DriverSetup import *
from dependencies.utility import is_birthday_correct, process_flight_info, process_passenger_list, refine_date
from datetime import datetime
from math import floor
from dependencies.utility import TraceReporter
from dependencies.Scripts_default import Scripts_default
import json

class UniAir(Scripts_default):
    url = "https://www.uniair.com.tw/rwd/index.aspx"
    REQUIRED_INFO = {    # FLIGHT INFO #
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
    INFO_HELP =     {   # FLIGHT INFO #
                        "FROM"      : "松山(TSA)",
                        "TO"        : "金門(KNH)",
                        "DATE"      : "in form of YYYY-mm-dd, ex:'2022-08-08'",
                        "PEOPLE"    : "number of adults, ex:4",
                        "BABY"      : "number of babies, ex:0",
                        "DEPARTURE" : "HH:MM, ex:'14:30'",
                        # FARE TYPE #
                        "FULLPRICE"     : "一般-全額, ex:1",
                        "ELDER"         : "一般-敬老, ex:1",
                        "CHILDREN"      : "一般-兒童, ex:0",
                        "MILITARY"      : "一般-軍人, ex:0",
                        "DISABLE"       : "一般-愛心, ex:0",
                        "DISABLE-COMP"  : "一般-愛心陪同, ex:0",
                        "RESIDENT"      : "居民, ex:2",
                        "RE-ELDER"      : "居民-敬老, ex:0",
                        "RE-DISABLE"    : "居民-愛心, ex:0",
                        "RE-DISABLE-COMP": "居民-愛心陪同, ex:0",
                        # PASSENGER LIST #
                        "PASSENGER-LIST" : "in the order of 一般-全額 > 一般-敬老 > 一般-兒童 > 一般-軍人 > 一般-愛心 > 一般-愛心陪同 > 居民 > 居民-敬老 > 居民-愛心 \n"+\
                                    "such as:['鍾_多多_先生_O123456789_1978-06-24', '林_小多_女士_B223456789_1935-06-24', '鍾_大多_女士_C223456789_1995-06-24', '林_多_女士_D223456789_1996-06-24']",                        
                        "CONTACT-INFO" : "['ex:0912345678', 'ex:stanxxxx@gmail.com']",
                        # PAYMENT INFO #
                        "CARD-TYPE"     : "ex:American Express(VISA/MasterCard/American Express/JCB)",
                        "CARD-NUMBER"   : "ex:1234567812345678",
                        "DUE-MONTH"     : "ex:06",
                        "DUE-YEAR"      : "ex:2024",
                        "CVV"           : "安全碼",        
                    }
    
    def start(self):
        # params
        url = self.url
        INFO = self.INFO
        # recorder
        ____tr = TraceReporter(debug_flag=True)
        # get        
        ____tr.session_start('start driver engine', 0)
        driver = DriverSetup()
        driver.get(url)
        driver.maximize_window()
        ____tr.session_end()
        # ----------------------------------------------------------------------------------- #
        # STEP ONE
        # ----------------------------------------------------------------------------------- #
        # Select FROM/TO
        ____tr.session_start('start step one', 1)
        el = driver.find_element(By.ID, "ddl_DEP")
        Select(el).select_by_visible_text(INFO["FROM"])
        el = driver.find_element(By.ID, "ddl_ARR")
        Select(el).select_by_visible_text(INFO["TO"])

        # Pick Date
        driver.find_element_then_click(By.ID, "CPH_Body_lb_TRIP_DATE")
        driver.find_element_then_click(By.CLASS_NAME, "datepicker--nav-title")
        driver.find_element_then_click(By.CLASS_NAME, "datepicker--nav-title")
        # refine DATE for webpage format
        DATE_refined = refine_date(INFO["DATE"])
        # YYYY
        driver.find_element_then_click(By.XPATH, "//div[text()='"+DATE_refined[0]+"']")
        # mm
        driver.find_element_then_click(By.XPATH, "//div[text()='"+DATE_refined[1]+"']")
        # dd
        driver.find_element_then_click(By.XPATH, "//div[text()='"+DATE_refined[2]+"']")

        # people
        driver.find_element_then_click(By.ID, "CPH_Body_tb_PaxNum")
        # people
        if not INFO["PEOPLE"] == 1:
            for i in range(INFO["PEOPLE"]):
                driver.find_element_then_click(By.XPATH, "(//button[@class='plus'])")
        # baby
        for i in range(INFO["BABY"]):
            driver.find_element_then_click(By.XPATH, "(//button[@class='plus'])[2]")
        driver.find_element_then_click(By.CLASS_NAME, "done-select")

        # press search button
        driver.find_element_then_click(By.ID, "CPH_Body_btn_SelectFlight")
        ____tr.session_end()
        # ----------------------------------------------------------------------------------- #
        # STEP TWO
        # ----------------------------------------------------------------------------------- #
        ____tr.session_start('start step two', 1, end='\n')
        # get flight information
        flight_info = driver.wait_find_element(By.ID, "CPH_Body_uc_SelectFlight_pnl_Flight").text.split('\n')
        departure_index = process_flight_info(flight_info, INFO['DEPARTURE'])
        # choose flight by departure time
        driver.find_element_then_click(By.XPATH, "//a[@id='CPH_Body_uc_SelectFlight_rpt_Flight_btn_SelectFlight_"+departure_index+"']//span[1]")

        ____tr.session_start('filling fare-type', 2)
        # fare type
        if INFO["PEOPLE"] == 1:
            try:
                Select(driver.wait_find_element(By.ID, "CPH_Body_rpt_FareType_rpt_FareInfo_0_ddl_Num_0")).select_by_index(INFO["FULLPRICE"])
            except:
                sleep(1)
                Select(driver.wait_find_element(By.ID, "CPH_Body_rpt_FareType_rpt_FareInfo_0_ddl_Num_0")).select_by_index(INFO["FULLPRICE"])
            Select(driver.find_element(By.ID, "CPH_Body_rpt_FareType_rpt_FareInfo_0_ddl_Num_1")).select_by_index(INFO["ELDER"])
            Select(driver.find_element(By.ID, "CPH_Body_rpt_FareType_rpt_FareInfo_0_ddl_Num_2")).select_by_index(INFO["MILITARY"])
            Select(driver.find_element(By.ID, "CPH_Body_rpt_FareType_rpt_FareInfo_0_ddl_Num_3")).select_by_index(INFO["DISABLE"])
            Select(driver.find_element(By.ID, "CPH_Body_rpt_FareType_rpt_FareInfo_1_ddl_Num_0")).select_by_index(INFO["RESIDENT"])
            Select(driver.find_element(By.ID, "CPH_Body_rpt_FareType_rpt_FareInfo_1_ddl_Num_1")).select_by_index(INFO["RE-ELDER"])
            Select(driver.find_element(By.ID, "CPH_Body_rpt_FareType_rpt_FareInfo_1_ddl_Num_2")).select_by_index(INFO["RE-DISABLE"])
        else:
            try:
                Select(driver.wait_find_element(By.ID, "CPH_Body_rpt_FareType_rpt_FareInfo_0_ddl_Num_0")).select_by_index(INFO["FULLPRICE"])
            except:
                sleep(1)
                Select(driver.wait_find_element(By.ID, "CPH_Body_rpt_FareType_rpt_FareInfo_0_ddl_Num_0")).select_by_index(INFO["FULLPRICE"])
            Select(driver.find_element(By.ID, "CPH_Body_rpt_FareType_rpt_FareInfo_0_ddl_Num_1")).select_by_index(INFO["ELDER"])
            Select(driver.find_element(By.ID, "CPH_Body_rpt_FareType_rpt_FareInfo_0_ddl_Num_2")).select_by_index(INFO["CHILDREN"])
            Select(driver.find_element(By.ID, "CPH_Body_rpt_FareType_rpt_FareInfo_0_ddl_Num_3")).select_by_index(INFO["MILITARY"])
            Select(driver.find_element(By.ID, "CPH_Body_rpt_FareType_rpt_FareInfo_0_ddl_Num_4")).select_by_index(INFO["DISABLE"])
            Select(driver.find_element(By.ID, "CPH_Body_rpt_FareType_rpt_FareInfo_0_ddl_Num_5")).select_by_index(INFO["DISABLE-COMP"])
            Select(driver.find_element(By.ID, "CPH_Body_rpt_FareType_rpt_FareInfo_1_ddl_Num_0")).select_by_index(INFO["RESIDENT"])
            Select(driver.find_element(By.ID, "CPH_Body_rpt_FareType_rpt_FareInfo_1_ddl_Num_1")).select_by_index(INFO["RE-ELDER"])
            Select(driver.find_element(By.ID, "CPH_Body_rpt_FareType_rpt_FareInfo_1_ddl_Num_2")).select_by_index(INFO["RE-DISABLE"])
            Select(driver.find_element(By.ID, "CPH_Body_rpt_FareType_rpt_FareInfo_1_ddl_Num_3")).select_by_index(INFO["RE-DISABLE-COMP"])
        ____tr.session_end()
        # confirm
        driver.find_element_then_click(By.ID, "CPH_Body_btn_NextStep")
        # ----------------------------------------------------------------------------------- #
        # STEP THREE
        # ----------------------------------------------------------------------------------- #
        ____tr.session_start('start step three', 1)
        # click agreement then NEXT
        driver.find_element_then_click(By.ID, "CPH_Body_lb_CheckNote")
        driver.find_element_then_click(By.ID, "CPH_Body_btn_NextStep")
        ____tr.session_end()
        # ----------------------------------------------------------------------------------- #
        # STEP FOUR
        # ----------------------------------------------------------------------------------- #
        ____tr.session_start('start step four', 1, end='\n')
        # break down INFO["PASSENGER-LIST"]
        passenger_list = process_passenger_list(INFO)
        sleep(2)
        # fill-in passenger list
        for i in range(INFO["PEOPLE"]):
            ____tr.session_start('fill person info : '+str(i), 2, end='\n')
            driver.send_ScrollDown(2)
            index = str(i)
            # last name
            driver.wait_find_element(By.ID, "CPH_Body_rpt_PassengerList_tb_LastName_"+index).send_keys(passenger_list[i][0])
            # first name
            driver.find_element(By.ID, "CPH_Body_rpt_PassengerList_tb_FirstName_"+index).send_keys(passenger_list[i][1])
            # title 
            Select(driver.find_element(By.ID, "CPH_Body_rpt_PassengerList_ddl_Title_"+index)).select_by_visible_text(passenger_list[i][2])
            sleep(1)
            # ----------------------------------------------------------------------------------- #
            # find correct year 
            # ----------------------------------------------------------------------------------- #
            if "ELDER" in passenger_list[i][5]:
                year = int(datetime.now().strftime("%Y")) - 65
            elif "CHILDREN" in passenger_list[i][5]:
                year = int(datetime.now().strftime("%Y")) - 12
            else:
                year = int(datetime.now().strftime("%Y")) - 30
            year -= year % 10
            shift_time = floor((int(passenger_list[i][4][0])-year) / 10)
            # click birthday
            driver.find_element_then_click(By.ID, "CPH_Body_rpt_PassengerList_lb_Birthday_"+index)    
            sleep(1)
            driver.find_element_then_click(By.ID, "CPH_Body_rpt_PassengerList_tb_Birthday_"+index)
            sleep(0.5)    
            if i == 0:
                driver.find_element_then_click(By.XPATH, "(//div[@class='datepicker--nav-title'])")
                sleep(0.5)
                driver.find_element_then_click(By.XPATH, "(//div[@class='datepicker--nav-title'])")
            else:
                driver.find_element_then_click(By.XPATH, "(//div[@class='datepicker--nav-title'])["+str(i+1)+"]")
                sleep(0.5)
                driver.find_element_then_click(By.XPATH, "(//div[@class='datepicker--nav-title'])["+str(i+1)+"]")
            sleep(0.5)
            # year-page shifting
            ____tr.session_start('find correct year', 3)
            if shift_time < 0:
                shift_time *= -1
                for j in range(shift_time):
                    #driver.send_Left_Alt()
                    driver.find_element_then_click(By.XPATH, "(//div[@class='datepicker--nav-action'])["+str((i)*2+1)+"]")
            elif shift_time > 0:
                for j in range(shift_time):
                    #driver.send_Right_Alt()
                    driver.find_element_then_click(By.XPATH, "(//div[@class='datepicker--nav-action'])["+str((i)*2+2)+"]")
            ____tr.session_end()
            # ----------------------------------------------------------------------------------- #
            # end - find correct year
            # ----------------------------------------------------------------------------------- #
            recheck_birthday_correct = False
            while not recheck_birthday_correct:
                sleep(1)
                # YYYY
                ____tr.session_start('fill birthday year', 3)
                for ii in range(i+1):
                    try:
                        driver.find_element_then_click(By.XPATH, "(//div[text()='"+passenger_list[i][4][0]+"'])["+str(ii+1)+"]")            
                    except:
                        pass
                ____tr.session_end()
                # mm
                sleep(0.5)
                ____tr.session_start('fill birthday month', 3)
                for ii in range(i+1):
                    try:
                        driver.find_element_then_click(By.XPATH, "(//div[text()='"+passenger_list[i][4][1]+"'])["+str(ii+1)+"]")            
                    except:
                        pass
                ____tr.session_end()
                # dd
                sleep(0.5)    
                ____tr.session_start('fill birthday day', 3)
                for ii in range(i+1):
                    try:
                        driver.find_element_then_click(By.XPATH, "(//div[text()='"+passenger_list[i][4][2]+"'])["+str(ii+1)+"]")
                    except:
                        pass
                ____tr.session_end()
                # recheck birthday filled correctly
                ____tr.session_start('check birthday input result',3)
                value = driver.find_element(By.ID, "CPH_Body_rpt_PassengerList_hi_Birthday_"+index).get_attribute("value")
                recheck_birthday_correct = is_birthday_correct(value, INFO, i)
                ____tr.session_end()
                if not recheck_birthday_correct:
                    ____tr.session_start('retry fill-in birthday',3, '\n')

            sleep(0.5)
            ____tr.session_start('fill country (TW)', 3)
            # Country
            try:
                # RESIDENT cant click the button
                driver.find_element_then_click(By.ID, "CPH_Body_rpt_PassengerList_btn_SelectCountry_"+index)
            except:
                pass
            driver.find_element_then_click(By.XPATH, "//li[@data-text='台灣 (TW)']")
            ____tr.session_end()
            # ID
            ____tr.session_start('fill ID number', 3)
            try:
                sleep(1.5)
                driver.find_element(By.ID,"CPH_Body_rpt_PassengerList_tb_ID_NO_"+index).send_keys(passenger_list[i][3])
            except:
                try:
                    sleep(2.5)
                    driver.find_element(By.ID,"CPH_Body_rpt_PassengerList_lb_ID_NO_"+index).send_keys(passenger_list[i][3]) 
                except:
                    sleep(2.5)
                    driver.find_element(By.ID,"CPH_Body_rpt_PassengerList_lb_ID_NO_"+index).send_keys(passenger_list[i][3])        
            ____tr.session_end()
            driver.send_ScrollDown()

        # fill-in CONTACT  "CONTACT-INFO" : ["0912345678","stanxxxx@gmail.com"]
        ____tr.session_start('fill contact info', 2, '\n')
        sleep(0.5)
        # select mobile country
        ____tr.session_start('select mobile: nation', 3)
        driver.find_element_then_click(By.ID, "CPH_Body_btn_SelectNational_Mobile")
        sleep(5)
        driver.find_element_then_click(By.ID, "CPH_Body_rpt_National_li_item_0")
        sleep(0.5)
        ____tr.session_end()
        # fill-in mobile phone num.
        ____tr.session_start('fill mobile number', 3)
        driver.find_element(By.ID, "CPH_Body_tb_Contact_Mobile_Number").send_keys(INFO["CONTACT-INFO"][0])
        ____tr.session_end()
        ____tr.session_start('fill email add.', 3)
        driver.find_element(By.ID, "CPH_Body_tb_Email").send_keys(INFO["CONTACT-INFO"][1])
        ____tr.session_end()
        driver.find_element_then_click(By.ID, "CPH_Body_btn_NextStep")
        # ----------------------------------------------------------------------------------- #
        # STEP FIVE
        # ----------------------------------------------------------------------------------- #
        ____tr.session_start('start step five',1,'\n')
        ____tr.session_start('select card type',2)
        Select(driver.wait_find_element(By.ID, "CPH_Body_rpt_Payment_ddl_CardType_0")).select_by_visible_text(INFO["CARD-TYPE"])
        sleep(0.5)
        ____tr.session_end()
        ____tr.session_start('fill card num',2)
        driver.find_element(By.ID, "CPH_Body_rpt_Payment_tb_CardNo_0").send_keys(INFO["CARD-NUMBER"])
        sleep(0.5)
        ____tr.session_end()
        ____tr.session_start('select card expired year',2)
        Select(driver.find_element(By.ID, "CPH_Body_rpt_Payment_ddl_CardExpire_M_0")).select_by_visible_text(INFO["DUE-MONTH"])
        sleep(0.5)
        ____tr.session_end()
        ____tr.session_start('select card expired month',2)
        Select(driver.find_element(By.ID, "CPH_Body_rpt_Payment_ddl_CardExpire_Y_0")).select_by_visible_text(INFO["DUE-YEAR"])
        sleep(0.5)
        ____tr.session_end()
        ____tr.session_start('fill CVV',2)
        driver.find_element(By.ID, "CPH_Body_rpt_Payment_tb_CVV_0").send_keys(INFO["CVV"])
        sleep(0.5)
        ____tr.session_end()

        # confirm payment
        ____tr.session_start('press confirm payment',2)
        driver.find_element_then_click(By.ID, "CPH_Body_btn_Payment")
        ____tr.session_end()

    def dump_required_info(self):
        for key in self.INFO_HELP:
            print(key,'\t',self.INFO_HELP[key])
        with open('REQUIRED_INFO.txt', mode='w', encoding='big5') as f:
            json.dump(self.REQUIRED_INFO,f,ensure_ascii=False)
    
    def check_data(self):
        pass