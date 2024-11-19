import re
from pprint import pprint

def coords_list_inside_lat_lon(input_string) -> list:
    lat_lon_list = ['с.ш.', 'ю.ш.', 'з.д.', 'в.д.', 'сш', 'юш', 'вд', 'зд']
    output_list = []
    for i in range(len(lat_lon_list)):
        if lat_lon_list[i] in input_string:
            output_list.append(lat_lon_list[i])
    return output_list

def coord_to_lat_lon(input_string)-> list:
    names_of_coords = coords_list_inside_lat_lon(input_string)
    output_list = []
    if names_of_coords != []:
        lat_lon_list = re.split(r'\D+.\D', input_string)
        if names_of_coords[0] == 'с.ш.' or names_of_coords[0] == 'сш':
            output_list.append(float(lat_lon_list[0]))
        else:
            output_list.append(-float(lat_lon_list[0]))
        if names_of_coords[1] == 'в.д.' or names_of_coords[1] == 'вд':
            output_list.append(float(lat_lon_list[1]))
        else:
            output_list.append(-float(lat_lon_list[1]))
    return output_list
pprint(coord_to_lat_lon(input_string))