import numpy as np
import matplotlib.pyplot as plt
import matplotlib
#from scipy.interpolate import interp1d
from PIL import Image

matplotlib.use('TkAgg') #Интерактивный режим работает должным образом

# Открытие картинки
def load_image(filename):
    img = Image.open(filename).convert('RGB')
    return np.array(img)

def map_color_2_evelation(rgb_image):
    evelation_colors ={
        (255, 0, 0):     307,   #Красный для 307 м
        (255, 69, 0):    293,   #Оражнево-красный для 293 м
        (255, 165, 0):   266,   #Оранжевый для 266 м
        (255, 255, 0):   240,   #Желтый для 240 м
        (253, 216, 53):  228,   #Светло-желтый для 228 м
        (173, 255, 47):  217,   #Желто-зеленый для 217 м
        (0, 255, 0):     195,   #Зеленый для 195 м
        (0, 200, 0):     185,   #Зеленый потемнее для 185 м
        (34, 139, 34):   175,   #Лесной зеленый для 175 м
        (0, 128, 0):     166,   #Темно-зеленый для 166 м
        (85, 107, 47):   150,   #Оливково-зеленый для 150 м
        (0, 206, 209):   137,   #Темно-голубой для 137 м
        (0, 255, 255):   132,   #Голубой для 132 м
        (0, 191, 255):   128,   #Глубокий небесно-голубой для 128 м
        (70, 130, 180):  126,   #Стальной синий для 126 м
        (0, 0, 128):     120,   #Формы морских офицеров для 120 м
        (0, 0, 0):       0,     #Черный для 0 м
    }

    color_keys = np.array(list(evelation_colors.keys()))
    elevation_values = np.array(list(evelation_colors.values()))

    def rgb_2_elevation(rgb):
        distances = np.linalg.norm(color_keys-rgb,axis=1)
        closest_index = distances.argsort()[:5] # Получить пять ближайших цветов
        weights = 1 /(distances[closest_index]+1e-5) # Взвешивание обратного расстояния с небольшим смещением
        weights /= weights.sum() # Нормализовать веса
        interpolated_elevation = np.dot(weights, elevation_values[closest_index])
        return interpolated_elevation

    elevation_map = np.zeros(rgb_image.shape[:2])
    for i in range(rgb_image.shape[0]):
        for j in range(rgb_image.shape[1]):
            rgb = rgb_image[i,j]
            elevation_map[i,j] = rgb_2_elevation(rgb)
    return elevation_map

def on_click(event, points):
    if event.xdata and event.ydata and event.button == 1:
        points.append((int(event.xdata), int(event.ydata)))
        print(f'Point selected: {int(event.xdata)}, {int(event.ydata)}')
    if len(points) == 2:
        plt.close()

def get_line_points(p1, p2):
    x_values = np.linspace(p1[0], p2[0], num=500)
    y_values = np.linspace(p1[1], p2[1], num=500)
    return np.column_stack((x_values, y_values))

def extract_elevation_profile(elevation_map, line_points):
    profile = []
    for x,y in line_points:
        if 0 <= int(y) < elevation_map.shape[0] and 0 <= int(x) < elevation_map.shape[1]:
            elevation = elevation_map[int(y), int(x)]
            profile.append(elevation)
    return np.array(profile)

#Программа
image_name =f'image.png' # лежит в той же папке, что и main.py
rgb_image = load_image(image_name)
elevation_map = map_color_2_evelation(rgb_image)

# Показываем, что загрузил пользователь
fig, ax = plt.subplots()
ax.imshow(rgb_image)
ax.set_title('Левой кнопной кликните 2 раза для выбора точек')

points = []
cid = fig.canvas.mpl_connect('button_press_event', lambda event: on_click(event, points))
plt.show() # Ждем, когда пользователь выберет две точки

while len(points) < 2:
    plt.pause(0.1)

if len(points) == 2:
    # Получаем точки на линии
    line_points = get_line_points(points[0], points[1])

    # Извлечение профиля высот
    elevation_profile = extract_elevation_profile(elevation_map, line_points)

    # Создаем массив расстояний для оси x
    distance = np.linspace(0, len(elevation_profile), num=len(elevation_profile))

    plt.figure()
    plt.plot(distance, elevation_profile, label='Профиль высот', color='green')
    plt.title('Профиль высот по линии')
    plt.xlabel('Расстояние')
    plt.ylabel('Высота')
    plt.grid(True)
    plt.legend()
    plt.show()

    # Численная аппроксимация с использованием полиномиальной подгонки
    poly_fit = np.polyfit(distance, elevation_profile, deg=15)
    poly_func = np.poly1d(poly_fit)

    plt.figure()
    plt.plot(distance, elevation_profile, 'o', label='Оригинальные данные', markersize=2)
    plt.plot(distance, poly_func(distance), '-', label='Полиномиальная аппроксимация (степень=15)', color='red')
    plt.title('Полиномиальная аппроксимация профиля рельефа')
    plt.xlabel('Дистанция (произвольные единицы)')
    plt.ylabel('Высота (метры)')
    plt.grid(True)
    plt.legend()
    plt.show()
else:
    print("Error: Обязательно выберите две точки.")