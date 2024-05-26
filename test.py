def find_max_index_and_value(lst):
    if not lst:
        return None, None  # Trả về None nếu danh sách trống

    max_value = max(lst)  # Tìm giá trị lớn nhất trong danh sách
    max_index = lst.index(max_value)  # Tìm chỉ số của giá trị lớn nhất

    return max_index, max_value

# Ví dụ sử dụng
numbers = [1, 2,7, 3, 7, 5, 6]
index, value = find_max_index_and_value(numbers)
print(f"Giá trị lớn nhất là {value} ở vị trí {index}")
