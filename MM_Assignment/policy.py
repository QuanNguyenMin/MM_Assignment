#HƯỚNG DẪN SỬ DỤNG NẾU KHÔNG THỂ CHẠY PROJECT!
#
#DOWNLOAD PROJECT TẠI: https://github.com/MrH4554N/MM_Assignment
#
#Yêu cầu:
#  Python 3.11 trở lên
#  Các thư viện yêu cầu
#    numpy
#    matplotlib
#
# Cài đặt thư viện
#  Mở terminal và chạy lệnh cài đặt thư viện: pip install numpy matplotlib
#
# Cách sử dụng
#   Tải 2 file main.py và policy.py, lưu chung 1 folder
#   Cài đặt các thư viện cần thiết
#   Chạy chương trình bằng cách gõ lệnh trên terminal: python main.py
#
# Các giá trị cần nhập:
#   Chiều dài, chiều rộng miếng vật liệu vật ban đầu (Rectangle Width, Rectangle Height)
#   Kích thước các mảnh cần cắt và số lượng (Slice Width, Slice Height, Demand)
#   Sau khi nhập các giá trị cần thiết, ấn Start Program để bắt đầu chương trình


import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from tkinter import *
from tkinter import ttk, font, messagebox

class Rectangle:
    def __init__(self, width, height, x=0, y=0):
        self.width = width
        self.height = height
        self.x = x
        self.y = y

    def area(self):
        return self.width * self.height


def check_zero(matrix, i, j, new_height, new_width):
    for m in range(i, new_height):
        for n in range(j, new_width):
            if matrix[m][n] != 0:
                return False
    return True

areas_dict = {}
def fit(rectangles, chromosome, return_matrix=False):
    if not return_matrix:
        if chromosome in areas_dict:
            return areas_dict[chromosome]

    material_matrix = np.zeros((material.height, material.width))
    area = material.area()

    for i in range(len(rectangles)):
        if chromosome[i] == "1" :
            j, k = 0, 0
            while j < material.height and k < material.width :
                if material_matrix[j][k] == 0:
                    new_height = j + rectangles[i].height
                    new_width = k + rectangles[i].width
                    if new_height <= material.height and new_width <= material.width:
                        if check_zero(material_matrix, j, k, new_height, new_width):
                            area -= rectangles[i].area()
                            for m in range(j, new_height):
                                for n in range(k, new_width):
                                    material_matrix[m][n] = i + 1
                            break

                    new_height = j + rectangles[i].width
                    new_width = k + rectangles[i].height
                    if new_height <= material.height and new_width <= material.width:
                        if check_zero(material_matrix, j, k, new_height, new_width):
                            area -= rectangles[i].area()
                            for m in range(j, new_height):
                                for n in range(k, new_width):
                                    material_matrix[m][n] = i + 1
                            break

                k += 1
                if k == material.width:
                    k = 0
                    j += 1

    areas_dict[chromosome] = area

    if return_matrix:
        return material_matrix
    else:
        return area


def is_valid_chromosome(rectangles, chromosome):
    temp_area = 0

    for i in range(len(rectangles)):
        if chromosome[i] == "1" :
            temp_area += rectangles[i].area()

    return fit(rectangles, chromosome) == material.area() - temp_area



def initialize_population(population_size, individual_count, rectangles):
    population = []
    while len(population) < population_size:
        new_chromosome = "".join(random.choice("01") for _ in range(individual_count))

        if is_valid_chromosome(rectangles, new_chromosome):
            population.append(new_chromosome)

    return population


def tournament_selection(population, individual_count, rectangles):
    def fitness(chromosome):
        return fit(rectangles, chromosome)

    parents = random.sample(population, individual_count)
    return min(parents, key=fitness)


def natural_selection(individuals, individual_count):
    return individuals[:individual_count]


def sorting(individuals, rectangles):
    return sorted(individuals, key=lambda x: fit(rectangles, x))


def roulette_selection(parents):
    pairs = []
    for i in range(0, len(parents), 2):
        chances = []
        for i in range(len(parents)):
            chances.append((len(parents) - i) * random.random())
        if chances[0] >= chances[1]:
            max1 = 0
            max2 = 1
        else:
            max1 = 1
            max2 = 0

        for i in range(2, len(parents)):
            if chances[i] > chances[max1]:
                max2 = max1
                max1 = i
            elif chances[i] > chances[max2]:
                max2 = 1
        pairs.append([parents[max1], parents[max2]])

    return pairs

