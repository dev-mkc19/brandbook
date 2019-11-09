from lxml import etree



def add_entry(dict, key, value = None):
    if key in dict: # если ключ существует
        if value == None:
            pass
            #'ключ есть, новое значение None - пропускаем'
            return dict
        else:
            if dict.get(key) == None:
                dict.update({key: [value]})
                #'ключ есть, старое значение None - добавляем не None'
                return dict
            else:
                old_value = dict.get(key)
                old_value.append(value)
                dict.update({key: old_value})
                #'ключ есть, старое значение не None - добавляем в список'
                return dict
    else:
        if value == None:
            dict.update({key: value})
            #'ключa нет - добавляем None'
            return dict
        else:
            dict.update({key: [ value]})
            #'ключa нет - добавляем'
            return dict



def HeaderCheck(filename):
    result = {}
    tree = etree.parse(filename)
    root = tree.getroot()
    for dashboard in root.iter('dashboard'): #проходим по каждой ноде <dashboard>
        header_check = list()

        for zones in dashboard.iter('zones'): #ищем первую ноду с именем <zones>

            for item in zones.getchildren():
                if item.get('type') == 'layout-basic': # проеряем тип зоны, чтобы исключить floating контейнеры

                    child = item.find('zone') #vert container
                    header_check.append(child.attrib)


                    if child.find('zone') != None: # проверка структуры заголовка
                        sub_child = child.find('zone') #horz container
                        header_check.append(sub_child.attrib)

                        # проверка структуры заголовка
                        if header_check[0].get('param') == 'vert' and header_check[1].get('param') == 'horz':
                            result = add_entry(key = 'Заголовок', dict = result)
                        else:
                            result = add_entry(key = 'Заголовок', value = ' в дашборде "{}" структура не соответствует'.format(dashboard.get('name')) , dict = result)

                        # проверка высоты заголовка
                        if int(header_check[1].get('fixed-size')) == 44:
                            result = add_entry(key = 'Заголовок', dict = result)
                        else:
                            result = add_entry(key = 'Заголовок', value = ' в дашборде "{}" высота не равна 44px'.format(dashboard.get('name')) , dict = result)

                        # проверка ширины логотипа
                        logo = sub_child.find('zone')

                        try:
                            if int(logo.get('fixed-size')) == 105:
                                result = add_entry(key = 'Заголовок', dict = result)
                            else:
                                result = add_entry(key = 'Заголовок', value = ' в дашборде "{}" ширина логотипа не равна 105px'.format(dashboard.get('name')), dict = result )
                        except:
                            result = add_entry(key = 'Заголовок', value = ' в дашборде "{}" проверка ширины логотипа не удалась'.format(dashboard.get('name')), dict = result )

                        # проверка отступов логотипа
                        try:
                            if int(logo.find('..//zone-style/format[@attr="margin"]').get('value')) == 12:
                                result = add_entry(key = 'Заголовок')
                            else:
                                result = add_entry(key = 'Заголовок', value = ' в дашборде "{}" внешние отступы логотипа не равны 12px'.format(dashboard.get('name')), dict = result )
                        except:
                            result = add_entry(key = 'Заголовок', value = ' в дашборде "{}" проверка отступов логотипа не удалась'.format(dashboard.get('name')), dict = result )

                        # проверка центровки логотипа
                        try:
                            if int(logo.get('is-centered')) == 0:
                                result = add_entry(key = 'Заголовок', value = ' в дашборде "{}" у логотипа не не стоит флаг "Center Image"'.format(dashboard.get('name')), dict = result )
                            else:
                                pass
                        except:
                            result = add_entry(key = 'Заголовок', dict = result)

                        # проверка Fit Image логотипа
                        try:
                            if int(logo.get('is-scaled')) == 1:
                                result = add_entry(key = 'Заголовок', dict = result)
                            else:
                                result = add_entry(key = 'Заголовок', value = ' в дашборде "{}" у логотипа не не стоит флаг "Fit Image"'.format(dashboard.get('name')), dict = result )
                        except:
                            result = add_entry(key = 'Заголовок', value = ' в дашборде "{}" проверка параметра "Fit Image" не удалась'.format(dashboard.get('name')), dict = result )

                        # проверка фона #565C61
                        if sub_child.find('..//zone-style/format[@attr="background-color"]').get('value').upper() == '#565C61':
                            result = add_entry(key = 'Заголовок', dict = result)
                        else:
                            result = add_entry(key = 'Заголовок', value = ' в дашборде "{}" у заголовка фон не "#565C61" '.format(dashboard.get('name')), dict = result )

                    else:
                        result = add_entry(key = 'Заголовок', value = ' в дашборде "{}" структура не соответствует'.format(dashboard.get('name')) , dict = result)


                else:
                    pass
    return result
