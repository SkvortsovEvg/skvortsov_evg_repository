def list_2_text_in_draw(input_list, diff=25):
    output_list = []
    tmp_list = []
    x_pos = 40
    y_pos = 150
    label = {
        20: " м/с",
        30: " мм.рт.ст.",
        31: "%",
    }
    for i in range(2, 4):
        for j in range(0, 2):
            tmp_list.append([x_pos, y_pos])
            y_pos += diff
            if i * 10 + j in label:
                if i * 10 + j == 20:
                    tmp_var = f"{input_list[i][j]}" + label[i * 10 + j] + f" {input_list[2][1]}"
                    tmp_list.append(tmp_var)
                    output_list.append(tmp_list.copy())
                    tmp_list.clear()
                    continue
            if i * 10 + j == 21:
                tmp_list.clear()
                y_pos -= diff
                continue
            tmp_var = f"{input_list[i][j]}" + label[i * 10 + j]
            tmp_list.append(tmp_var)
            output_list.append(tmp_list.copy())
            tmp_list.clear()
            tmp_var = ""

    x_pos = 180
    y_pos = 150
    for i in range(5, 7):
        if i == 5:
            for j in range(3):
                tmp_list.append([x_pos, y_pos])
                y_pos += diff
                tmp_list.append(f"{str(input_list[i][j])}")
                output_list.append(tmp_list.copy())
                tmp_list.clear()
        else:
            x_pos = 290
            for j in range(len(input_list[i])):
                if j == 0:
                    y_pos = 150
                tmp_list.append([x_pos, y_pos])
                y_pos += diff
                tmp_list.append(input_list[i][j])
                output_list.append(tmp_list.copy())
                tmp_list.clear()

    return output_list
