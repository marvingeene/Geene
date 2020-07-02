import xlsxwriter

class Birthday():
    def __init__(self, name, day, month):
        self.name = name
        self.day = day
        self.month = month



def getEntriesMonthSorted(listToSort, month):
    returnValue = []
    for birthday in listToSort:
        if(int(birthday.month) == month):
            returnValue.append(birthday)
    return sorted(returnValue, key = lambda x: x.day)

def createEntriesMonth(month):
    entries_month = getEntriesMonthSorted(birthdays, month)
    starting_row = start_of_row[rows[month]]+1
    column = columns.get(month)
    for birthday in range(row_count[rows[month]]):
        try:
            birthday_entry = entries_month[birthday]
            worksheet.write(starting_row+birthday, column, int(birthday_entry.day), default_cell_format)
        except:
            birthday_entry = Birthday("","","")
            worksheet.write(starting_row+birthday, column, "", default_cell_format)
        worksheet.write(starting_row+birthday, column+1, birthday_entry.name, default_cell_format)


#This is the beginning
#Create an excel file and a worksheet in it.
workbook = xlsxwriter.Workbook('geburtstage.xlsx')
worksheet = workbook.add_worksheet()


birthdays = []

#open the file
with open("geburtstage.txt", "r") as f:
    #for each row extract the information into a birthday object
    for birthday_line in f:
        #name is everything before the last space
        birthday_info = birthday_line.rsplit(" ", 1)
        birthday_name = birthday_info[0]
        #split the date on a dot.
        birthday_date = birthday_info[1].split(".", 1)
        birthday_day = birthday_date[0]
        #remove the end of line symbol
        birthday_month = birthday_date[1].replace("\n","")

        birthdays.append(Birthday(birthday_name, birthday_day, birthday_month))

#initialize the month count array and map which row a month belongs to and in which column it starts.
month_count = {1 : 0, 2 : 0, 3 : 0, 4 : 0, 5 : 0, 6 : 0, 7 : 0, 8 : 0, 9 : 0, 10 : 0,  11 : 0, 12 : 0}
rows = {1 : 1, 2 : 1, 3 : 1, 4 : 2, 5 : 2, 6 : 2, 7 : 3, 8 : 3, 9 : 3, 10 : 4,  11 : 4, 12 : 4}
columns = {1 : 0, 2 : 2, 3 : 4, 4 : 0, 5 : 2, 6 : 4, 7 : 0, 8 : 2, 9 : 4, 10 : 0,  11 : 2, 12 : 4}
    

#check how many entries there are per month.
for birthday in birthdays:
    month_count[int(birthday.month)] += 1

#save how many data entries is the maximum for each month row.
row_count = {
    1 : max(month_count[1], month_count[2], month_count[3])+1,
    2 : max(month_count[4], month_count[5], month_count[6])+1,  
    3 : max(month_count[7], month_count[7], month_count[9])+1,
    4 : max(month_count[10], month_count[11], month_count[12])        
}

#format for the headers, bold letters, centered across the merged cells, background color light grey.
header_format = workbook.add_format()
header_format.set_bg_color("#bfbfbf")
header_format.set_center_across()
header_format.set_border()
header_format.set_bold()

#default cell format, set borer and center 
default_cell_format = workbook.add_format()
default_cell_format.set_border()
default_cell_format.set_align("center")

#set the widhts of columns a-f (width in cm)
#3.57cm = 30px
worksheet.set_column(0,0, 3.57)
worksheet.set_column(2,2, 3.57)
worksheet.set_column(4,4, 3.57)

#13.57cm = 100px
worksheet.set_column(1,1, 13.57)
worksheet.set_column(3,3, 13.57)
worksheet.set_column(5,5, 13.57)


#in which row should the next month row start.
row_1 = 0
row_2 = row_1 + row_count[1]+1
row_3 = row_2 + row_count[2]+1
row_4 = row_3 + row_count[3]+1

#save the starting rows in a map to access them easily.
start_of_row = {1:row_1, 2:row_2, 3:row_3, 4:row_4}

#create the month headers and create the data entries.
worksheet.merge_range(row_1, 0, row_1, 1, "Januar", header_format)
createEntriesMonth(1)
worksheet.merge_range(row_1, 2, row_1, 3, "Februar", header_format)
createEntriesMonth(2)
worksheet.merge_range(row_1, 4, row_1, 5, "März", header_format)
createEntriesMonth(3)
worksheet.merge_range(row_2, 0, row_2, 1, "April", header_format)
createEntriesMonth(4)
worksheet.merge_range(row_2, 2, row_2, 3, "Mai", header_format)
createEntriesMonth(5)
worksheet.merge_range(row_2, 4, row_2, 5, "Juni", header_format)
createEntriesMonth(6)
worksheet.merge_range(row_3, 0, row_3, 1, "Juli", header_format)
createEntriesMonth(7)
worksheet.merge_range(row_3, 2, row_3, 3, "August", header_format)
createEntriesMonth(8)
worksheet.merge_range(row_3, 4, row_3, 5, "September", header_format)
createEntriesMonth(9)
worksheet.merge_range(row_4, 0, row_4, 1, "Oktober", header_format)
createEntriesMonth(10)
worksheet.merge_range(row_4, 2, row_4, 3, "Novemeber", header_format)
createEntriesMonth(11)
worksheet.merge_range(row_4, 4, row_4, 5, "Dezember", header_format)
createEntriesMonth(12)

#close the workbook to save the file
workbook.close()
        



