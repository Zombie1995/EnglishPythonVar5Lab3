import tkinter as tk
from tkinter import PhotoImage, ttk
import math
import time
import os
import random
import string

class KeyGenerator:
    """Класс для генерации ключей по варианту 5"""
    
    def __init__(self):
        self.alphabet = string.ascii_uppercase + string.digits
    
    def shift_char(self, char, shift):
        """Сдвигает символ на заданное количество позиций в алфавите"""
        if char in self.alphabet:
            current_index = self.alphabet.index(char)
            new_index = (current_index + shift) % len(self.alphabet)
            return self.alphabet[new_index]
        return char
    
    def generate_random_block(self):
        """Генерирует случайный блок из 5 символов"""
        return ''.join(random.choice(self.alphabet) for _ in range(5))
    
    def validate_block(self, block):
        """Возвращает пустой, если неправильно"""
        block = block.upper().strip()
        if len(block) != 5 or not all(c in self.alphabet for c in block):
            return ""
        return block
    
    def generate_key(self, input_block):
        """
        Генерирует ключ по правилу варианта 5:
        блок 2 – сдвиг на 3 символа вправо
        блок 3 – сдвиг на 5 символов влево
        """
        # Валидируем входной блок
        block1 = self.validate_block(input_block)
        
        # Блок 2: сдвиг на 3 позиции вправо
        block2 = ''.join(self.shift_char(char, 3) for char in block1)
        
        # Блок 3: сдвиг на 5 позиций влево
        block3 = ''.join(self.shift_char(char, -5) for char in block1)
        
        return f"{block1}-{block2}-{block3}", block1
    
    def generate_and_update_ui(self, entry_widget, key_var):
        """Генерирует ключ и обновляет UI элементы"""
        input_block = entry_widget.get()
        full_key, corrected_block = self.generate_key(input_block)
        
        # Если блок был исправлен, обновляем поле ввода
        if corrected_block != input_block.upper().strip():
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, corrected_block)
        
        # Отображаем ключ
        key_var.set(full_key)

class AnimatedCube:
    def __init__(self, root):
        self.root = root
        
        # Создаем Canvas для рисования с прозрачным фоном
        self.canvas = tk.Canvas(root, width=100, height=100, highlightthickness=0)
        self.canvas.pack(pady=25, padx=25)
        
        # Делаем Canvas прозрачным
        self.canvas.configure(highlightthickness=0)
        
        # Центр canvas
        self.center_x = 50
        self.center_y = 50

        # Угол поворота
        self.rotation = 0
        
        # Вершины куба (8 вершин)
        self.vertices = [
            [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],  # задняя грань
            [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]       # передняя грань
        ]
        
        # Рёбра куба (12 рёбер)
        self.edges = [
            # Задняя грань
            [0, 1], [1, 2], [2, 3], [3, 0],
            # Передняя грань
            [4, 5], [5, 6], [6, 7], [7, 4],
            # Соединяющие рёбра
            [0, 4], [1, 5], [2, 6], [3, 7]
        ]
        
        # Запускаем анимацию
        self.animate()
    
    def rotate_point(self, x, y, z, rx, ry):
        """Поворот точки по осям X и Y"""
        cos1, sin1 = math.cos(rx), math.sin(rx)
        cos2, sin2 = math.cos(ry), math.sin(ry)
        
        # Поворот по оси X
        y1 = y * cos1 - z * sin1
        z1 = y * sin1 + z * cos1
        
        # Поворот по оси Y
        x1 = x * cos2 + z1 * sin2
        z2 = -x * sin2 + z1 * cos2
        
        return [x1, y1, z2]
    
    def move_in_semicircle(self, x, y, z, angle):
        """Движение куба по полукругу"""
        radius = 80
        offset_x = math.cos(angle) * radius * 0.01
        offset_y = -abs(math.sin(angle)) * radius * 0.01
        return [x + offset_x, y + offset_y, z]
    
    def project(self, x, y, z):
        """Проекция 3D точки на 2D плоскость"""
        scale = 100
        distance = 5
        factor = scale / (distance + z)
        return [self.center_x + x * factor, self.center_y + y * factor]
    
    def draw_frame(self):
        """Отрисовка одного кадра анимации"""
        # Очищаем только линии куба
        self.canvas.delete("cube_lines")
        
        # Поворачиваем все вершины
        rotated_vertices = []
        for vertex in self.vertices:
            rotated = self.rotate_point(vertex[0], vertex[1], vertex[2], 
                                      self.rotation * 0.01, self.rotation * 0.01)
            rotated_vertices.append(rotated)
        
        # Применяем движение по полукругу
        translated_vertices = []
        for vertex in rotated_vertices:
            translated = self.move_in_semicircle(vertex[0], vertex[1], vertex[2], 
                                               self.rotation * 0.04)
            translated_vertices.append(translated)
        
        # Проецируем на 2D
        projected_vertices = []
        for vertex in translated_vertices:
            projected = self.project(vertex[0], vertex[1], vertex[2])
            projected_vertices.append(projected)
        
        # Рисуем рёбра
        for edge in self.edges:
            start, end = edge
            x1, y1 = projected_vertices[start]
            x2, y2 = projected_vertices[end]
            
            self.canvas.create_line(x1, y1, x2, y2, 
                                  fill='cyan', width=2, smooth=True, tags="cube_lines")
        
        # Увеличиваем угол поворота
        self.rotation += 1
    
    def animate(self):
        """Основной цикл анимации"""
        self.draw_frame()
        # Планируем следующий кадр через 16 мс (~60 FPS)
        self.root.after(16, self.animate)

