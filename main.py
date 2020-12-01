from coin_amount_calculate import calculate_amount
import cv2

if __name__ == "__main__":
    for i in range(1, 10):
        coins = cv2.imread(f"input_image/coin_set_{i}.jpg", 1)
        calculate_amount(coins, i)
