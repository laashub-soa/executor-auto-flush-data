if __name__ == '__main__':
    with open('test.txt', 'r')as f:
        content_lines = f.readlines()
    print(content_lines)
    occur_times_3 = []
    temp_counter = {}
    for item in content_lines:
        item = item.strip()
        item = item[:item.rfind('-')]
        item = item[:item.rfind('-')]
        if item in temp_counter:
            temp_counter[item] += 1
            if temp_counter[item] > 2:
                if item not in occur_times_3:
                    occur_times_3.append(item)
        else:
            temp_counter[item] = 1
    print(temp_counter)

    print("occur_times_3", "-" * 200)
    print(occur_times_3)
