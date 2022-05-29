def refine_date(DATE):
    """
    refine date input to list

    :args::
    `DATE:str` = 'YYYY-mm-dd'

    rtype::
    `list` = ['YYYY','mm','dd] mm:CHT
    """
    def month_num2cht(num):
        month = {   "01":"一月",
                    "02":"二月",
                    "03":"三月",
                    "04":"四月",
                    "05":"五月",
                    "06":"六月",
                    "07":"七月",
                    "08":"八月",
                    "09":"九月",
                    "10":"十月",
                    "11":"十一月",
                    "12":"十二月"
                }
        return month[num]
    YYYY = DATE[:4]
    mm = month_num2cht(DATE[5:7])
    dd = DATE[8:]
    if dd[0] == "0":
        dd = dd[1:]
    return [YYYY,mm,dd]

def process_flight_info(web_flight_info, DEPARTURE):
    departure_time_list = []
    web_flight_info = list(filter(('無可售機位').__ne__, web_flight_info))
    for i in range(0,len(web_flight_info)):
        if i % 5 == 1:
            departure_time_list.append(web_flight_info[i])
    index = str(departure_time_list.index(DEPARTURE))    
    return  index

def process_passenger_list(INFO):
    raw_passenger_list = INFO["PASSENGER-LIST"]
    passenger_list = []
    fare_type = ["FULLPRICE", "ELDER", "CHILDREN", "MILITARY", "DISABLE", "DISABLE-COMP", "RESIDENT", "RE-ELDER", "RE-DISABLE", "RE-DISABLE-COMP"]
    type_list = []    
    for type_ in fare_type:
        for q in range(INFO[type_]):
            type_list.append(type_)
    for i in range(INFO["PEOPLE"]):
        person_info = []
        raw_info = raw_passenger_list[i].split('_')
        for j in range(4):
            person_info.append(raw_info[j])
        person_info.append(refine_date(raw_info[-1]))
        # fare_type
        person_info.append(type_list[i])
        passenger_list.append(person_info)    
    return passenger_list

def is_birthday_correct(value:str, INFO, index):
    return value == INFO["PASSENGER-LIST"][index].replace('-','/').split('_')[-1]

from datetime import datetime
class TraceReporter:
    def __init__(self, debug_flag:bool=False):
        self.report = ''
        self.debug_flag = debug_flag

    def session_start(self, text:str, level:int, end=''):
        if self.debug_flag:
            time = datetime.now().strftime('[%H:%M:%S]')
            msg = time + '\t' * level +  ' - ' + text + ' '
            print(msg, end=end)
            self.report = self.report + msg + end
            self.dump()
        

    def session_end(self, msg:str='...done'):
        if self.debug_flag:
            print(msg)
            self.report = self.report + msg + '\n'
            self.dump()

    def session_statement(self, text:str):
        if self.debug_flag:
            msg = text 
            self.report = self.report + msg
            self.dump()

    def dump(self):
        with open('TraceReporter.txt', mode='w') as f:
            f.write(self.report)