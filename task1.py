import random
import timeit
import matplotlib.pyplot as plt
import numpy as np

# Реалізація сортування злиттям
def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left = arr[:mid]
        right = arr[mid:]

        merge_sort(left)
        merge_sort(right)

        i = j = k = 0

        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            k += 1

        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1

        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1

# Реалізація сортування вставками
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

# Функція для тестування
def test_sorting_algorithm(algorithm, data):
    def wrapper():
        arr = data.copy()
        algorithm(arr)
    return wrapper

# Генерація тестових даних
def generate_test_data(size, case='random'):
    if case == 'random':
        return [random.randint(0, 10000) for _ in range(size)]
    elif case == 'sorted':
        return list(range(size))
    elif case == 'reversed':
        return list(range(size, 0, -1))
    elif case == 'almost_sorted':
        arr = list(range(size))
        # Змінюємо кожен 10-й елемент
        for i in range(0, len(arr), 10):
            arr[i] = random.randint(0, size)
        return arr

# Тестування
sizes = [100, 1000, 5000, 10000, 20000]
cases = ['random', 'sorted', 'reversed', 'almost_sorted']
results = {'merge': {case: [] for case in cases},
           'insertion': {case: [] for case in cases},
           'timsort': {case: [] for case in cases}}

for size in sizes:
    for case in cases:
        data = generate_test_data(size, case)
        
        # Тестування merge sort
        merge_time = timeit.timeit(test_sorting_algorithm(merge_sort, data), number=1)
        results['merge'][case].append(merge_time)
        
        # Тестування insertion sort (тільки для малих масивів через O(n^2))
        if size <= 5000:
            insertion_time = timeit.timeit(test_sorting_algorithm(insertion_sort, data), number=1)
            results['insertion'][case].append(insertion_time)
        else:
            results['insertion'][case].append(float('inf'))
        
        # Тестування вбудованого sorted (Timsort)
        timsort_time = timeit.timeit(test_sorting_algorithm(sorted, data), number=1)
        results['timsort'][case].append(timsort_time)

# Візуалізація результатів
def plot_results(case):
    plt.figure(figsize=(10, 6))
    x = sizes
    
    # Обмежуємо розміри для insertion sort для кращого відображення
    max_size_for_insertion = 5000
    x_insertion = [s for s in sizes if s <= max_size_for_insertion]
    y_insertion = results['insertion'][case][:len(x_insertion)]
    
    plt.plot(x, results['merge'][case], label='Merge Sort', marker='o')
    plt.plot(x_insertion, y_insertion, label='Insertion Sort', marker='s')
    plt.plot(x, results['timsort'][case], label='Timsort (sorted)', marker='^')
    
    plt.xlabel('Розмір масиву')
    plt.ylabel('Час виконання (секунди)')
    plt.title(f'Час сортування для випадку: {case}')
    plt.legend()
    plt.grid(True)
    plt.xscale('log')
    plt.yscale('log')
    plt.show()

for case in cases:
    plot_results(case)