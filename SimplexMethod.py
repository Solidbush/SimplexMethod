from scipy.optimize import linprog
import json


obj = []
goal = ""
lhs_ineq = []
rhs_ineq = []
lhs_eq = []
rhs_eq = []
bnd = []

with open('input1.json') as f:
    file_content = f.read()
    templates_global = json.loads(file_content)


def process_iteration(iter_data):
    print(f"Сообщение с результатом решения: {iter_data.message}")
    print(f"Колличество итераций для решения: {iter_data.nit}")
    print(f"Статус решения: {iter_data.status}")
    print(f"Значения переменных решения: {repr(iter_data.x)}")


def parse_json(templates):
    global goal
    goal = templates["goal"]
    if goal == 'max':
        for item in templates["f"]:
            obj.append(item * -1)
    else:
        for item in templates["f"]:
            obj.append(item)
    for sample in templates["constraints"]:
        if sample['type'] == 'lte':
            lhs_ineq.append(sample['coefs'])
            rhs_ineq.append(sample['b'])
        elif sample['type'] == 'gte':
            list = sample['coefs']
            cor_list = []
            for item in list:
                cor_list.append(item * -1)
            lhs_ineq.append(cor_list)
            rhs_ineq.append(sample['b'] * -1)
        elif sample['type'] == 'eq':
            lhs_eq.append(sample['coefs'])
            rhs_eq.append(sample['b'])
    for items in obj:
        bnd.append((0, float("inf")))

    print("Входные данные: ")
    print(f"Коэффициенты целевой функции: {repr(obj)}")
    print(f"Направление оптимизации: {goal}")
    print(f"Коэффициенты из ограничений-неравенств (левая часть): {repr(lhs_ineq)}")
    print(f"Коэффициенты из ограничений-неравенств (правая часть): {repr(rhs_ineq)}")
    print(f"Коэффициенты из ограничивающего уравнения (левая часть): {repr(lhs_eq)}")
    print(f"Коэффициенты из ограничивающего уравнения (правая часть):{repr(rhs_eq)}")
    print(f"Границ каждой переменной: {repr(bnd)}")


parse_json(templates_global)
if len(lhs_ineq) > 0:
    opt = linprog(c=obj, A_eq=lhs_eq, b_eq=rhs_eq, b_ub=rhs_ineq, A_ub=lhs_ineq, bounds=bnd, method='simplex', callback=process_iteration)
else:
    opt = linprog(c=obj, A_eq=lhs_eq, b_eq=rhs_eq, bounds=bnd, method='simplex', callback=process_iteration)

print("")
print(f"Сообщение с результатом решения: {opt.message}")
print(f"Колличество итераций для решения: {opt.nit}")
if goal == 'max':
    print(f"Оптимальное значение целевой функции: {-opt.fun}")
else:
    print(f"Оптимальное значение целевой функции: {opt.fun}")
print(f"Статус решения: {opt.status}")
print(f"Оптимальные значения переменных решения: {repr(opt.x)}")