def crossover(pairs, rectangles):
    length = len(pairs[0][0])
    children = []

    for (a, b) in pairs:
        while True:
            r1 = random.randrange(0, length)
            r2 = random.randrange(0, length)

            if r1 < r2:
                d1 = a[:r1] + b[r1:r2] + a[r2:]
                d2 = b[:r1] + a[r1:r2] + b[r2:]

                if is_valid_chromosome(rectangles, d1) and is_valid_chromosome(rectangles, d2):
                    children.append(d1)
                    children.append(d2)
                    break
            else:
                d1 = a[:r2] + b[r2:r1] + a[r1:]
                d2 = b[:r2] + a[r2:r1] + b[r1:]
                if is_valid_chromosome(rectangles, d1) and is_valid_chromosome(rectangles, d2):
                    children.append(d1)
                    children.append(d2)
                    break

    return children

def inverse_mutation(individuals, percentage, rectangles):
    mutated_individuals = []

    for individual in individuals:
        while True:
            if random.random() < percentage and len(individual) > 1:
                r1 = random.randrange(0, len(individual) - 1)
                r2 = random.randrange(0, len(individual) - 1)

                if r1 < r2:
                    mutated = individual[:r1] + individual[r1:r2][::-1] + individual[r2:]
                    if is_valid_chromosome(rectangles, mutated):
                        mutated_individuals.append(mutated)
                        break
                else:
                    mutated = individual[:r2] + individual[r2:r1][::-1] + individual[r1:]
                    if is_valid_chromosome(rectangles, mutated):
                        mutated_individuals.append(mutated)
                        break

            else:
                mutated_individuals.append(individual)
                break

    return mutated_individuals

def elitism(old_individuals, mutated_individuals, elitism_rate, population_size):
    old_individual_size = int(np.round(population_size * elitism_rate))
    return old_individuals[:old_individual_size] + mutated_individuals[:(population_size - old_individual_size)]

def cost(rectangles, chromosome):
    return fit(rectangles, chromosome) / material.area()


