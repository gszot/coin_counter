import cv2
DEBUG_PRINT = False


def detect_coins(coins, i):
    gray = cv2.cvtColor(coins, cv2.COLOR_BGR2GRAY)
    #img = cv2.medianBlur(gray, 7)
    blur_scale = 7
    img = cv2.medianBlur(gray, blur_scale)
    circles = cv2.HoughCircles(
        img,  # source image
        cv2.HOUGH_GRADIENT,  # type of detection
        1,
        50,
        param1=230,
        param2=50,
        minRadius=10,  # minimal radius
        maxRadius=380,  # max radius
        #param1=200,
        #param2=50,
        #minRadius=30,  # minimal radius
        #maxRadius=170,  # max radius
    )

    coins_copy = coins.copy()
    coins_detected = None

    for detected_circle in circles[0]:
        x_coor, y_coor, detected_radius = detected_circle
        coins_detected = cv2.circle(
            coins_copy,
            (int(x_coor), int(y_coor)),
            int(detected_radius),
            (0, 255, 0),
            4,
        )

    cv2.imwrite(f"output_image/coins_test_Hough_{i}.jpg", coins_detected)

    return circles


def calculate_amount(coins, i):
    nominals = {
        "0.01 PLN": {
            "value": 0.01,
            "radius": 15.5,
            "ratio": 1,
            "count": 0,
        },
        "0.02 PLN": {
            "value": 0.02,
            "radius": 17.5,
            "ratio": 17.5/15.5,
            "count": 0,
        },
        "0.05 PLN": {
            "value": 0.05,
            "radius": 19.5,
            "ratio": 19.5/15.5,
            "count": 0,
        },
        "0.1 PLN": {
            "value": 0.1,
            "radius": 16.5,
            "ratio": 16.5/15.5,
            "count": 0,
        },
        "0.2 PLN": {
            "value": 0.2,
            "radius": 18.5,
            "ratio": 18.5/15.5,
            "count": 0,
        },
        "0.5 PLN": {
            "value": 0.5,
            "radius": 20.5,
            "ratio": 20.5/15.5,
            "count": 0,
        },
        "1 PLN": {
            "value": 1,
            "radius": 23,
            "ratio": 23/15.5,
            "count": 0,
        },
        "2 PLN": {
            "value": 2,
            "radius": 21.5,
            "ratio": 21.5/15.5,
            "count": 0,
        },
        "5 PLN": {
            "value": 5,
            "radius": 24,
            "ratio": 24/15.5,
            "count": 0,
        },
    }

    tolerance = 0.0375
    ################################testowe
    #tolerance = 0.025
    #scale = 1
    #blur_scale_x = 3
    #blur_scale_y = 3

    #coins_height, coins_width, coins_channel = coins.shape
    #coins_resized = cv2.resize(coins, (int(coins_width / scale), int(coins_height / scale)))
    #coins_blurred = cv2.GaussianBlur(coins_resized, (blur_scale_x, blur_scale_y), cv2.BORDER_DEFAULT)
    #cv2.imwrite("output_image/coins_blurred.jpg", coins_blurred)
    #circles = detect_coins(coins_blurred)
    ################################testowe
    circles = detect_coins(coins, i)

    radius = []
    coordinates = []

    for detected_circle in circles[0]:
        x_coor, y_coor, detected_radius = detected_circle
        radius.append(detected_radius)
        coordinates.append([x_coor, y_coor])

    smallest = min(radius)
    total_amount = 0

    coins_circled = cv2.imread(f"output_image/coins_test_Hough_{i}.jpg", 1)
    font = cv2.FONT_HERSHEY_SIMPLEX

    for coin in circles[0]:
        ratio_to_check = coin[2] / smallest
        coor_x = coin[0]
        coor_y = coin[1]
        for nominal in nominals:
            value = nominals[nominal]['value']
            if abs(ratio_to_check - nominals[nominal]['ratio']) <= tolerance:
                nominals[nominal]['count'] += 1
                total_amount += nominals[nominal]['value']
                cv2.putText(coins_circled, str(value), (int(coor_x), int(coor_y)), font, 1,
                            (0, 0, 0), 4)
                if DEBUG_PRINT:
                    cv2.putText(coins_circled, "rc"+str(round(ratio_to_check, 3)), (int(coor_x), int(coor_y-100)), font, 1,
                                (0, 0, 0), 4)
                    cv2.putText(coins_circled, "r"+str(round(nominals[nominal]['ratio'], 3)), (int(coor_x), int(coor_y - 60)), font, 1,
                                (0, 0, 0), 4)
                break
    if DEBUG_PRINT:
        cv2.putText(coins_circled, "rr" + str(round(nominals["0.5 PLN"]['ratio'], 3)), (int(170), int(300)), font, 1,
                    (0, 0, 0), 4)

    print(f"The total amount is {total_amount} PLN")
    for nominal in nominals:
        pieces = nominals[nominal]['count']
        print(f"{nominal} = {pieces}x")

    cv2.imwrite(f"output_image/coins_final_{i}.jpg", coins_circled)
    cv2.imshow("image", coins_circled)
    #cv2.waitKey()
