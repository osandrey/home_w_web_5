from datetime import datetime, timedelta
# 03.05.2023

def get_date():
    current_date = datetime.now().date()
    format_date = current_date.strftime('%d-%m-%Y')
    print(format_date)
    return format_date


def get_timedelta(num):
    current_datetime = datetime.now().date()
    data_list = []
    for i in range(1, num+1):
        print(i)
        day_off = current_datetime - timedelta(days=i)
        print(day_off.strftime('%d-%m-%Y'))
        data_list.append(day_off.strftime('%d-%m-%Y'))

    print(data_list)
    return data_list

for i in get_timedelta(2):
    print(i)



    # if num < 10:
    #     num = str(0) + str(num)
    # print(num)





get_date()
get_timedelta(2)