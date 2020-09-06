import datetime as dt
from packing_list import PackingList

trip_name = 'Austin'
start_date = dt.date(2020, 8, 28)
end_date = dt.date(2020, 9, 7)

pl = PackingList(trip_name, start_date, end_date)
print(pl)

print(); print()

pl.load_packing_list_csv('packing_lists/dummy_data.csv')
pl.print_packing_list()

print(); print()

print('Packing Pants...')
pl['Pants'].pack()

pl.write_yaml()

pl2 = PackingList.read_yaml('Austin 2020-08-28 to 2020-09-07.yaml')
print(pl2)

print(PackingList.list_packing_lists())