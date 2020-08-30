import datetime as dt
from packing_list import PackingList

trip_name = 'Austin'
start_date = dt.date(2020, 8, 28)
end_date = dt.date(2020, 9, 7)

pl = PackingList(trip_name, start_date, end_date)
print(pl)

print(); print()

pl.load_packing_list_csv('dummy_data.csv')
pl.print_packing_list()

print(); print()

print('Packing Pants...')
pl['Pants'].pack()

pl.write_yaml('austin.yaml')