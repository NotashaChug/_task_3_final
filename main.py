from astropy.io import fits
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import numpy as np
import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication,QMainWindow,QFileDialog,QGridLayout,QDialog


def application(): #функция запуска приложения

    # создаем глобальные переменые с данными введеными пользавателем
    global CutX,CutY,grafik_3d
    global koordinat_X,koordinat_Y,radius
    global data,window

    app = QApplication(sys.argv) #создаем приложение
    window = QMainWindow()     #оздаем окно
    window.setWindowTitle('Приложение') #название окна
    window.setGeometry(150,150,1000,500) #смещение и размеры
    image_widget = QtWidgets.QWidget(window) #виджет для размещения изображения
    image_widget.setGeometry(0, 0, 600, 500)
    choose_widget = QtWidgets.QWidget(window) #виджет для размещения кнопок полей ввода
    choose_widget.setGeometry(600,0,400,500)
    grid_image = QGridLayout() #создаем сетчатое выравнивание для виджета с картинкой
    grid_choose = QGridLayout() #создаем сетчатое выравнивание для виджета с полями ввода и кнопками

    #хотим запросить расположение файла и вывести картинку в приложении
    file_path=QFileDialog.getOpenFileName(window, 'Открыть файл fit')[0] #спрашиваем путь
    image = fits.open(file_path)  # читаем файл
    data = image[0].data  # вытаскиваем список числовых данных

    figure = Figure(figsize=(40, 40)) # создаем холст где будет рисоваться график
    axes = figure.add_subplot(111)
    canvas = FigureCanvas(figure)
    navToolbar = NavigationToolbar(canvas) # добавляем навигационую панель
    axes.imshow(data, cmap="gray", vmin=1E3, vmax=2E3)  # наша картинка
    grid_image.addWidget(canvas, 1, 0) # добавляем график и нвигационую панель в сетку выравнивания
    grid_image.addWidget(navToolbar, 0, 0)

    # создадим поля ввода, чекбоксы и кнопки

    # поля ввода для запроса координат выбраной звезды
    koordinat_labelX = QtWidgets.QLabel(choose_widget) # создали текст в виджете
    koordinat_labelX.setText('Координаты звезды  X:') # написали отображаемый текст
    koordinat_labelX.adjustSize() # задали отображение во весь размер
    grid_choose.addWidget(koordinat_labelX,0,0) # привизали к сетке выравнивания
    koordinat_X = QtWidgets.QLineEdit(choose_widget)
    koordinat_X.setFixedWidth(50) # задание фиксированиго размера
    grid_choose.addWidget(koordinat_X,0,1)
    koordinat_labelY = QtWidgets.QLabel(choose_widget)
    koordinat_labelY.setText("      Y:")
    koordinat_labelY.adjustSize()
    grid_choose.addWidget(koordinat_labelY,0,2)
    koordinat_Y = QtWidgets.QLineEdit(choose_widget)
    koordinat_Y.setFixedWidth(50)
    grid_choose.addWidget(koordinat_Y,0,3)

    # поля ввода для запроса радиуса звезды
    radius_label = QtWidgets.QLabel(choose_widget)
    radius_label.setText('Радиус звезды: ')
    radius_label.adjustSize()
    grid_choose.addWidget(radius_label,1,0)
    radius = QtWidgets.QLineEdit(choose_widget)
    radius.setFixedWidth(50)
    grid_choose.addWidget(radius,1,1)

    # чекбоксы
    CutX = QtWidgets.QCheckBox("показать график среза по оси Ox",choose_widget) # создание чекбокса
    grid_choose.addWidget(CutX,2,0,1,2) #виджет начинается в ячейке 2,0 и занимает 1 строку и 2 колоны
    CutX.adjustSize()
    CutY = QtWidgets.QCheckBox("показать график среза по оси Oy",choose_widget)
    grid_choose.addWidget(CutY,3,0,1,2)
    CutY.adjustSize()
    grafik_3d = QtWidgets.QCheckBox("показать 3D профиль",choose_widget)
    grid_choose.addWidget(grafik_3d,4,0,1,2)
    grafik_3d.adjustSize()

    # кнопка
    button_show_results=QtWidgets.QPushButton(choose_widget) # создание кнопки
    grid_choose.addWidget(button_show_results,5,3)
    button_show_results.setText("Показать") # надпись на кнопке

    #соеденение действия "нажатие на кнопку" и выполнения заданной функции
    button_show_results.clicked.connect(push_button)

    image_widget.setLayout(grid_image)
    choose_widget.setLayout(grid_choose)
    window.show()
    sys.exit(app.exec_())