def main():
    # Создаем главное окно
    root = tk.Tk()
    root.title("AutoDesktop KeyGen")
    root.geometry("630x300")
    root.resizable(False, False)
    
    # Фон
    bg_img = PhotoImage(file="bg.png")
    bg_label = tk.Label(root, image=bg_img)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    bg_label.image = bg_img
    
    # Кубик
    cube_animation = AnimatedCube(root)
    
    # Создаем генератор ключей
    key_gen = KeyGenerator()
    
    # Создаем Frame для элементов управления
    control_frame = tk.Frame(root, bg='black', relief='raised', bd=2)
    control_frame.place(x=50, y=220, width=530, height=60)
    
    # Поле для ввода первого блока ключа
    tk.Label(control_frame, text="Блок 1:", bg='black', fg='cyan', font=('Arial', 10, 'bold')).place(x=10, y=8)
    entry_block = tk.Entry(control_frame, font=('Courier', 10), width=8, justify='center')
    entry_block.place(x=70, y=8)
    
    # Переменная для ключа
    key_var = tk.StringVar()
    
    # Кнопка генерации
    generate_btn = tk.Button(control_frame, text="Сгенерировать ключ", 
                           command=lambda: key_gen.generate_and_update_ui(entry_block, key_var),
                           bg='cyan', fg='black', 
                           font=('Arial', 10, 'bold'), relief='raised')
    generate_btn.place(x=160, y=5)
    
    # Поле для отображения сгенерированного ключа
    tk.Label(control_frame, text="Ключ:", bg='black', fg='cyan', font=('Arial', 10, 'bold')).place(x=310, y=8)
    key_var = tk.StringVar()
    key_display = tk.Entry(control_frame, textvariable=key_var, font=('Courier', 10), 
                          width=20, justify='center', state='readonly', 
                          readonlybackground='black', fg='cyan')
    key_display.place(x=350, y=8)
    
    # Дополнительная информация
    info_label = tk.Label(control_frame, text="Формат: XXXXX-XXXXX-XXXXX (блок 2: +3 сдвиг, блок 3: -5 сдвиг)", 
                         bg='black', fg='gray', font=('Arial', 8))
    info_label.place(x=10, y=35)
    
    # Запускаем главный цикл tkinter
    root.mainloop()

if __name__ == "__main__":
    main()