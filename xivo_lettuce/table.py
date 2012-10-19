# -*- coding: UTF-8 -*-


def extract_webi_talbe_to_dict(table):
    list_tr = table.find_elements_by_tag_name('tr')

    headers_line = list_tr.pop(0)
    headers = _extract_th_from_tr_element(headers_line)

    lines = list()
    for tr_element in list_tr:
        td_elements = tr_element.find_elements_by_tag_name('td')
        td_elements_text = [td_element.text.strip() for td_element in td_elements]
        if len(td_elements_text) > 1:
            line_dict = dict(zip(headers, td_elements_text))
            lines.append(line_dict)

    return lines


def _extract_td_from_tr_elements(list_tr, headers, expected_headers):
    lines = list()
    for tr_element in list_tr:
        td_elements = tr_element.find_elements_by_tag_name('td')
        td_elements_text = [td_element.text.strip() for td_element in td_elements]
        line_dict = dict(zip(headers, td_elements_text))
        lines.append(line_dict)
    return lines


def _extract_th_from_tr_element(tr_element):
    header_th = tr_element.find_elements_by_tag_name('th')
    return [header.text.strip() for header in header_th]
