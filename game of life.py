import unittest
from concurrent.futures import ThreadPoolExecutor
import ita

# Hàm đếm số ô sống xung quanh
def count_neighbor(data, i, j):
    # Đếm số hàng và cột của data
    rows = len(data)
    cols = len(data[0])
    # Khởi tạo giá trị count ban đầu
    count = 0
    # Duyệt tất cả phần tử xung quanh 
    
    for x in range(i-1, i+2): # Có thể duyệt qua được cả ô bên trái, phải và chính ô [i][j]
        for y in range(j-1, j+2):
            if 0 <= x < rows and 0 <= y < cols and (x != i or y != j): # Kiểm tra điều kiện của x và y (<= 0 bởi chỉ số index của mảng xét từ 0 đồng thời phải nằm trong khoảng số hàng và cột của data, x khác i và y khác j để count không tính ô mà ta đang kiểm tra)
                count += data[x][y]
    
    return count

# Hàm tính toán trạng thái tiếp theo của ô tuân theo luật của trò chơi
def lifegame_rule(cur, neighbor):
    # Khi ô = 1 tức ô sống
    if cur == 1:
        if neighbor < 2 or neighbor > 3:
            return 0
        else:
            return 1
    
    # Khi ô = 0 tức ô chết
    else:
        if neighbor == 3:
            return 1
        else:
            return 0

# Hàm tính toán bước tiếp theo của trò chơi
def lifegame_step(data):
    rows = len(data)
    cols = len(data[0])
    # Tạo mảng mới có cùng kích thước với mảng ban đầu (2 chiều)
    new_data = ita.array.make2d(rows, cols)
    # Xét tất cả các phần tử trong mảng, áp dụng 2 hàm trên để tính giá trị của phần từ đó tại bước tiếp theo (0 hoặc 1)
    
    for i in range(rows):
        for j in range(cols):
            neighbor = count_neighbor(data, i, j)
            new_data[i][j] = lifegame_rule(data[i][j], neighbor)
    
    return new_data
    
# Hàm chạy trò chơi trong một số bước nhất định
def lifegame(data, steps):
    # Tạo mảng 1 chiều có kích thước "steps", mỗi phần tử ghi lại trạng thái của bảng tại một bước.
    results = ita.array.make1d(steps)
    # Giá trị đầu tiên của mảng "results" là data ban đầu
    results[0] = data
    
    print(f"Step 0:")
    for row in data:
        print(row)
    
    for step in range(1, steps):
        # Tính các data tại các bước tiếp theo rồi gán vào mảng "results"
        data = lifegame_step(data)
        results[step] = data
        # In kết quả sau mỗi bước
        print(f"\nStep {step}:")
        for row in data:
            print(row)
    
    return results

# Thực hiện unittest 
class TestGameOfLife(unittest.TestCase):
    
    def test_count_neighbor(self):
        data = [
            [0, 1, 1],
            [0, 0, 0],
            [1, 0, 0]
        ]
        result = count_neighbor(data, 1, 1)  # Ô (1,1) có 3 ô sống xung quanh
        self.assertEqual(result, 3)

    def test_lifegame_rule(self):
        result = lifegame_rule(0, 3)  # Ô chết và có 3 ô sống xung quanh -> Ô sống
        self.assertEqual(result, 1)
        result = lifegame_rule(1, 2)  # Ô sống và có 2 ô sống xung quanh -> Ô sống
        self.assertEqual(result, 1)
        result = lifegame_rule(1, 1)  # Ô sống và có 1 ô sống xung quanh -> Ô chết
        self.assertEqual(result, 0)

    def test_lifegame_step(self):
        data = [
            [0, 1, 1],
            [0, 0, 0],
            [1, 0, 0]
        ]
        result = lifegame_step(data)
        self.assertEqual(result, [
            [0, 0, 0],
            [0, 1, 0],
            [0, 0, 0]
        ])

# Hàm chạy song song với ThreadPoolExecutor
def run_parallel_tests():
    with ThreadPoolExecutor() as executor:
        # Tạo một danh sách các test case
        test_suite = unittest.TestLoader().loadTestsFromTestCase(TestGameOfLife)
        
        # Chạy các test cases song song
        futures = [executor.submit(unittest.TextTestRunner().run, test_suite)]
        
        for future in futures:
            future.result()  # Chờ đợi kết quả từ các test case

if __name__ == '__main__':
    # Chạy kiểm thử song song
    run_parallel_tests()





