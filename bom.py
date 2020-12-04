import csv

# init var setup
_itemName = []
_level = []
_rawMaterial = []
_quantity = []
_unit = []

# read data from CSV File and store them in their respective  list
with open('bom.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        if line_count >= 0:
            _itemName.append(row["Item Name"])
            _level.append(int(row['Level'].replace('.', '')))  # replace dot and type cast level value to integer
            _rawMaterial.append(row['Raw material'])
            _quantity.append(row['Quantity'])
            _unit.append(row['Unit '])
        line_count += 1

# get top level item 
_uniqueItems = set(_itemName)

# get all unique level
_uniqueLevels = []
for lvl in _level:
    if lvl not in _uniqueLevels:
        _uniqueLevels.append(lvl)

# sort to make it easy for later maths
_uniqueLevels.sort()

# loop through the top level item items and 
# make their respective BOM files
counter = 0
for item in _uniqueItems:
    filename = item
    with open(f'{filename}.csv', mode='w') as f:
        info_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        info_writer.writerow(['Finished Good List'])
        fieldnames = ['#', 'Item Description', 'Quantity', 'Unit']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({'#': 1, 'Item Description': filename, 'Quantity': 1, 'Unit': 'Pc'})

        info_writer.writerow(['End Of FG'])
        info_writer.writerow(['Raw Material List'])
        writer.writeheader()

        row = 0
        serial = 1
        for uniLevel in _uniqueLevels:
            for level in _level:
                if uniLevel > 1:
                    if _itemName[row] == item and _level[row] == uniLevel:
                        _list = []
                        for i in reversed(range(row)):
                            _list.append(i + 1)
                            if _level[i] == uniLevel - 1:
                                rm_filename = _rawMaterial[i]
                                with open(f'{rm_filename}.csv', mode='w') as rmf:
                                    rm_info_writer = csv.writer(rmf, delimiter=',', quotechar='"',
                                                                quoting=csv.QUOTE_MINIMAL)
                                    rm_info_writer.writerow(['Finished Good List'])
                                    rm_fieldnames = ['#', 'Item Description', 'Quantity', 'Unit']
                                    rm_writer = csv.DictWriter(rmf, fieldnames=rm_fieldnames)
                                    rm_writer.writeheader()
                                    rm_writer.writerow(
                                        {'#': 1, 'Item Description': rm_filename, 'Quantity': _quantity[i],
                                         'Unit': _unit[i]})

                                    rm_info_writer.writerow(['End Of FG'])
                                    rm_info_writer.writerow(['Raw Material List'])
                                    rm_writer.writeheader()

                                    rm_serial = 1
                                    for product_serial in _list:
                                        rm_writer.writerow({'#': rm_serial,
                                                            'Item Description': _rawMaterial[product_serial],
                                                            'Quantity': _quantity[product_serial],
                                                            'Unit': _unit[product_serial]
                                                            })
                                        rm_serial += 1
                                break
                else:
                    if _itemName[row] == item and _level[row] == 1:
                        writer.writerow({'#': serial, 'Item Description': _rawMaterial[row], 'Quantity': _quantity[row],
                                         'Unit': _unit[row]})
                        serial += 1
                row += 1
            row = 0
        info_writer.writerow(['End Of RM'])
    counter += 1
