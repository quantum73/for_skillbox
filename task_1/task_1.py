import logging

test_data = (
    (0, 1), (1, 1), (1, 2), (2, 1),
    (2, 2), (2, 3), (2, 4), (2, 5), (2, 6),
    (7, 3), (6, 3), (5, 3), (4, 3), (3, 3),
    (10, 11), (10, 19),
)

logging.basicConfig(level=logging.INFO)


def arrange_cars(general_count=None, general_element=None, extend_element=None, extend_count=None):
    if not general_count:
        raise ValueError("Параметр general_count обязательный!")
    if not isinstance(general_count, int):
        raise ValueError("Параметр general_count должен быть INT!")
    general_element = general_element or 'RW'
    extend_element = extend_element or ''
    extend_count = extend_count or 0

    result = [general_element for _ in range(general_count)]
    for i in range(extend_count):
        result[i] = f"{extend_element}{result[i]}"
    return ''.join(result)


def main():
    no_solution_msg = "Нет решения\n"

    for idx, (red_cars, white_cars) in enumerate(test_data):
        # check values
        logging.info(f"#{idx + 1} | red cars = {red_cars}, white cars = {white_cars}")
        if red_cars + white_cars < 2:
            logging.info(no_solution_msg)
            continue

        min_val = min(red_cars, white_cars)
        max_val = max(red_cars, white_cars)
        if max_val > min_val * 2:
            logging.info(no_solution_msg)
            continue

        # arrange cars
        general_count, general_element, extend_element, extend_count = None, None, None, None

        if red_cars == white_cars:
            general_count = red_cars
        elif red_cars > white_cars:
            general_count = white_cars
            general_element = 'WR'
            extend_element = 'R'
            extend_count = red_cars - white_cars
        elif red_cars < white_cars:
            general_count = red_cars
            extend_element = 'W'
            extend_count = white_cars - red_cars

        answer = arrange_cars(general_count, general_element, extend_element, extend_count)
        logging.info(f"{answer}\n")


if __name__ == '__main__':
    main()
