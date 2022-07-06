def SpaceInNumber(number):
    number = str(number)
    shape_clean = ""
    count = 0
    for n in range(0, len(number))[::-1]:
        if count == 3:
            shape_clean = " "+shape_clean
            count = 0

        shape_clean = f"{number[n]}"+shape_clean
        count += 1

    return shape_clean