def draw_rectangle(matrix):
    # Create a color map to map values to colors
    cmap = plt.get_cmap('jet')
    # Normalize the matrix values to the range [0, 1]
    norm = plt.Normalize(vmin=np.min(matrix), vmax=np.max(matrix))
    # Create a figure
    fig, ax = plt.subplots()
    # Plot the matrix as a rectangle with each element represented as a square
    ax.imshow(matrix, cmap=cmap, norm=norm)
    # Remove the axis labels
    ax.set_xticks([])
    ax.set_yticks([])
    # Create a custom legend
    unique_values = np.unique(matrix)
    patches = []
    for value in unique_values:
        color = cmap(norm(value))
        patches.append(mpatches.Patch(color=color, label=str(int(value))))
    ax.legend(handles=patches, bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    # Display the figure
    plt.show()

def remaining_percentage(rectangles, chromosome):
    if chromosome in areas_dict:
        return areas_dict[chromosome] / material.area() * 100
    else:
        return fit(rectangles, chromosome) / material.area() * 100


class InputForm(Tk):
    def __init__(self):
        self.slices = []
        self.material_width = 0
        self.material_height = 0

        super().__init__()

        self.geometry("470x450")
        self.title("Input Form")

        input_font = font.Font(size=15)
        label_font = font.Font(size=15)

        style = ttk.Style()
        style.configure("TEdge.TEntry",
                        background="white",
                        fieldbackground="white",
                        foreground="black",
                        relief="solid",
                        bordercolor="black",
                        borderwidth=2,
                        padding=5,
                        font=input_font,
                        )

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        label_1 = Label(self, text="Slice Width:", font=label_font)
        label_2 = Label(self, text="Slice Height:", font=label_font)
        label_5 = Label(self, text="Demand:", font=label_font)
        label_3 = Label(self, text="Rectangle Width:", font=label_font)
        label_4 = Label(self, text="Rectangle Height:", font=label_font)

        vcmd = (self.register(self.validate), '%P')
        self.input_1 = ttk.Entry(self, style="TEdge.TEntry", validate="key", validatecommand=vcmd)
        self.input_2 = ttk.Entry(self, style="TEdge.TEntry", validate="key", validatecommand=vcmd)
        self.input_5 = ttk.Entry(self, style="TEdge.TEntry", validate="key", validatecommand=vcmd)
        self.input_3 = ttk.Entry(self, style="TEdge.TEntry", validate="key", validatecommand=vcmd)
        self.input_4 = ttk.Entry(self, style="TEdge.TEntry", validate="key", validatecommand=vcmd)

        # Tạo TreeView để hiển thị các miếng cắt
        self.tree = ttk.Treeview(self, columns=("Slice Width", "Slice Height","Demand"), show="headings")
        self.tree.column("Slice Width", width=70, anchor='center')
        self.tree.heading("Slice Width", text="Slice Width")
        self.tree.column("Slice Height", width=70, anchor='center')
        self.tree.heading("Slice Height", text="Slice Height")
        self.tree.column("Demand", width=50, anchor='center')
        self.tree.heading("Demand", text="Demand")

        # Đặt vị trí các thành phần
        self.tree.place(x=20, y=20, width=200, height=200)

        label_1.place(x=250, y=20)
        self.input_1.place(x=250, y=50, width=150, height=25)

        label_2.place(x=250, y=80)
        self.input_2.place(x=250, y=110, width=150, height=25)

        label_5.place(x=250, y=140)
        self.input_5.place(x=250, y=170, width=150, height=25)

        label_3.place(x=20, y=250)
        self.input_3.place(x=20, y=280, width=170, height=25)

        label_4.place(x=20, y=310)
        self.input_4.place(x=20, y=340, width=170, height=25)

        # Tạo các nút
        myfont = font.Font(family='Arial', size=10, weight='bold')
        self.button1 = Button(self, text="Add Slice", font=myfont, command=self.add_to_table)
        self.button1.place(x=250, y=210, width=130, height=35)

        self.button2 = Button(self, text="Start Program", font=myfont, command=self.start_program)
        self.button2.place(x=20, y=380, width=130, height=35)

    def validate(self, P):
        return P.isdigit() or P == ""

    def add_to_table(self):
        slice_width = self.input_1.get()
        slice_height = self.input_2.get()
        slice_demand = self.input_5.get()
        
        if slice_width.isdigit() and slice_height.isdigit() and slice_demand.isdigit():
            self.tree.insert("", "end", values=(slice_width, slice_height, slice_demand))
            self.slices.append([int(slice_width), int(slice_height), int(slice_demand)])
            self.input_1.delete(0, 'end')
            self.input_2.delete(0, 'end')
            self.input_5.delete(0, 'end')
        else:
            messagebox.showerror("Error", "Please enter valid numbers!")

    def start_program(self):
        material_width = self.input_3.get()
        material_height = self.input_4.get()

        if material_width.isdigit() and material_height.isdigit() and len(self.slices) > 0:
            self.material_width = int(material_width)
            self.material_height = int(material_height)
            self.process_data()
            self.destroy()
        else:
            messagebox.showerror("Error", "Please enter all required data!")

    def process_data(self):
        # Tạo các đối tượng Rectangle
        global material, rectangles
        material = Rectangle(self.material_width, self.material_height)
        rectangles = []
    
        # Tạo đủ số lượng hình chữ nhật dựa trên yêu cầu (demand) của từng miếng cắt
        for width, height, demand in self.slices:
            for _ in range(demand):  # Add multiple rectangles for slices based on their demand
                rectangles.append(Rectangle(width, height))
    
        # Các tham số thuật toán di truyền
        population_size = 50
        individual_count = len(rectangles)
        generations = 100
        elitism_rate = 0.1
        mutation_rate = 0.1

        # Chạy thuật toán
        population = initialize_population(population_size, individual_count, rectangles)
        best_individual = None

        for _ in range(generations):
            sorted_population = sorting(population, rectangles)
            parents = roulette_selection(sorted_population)
            children = crossover(parents, rectangles)
            mutated_children = inverse_mutation(children, mutation_rate, rectangles)
            population = elitism(sorted_population, mutated_children, elitism_rate, population_size)
            best_individual = min(population, key=lambda x: fit(rectangles, x))

        # Hiển thị kết quả
        result_area = fit(rectangles, best_individual)
        remaining_percentage = (result_area / material.area()) * 100

        # Tạo cửa sổ kết quả
        result_window = Toplevel()
        result_window.title("Results")
        result_window.geometry("300x150")

        Label(result_window, text=f"Remaining Area Percentage: {remaining_percentage:.2f}%", 
          font=("Arial", 12)).pack(pady=10)

        # Vẽ hình ảnh kết quả
        draw_rectangle(fit(rectangles, best_individual, return_matrix=True))
