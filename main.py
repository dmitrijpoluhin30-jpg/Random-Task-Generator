import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import json
import os

# 1. Список предопределённых задач по категориям
TASKS = {
    "учёба": ["Прочитать статью", "Решить задачу", "Посмотреть лекцию", "Написать конспект"],
    "спорт": ["Сделать зарядку", "Пробежаться", "Потренироваться", "Сделать растяжку"],
    "работа": ["Написать отчёт", "Провести встречу", "Проверить почту", "Составить план"]
}

class TaskGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Task Generator")
        self.root.geometry("450x500")
        
        # Загрузка истории из файла
        self.history = self.load_history()
        
        # Текущий выбранный фильтр
        self.current_category = tk.StringVar(value="все")
        
        # Создаем интерфейс
        self.create_widgets()
        
    def create_widgets(self):
        """Создает все элементы GUI."""
        
        # Кнопка генерации задачи
        self.generate_btn = tk.Button(self.root, text="Сгенерировать задачу", font=("Arial", 12), command=self.generate_task)
        self.generate_btn.pack(pady=10)
        
        # Поле для отображения текущей задачи
        self.task_label = tk.Label(self.root, text="", font=("Arial", 14, "bold"), wraplength=400)
        self.task_label.pack(pady=15)
        
        # Блок фильтрации
        filter_frame = tk.LabelFrame(self.root, text="Фильтр по типу", padx=10, pady=10)
        filter_frame.pack(pady=5, fill="x")
        
        categories = ["все"] + list(TASKS.keys())
        for cat in categories:
            rb = tk.Radiobutton(filter_frame, text=cat, variable=self.current_category, value=cat)
            rb.pack(anchor="w")
            
        # Кнопка добавления новой задачи (для проверки ввода)
        self.add_task_btn = tk.Button(self.root, text="Добавить свою задачу", command=self.add_custom_task)
        self.add_task_btn.pack(pady=10)
        
        # Блок истории
        history_frame = tk.LabelFrame(self.root, text="История сгенерированных задач", padx=10, pady=10)
        history_frame.pack(padx=20, pady=5, fill="both", expand=True)
        
        self.history_listbox = tk.Listbox(history_frame, width=50, height=12)
        self.history_listbox.pack(side="left")
        
        scrollbar = tk.Scrollbar(history_frame, orient="vertical")
        scrollbar.config(command=self.history_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.history_listbox.config(yscrollcommand=scrollbar.set)
        
    def generate_task(self):
        """Генерирует случайную задачу с учетом фильтра."""
        category = self.current_category.get()
        
        if category == "все":
            all_tasks = [task for sublist in TASKS.values() for task in sublist]
            task = random.choice(all_tasks)
        else:
            task = random.choice(TASKS[category])
            
        self.task_label.config(text=task)
        
        # Добавляем в историю и сохраняем
        self.history.append(task)
        self.save_history()
        
    def load_history(self):
        """Загружает историю из файла JSON."""
        if os.path.exists('tasks.json'):
            try:
                with open('tasks.json', 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []
    
    def save_history(self):
        """Сохраняет историю в файл JSON и обновляет список на экране."""
        with open('tasks.json', 'w') as f:
            json.dump(self.history, f)
            
        # Обновляем виджет списка
        self.history_listbox.delete(0, tk.END)
        for task in self.history:
            self.history_listbox.insert(tk.END, task)
    
    def add_custom_task(self):
        """Добавляет новую задачу с проверкой на пустую строку."""
        new_task = simpledialog.askstring("Новая задача", "Введите текст новой задачи:")
        
        if new_task is None: # Пользователь нажал Отмена
            return
            
        new_task = new_task.strip()
        
        if not new_task: # Проверка на пустую строку или пробелы
            messagebox.showerror("Ошибка ввода", "Задача не может быть пустой!")
            return
            
        # Добавляем в категорию "работа" (можно изменить логику)
        TASKS["работа"].append(new_task)
        
# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = TaskGeneratorApp(root)
    root.mainloop()