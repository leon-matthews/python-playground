
import random


fruit = [
    'watermelon',
    'raspberry',
    'papaya',
    'mandarin',
    'tangerine',
    'honeydew',
    'cherry',
]



if __name__ == '__main__':
    data = fruit.copy()
    random.shuffle(data)
    print(data)

    num_swaps = 0
    while True:
        has_swapped = False
        previous_index = previous = None
        for index, current in enumerate(data):
            if previous is not None and current < previous:
                count = f"{num_swaps + 1}."
                print(f"{count:<3} Swap {current} and {previous}")
                data[previous_index] = current
                data[index] = previous
                current = previous
                num_swaps += 1
                has_swapped = True
            previous_index, previous = index, current

        print(data)

        if has_swapped == 0:
            break

    print(data)
