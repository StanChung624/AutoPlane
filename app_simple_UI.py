from script_UniAir import UniAir
# -----------------------------------------------------------------------------#
# Initiate
# -----------------------------------------------------------------------------#
crawler = UniAir()
# -----------------------------------------------------------------------------#
# dump REQUIREMENT_INFO.txt for editing
# -----------------------------------------------------------------------------#
crawler.dump_required_info()
print("'REQUIREMENT_INFO.txt' has been created, please modify the INFO then save the file.")
print(" press Enter when done...")
input()
# -----------------------------------------------------------------------------#
# read INFO.txt
# -----------------------------------------------------------------------------#
crawler.read_info()
# -----------------------------------------------------------------------------#
# start when
# -----------------------------------------------------------------------------#
print('When should it begin to crawl? in the format of YYYY-mm-dd_HH:mm (ex. 2022-06-24_20:20)')
print('(Press Enter to start immediately.)')
start_when = str(input(":"))
if start_when == '':
    crawler.run()
else:
    crawler.run(start_when=start_when)