def push_button():

    window_results = QDialog(window) # создаем новое окно для отображения результата запроса пользователя
    window_results.setWindowTitle('Результаты запроса') #название окна
    window_results.setGeometry(150,150,1000,500) #смещение и размеры
    widget_results = QtWidgets.QWidget(window_results) # создали виджет результатов
    widget_results.setGeometry(0,0,1000,500)
    grid_results = QGridLayout() # создали сетчатое выравнивание для виджета результатов

    # вытаскиваем значения введеные пользователем
    koordinat_X_znach = int(koordinat_X.text())
    koordinat_Y_znach = int(koordinat_Y.text())
    radius_znach = int(radius.text())

    # проверим отмеченые чекбоксы и выведим соответствующие графики в виджет результатов
    count = 0 # зададим счетчик кол-ва выбраных чекбоксов
    if CutX.isChecked() == True:
        figure_CutX = Figure(figsize=(20,20 )) # создаем холст где будет рисоваться график
        axes_CutX = figure_CutX.add_subplot(111)
        canvas_CutX = FigureCanvas(figure_CutX)

        #выделим данные для построения графика
        Ox = list(range(koordinat_X_znach-radius_znach,koordinat_X_znach+radius_znach+1))
        Oz = data[koordinat_Y_znach][(koordinat_X_znach-radius_znach):(koordinat_X_znach+radius_znach+1)]

        #создаем подпись к графику
        title_СutX = 'Срез звезды с координатами (' + str(koordinat_X_znach) + ',' + str(koordinat_Y_znach) + ') по оси X'
        axes_CutX.set_title(title_СutX)

        axes_CutX.plot(Ox,Oz,'-r')  # наш график
        grid_results.addWidget(canvas_CutX, 1, count) # добавляем график в сетку выравнивания
        print(count)
        count=count+1

    if CutY.isChecked() == True:
        figure_CutY = Figure(figsize=(20, 20)) # создаем холст где будет рисоваться график
        axes_CutY = figure_CutY.add_subplot(111)
        canvas_CutY = FigureCanvas(figure_CutY)

        #выделим данные для построения графика
        Oy = list(range(koordinat_Y_znach-radius_znach,koordinat_Y_znach+radius_znach+1))
        Oz=[]
        for i in range(koordinat_Y_znach-radius_znach,koordinat_Y_znach+radius_znach+1):
            Oz.append(data[i][koordinat_X_znach])

        #создаем подпись к графику
        title_СutY = 'Срез звезды с координатами (' + str(koordinat_X_znach) + ',' + str(koordinat_Y_znach) + ') по оси Y'
        axes_CutY.set_title(title_СutY)

        axes_CutY.plot(Oy,Oz,'b-')  # наш график
        grid_results.addWidget(canvas_CutY, 1, count) # добавляем график в сетку выравнивания
        print(count)
        count=count+1

    if grafik_3d.isChecked() == True:
        figure_grafik_3d = Figure(figsize=(20, 20)) # создаем холст где будет рисоваться график
        axes_grafik_3d = figure_grafik_3d.add_subplot(111, projection="3d")
        canvas_grafik_3d = FigureCanvas(figure_grafik_3d)
        title_grafik_3d = '3-х мерный график звезды с координатами ('+str(koordinat_X_znach)+','+str(koordinat_Y_znach)+')'
        axes_grafik_3d.set_title(title_grafik_3d)

        #пространство заначений для х и y
        Ox = list(range(koordinat_X_znach-radius_znach,koordinat_X_znach+radius_znach+1))
        Oy = list(range(koordinat_Y_znach-radius_znach,koordinat_Y_znach+radius_znach+1))
        X,Y = np.meshgrid(Ox,Oy) # создаем сетку значений

        Z = np.zeros((len(Ox),len(Oy))) #заполняем данный массив значениями по оси Oz.
        for i in range(len(Oy)):      #как бы смотря на пл-ть xOy сверху
            for j in range(len(Ox)):  #точка (x-d,y-d) в левом верхнем углу
                Z[i][j]=data[Oy[i]][Ox[j]]

        axes_grafik_3d.plot_surface(X,Y,Z,cmap='cividis')
        grid_results.addWidget(canvas_grafik_3d,1,count)
        print(count)
        count=count+1

    # расчитаем светимость звезды и выведим ее в виджет результатов
    star_svetimost = str(svetimost(koordinat_X_znach,koordinat_Y_znach,radius_znach))
    star_svetimost_label = QtWidgets.QLabel(widget_results)
    star_svetimost_label.setText('Cветимость звезды :   ' + star_svetimost)
    grid_results.addWidget(star_svetimost_label,0,0,1,count)
    star_svetimost_label.setAlignment(QtCore.Qt.AlignHCenter)
    widget_results.setLayout(grid_results)
    window_results.show()



def svetimost(x,y,R): # функция расчета светимости
    svet_star_ishod = 0
    square_star = 0
    svet_fon = 0
    square_fon = 0
    for i in range(x-R,x+R):
        for j in range(y-R,y+R):
            if (i-x)**2+(j-y)**2 <= R**2:
                svet_star_ishod=svet_star_ishod+data[j][i]
                square_star=square_star+1
    for i in range(x-R*2,x+R*2):
        for j in range(y-R*2,y+R*2):
            if (i-x)**2+(j-y)**2 >= R**2 and (i-x)**2+(j-y)**2 <= (R*2)**2:
                 svet_fon=svet_fon+data[j][i]
                 square_fon=square_fon+1
    svet_star=svet_star_ishod-square_star*(svet_fon/square_fon)
    return svet_star

if __name__ == '__main__': #при запуске программы - запускается  приложение
    application()

