hex_color = input('Enter hex: ').lstrip('#')
print('RGB =', tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4)))