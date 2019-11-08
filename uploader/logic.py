from lxml import etree

result = {}

def add_entry(key, value=None):
    if key in result: # если ключ существует
        if value == None:
            pass
            return 'ключ есть, новое значение None - пропускаем'
        else:
            if result.get(key) == None:
                result.update({key: [value]})
                return 'ключ есть, старое значение None - добавляем не None'
            else:
                old_value = result.get(key)
                old_value.append(value)
                result.update({key: old_value})
                return 'ключ есть, старое значение не None - добавляем в список'
                print(result[key], result.get(key))
    else:
        if value == None:
            result.update({key: value})
            return 'ключa нет - добавляем None'
        else:
            result.update({key: [value]})
            return 'ключa нет - добавляем'



def HeaderCheck(filename):

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
                            add_entry('Заголовок')
                        else:
                            add_entry('Заголовок', ' в дашборде "{}" структура не соответствует'.format(dashboard.get('name')) )

                        # проверка высоты заголовка
                        if int(header_check[1].get('fixed-size')) == 44:
                            add_entry('Заголовок')
                        else:
                            add_entry('Заголовок', ' в дашборде "{}" высота не равна 44px'.format(dashboard.get('name')) )

                        # проверка ширины логотипа
                        logo = sub_child.find('zone')

                        try:
                            if int(logo.get('fixed-size')) == 105:
                                add_entry('Заголовок')
                            else:
                                add_entry('Заголовок', ' в дашборде "{}" ширина логотипа не равна 105px'.format(dashboard.get('name')) )
                        except:
                            add_entry('Заголовок', ' в дашборде "{}" проверка ширины логотипа не удалась'.format(dashboard.get('name')) )

                        # проверка отступов логотипа
                        try:
                            if int(logo.find('..//zone-style/format[@attr="margin"]').get('value')) == 12:
                                add_entry('Заголовок')
                            else:
                                add_entry('Заголовок', ' в дашборде "{}" внешние отступы логотипа не равны 12px'.format(dashboard.get('name')) )
                        except:
                            add_entry('Заголовок', ' в дашборде "{}" проверка отступов логотипа не удалась'.format(dashboard.get('name')) )

                        # проверка центровки логотипа
                        try:
                            if int(logo.get('is-centered')) == 0:
                                add_entry('Заголовок', ' в дашборде "{}" у логотипа не не стоит флаг "Center Image"'.format(dashboard.get('name')) )
                            else:
                                pass
                        except:
                            add_entry('Заголовок')

                        # проверка Fit Image логотипа
                        try:
                            if int(logo.get('is-scaled')) == 1:
                                add_entry('Заголовок')
                            else:
                                add_entry('Заголовок', ' в дашборде "{}" у логотипа не не стоит флаг "Fit Image"'.format(dashboard.get('name')) )
                        except:
                            add_entry('Заголовок', ' в дашборде "{}" проверка параметра "Fit Image" не удалась'.format(dashboard.get('name')) )

                        # проверка фона #565C61
                        if sub_child.find('..//zone-style/format[@attr="background-color"]').get('value').upper() == '#565C61':
                            add_entry('Заголовок')
                        else:
                            add_entry('Заголовок', ' в дашборде "{}" у заголовка фон не "#565C61" '.format(dashboard.get('name')) )

                    else:
                        add_entry('Заголовок', ' в дашборде "{}" структура не соответствует'.format(dashboard.get('name')) )


                else:
                    pass
    return result
