import java.util.Scanner;

public class Main {

    /*A. Если в тексте между словами присутствует несколько пробелов подряд, надо оставить только один из них.
    Для реализации этого подпункта нельзя пользоваться методами replace() и replaceAll().
    */
    private static String aLessSpaces(String line) {
        StringBuilder answer = new StringBuilder(); //Можно изменять в отличие от String
        boolean isSpace = false;
        for (int index = 0; index < line.length(); index++) {
            if (line.charAt(index) == ' ') {            //Возвращает значение char по указанному индексу
                if (!isSpace) {
                    answer.append(line.charAt(index));
                }
                isSpace = true;
            } else {
                answer.append(line.charAt(index));
                isSpace = false;
            }
        }
        return answer.toString();
    }

    /*B. Если в тексте присутствует знак минус (-), это значит, что символ слева от этого знака надо поменять местами с
    символом, который стоит справа от этого знака. Обратите внимание, что символом может быть не только буква, но и
    цифра или любой другой знак/символ, в том числе символ пробела. После смены символов местами, знак минус (-) надо
    удалить из строки результата.
    */
    private static String bReplaceCharsMinus(String line) {
        StringBuilder answer = new StringBuilder();
        for (int index = 0; index < line.length(); index++) {
            if (line.charAt(index) == '-') {
                answer.deleteCharAt(answer.length() - 1);
                answer.append(line.charAt(index + 1));
                answer.append(line.charAt(index - 1));
                index++;
            } else {
                answer.append(line.charAt(index));
            }
        }
        return answer.toString();
    }

    /*C. Если в тексте присутствует знак плюс (+), вам необходимо заменить его на восклицательный знак (!)
    P.S. Как я понял, то здесь можно использовать replace(), но не как в пункте А.*/
    private static String cReplacePlus(String line) {
        return line.replace("+", "!");
    }

    /*D. В тексте могут присутствовать цифры (от 0 до 9). Вам необходимо посчитать их сумму и удалить из текста.
    Сумму цифр вам нужно добавить в конец результирующей строки через пробел (пробел должен стоять перед суммой цифр).
    Если цифр в тексте не было - "0" (ноль) в конце строки выводить не нужно.
    */
    private static String dSumInText(String line) {
        StringBuilder answer = new StringBuilder();
        int sum = 0;
        for (int index = 0; index < line.length(); index++) {
            char ch = line.charAt(index);
            if (Character.isDigit(ch)) {
                sum += Character.getNumericValue(ch);
            } else {
                answer.append(ch);
            }
        }
        if (sum != 0) {
            answer.append(" ").append(sum);
        }
        return answer.toString();
    }

    public static String textModifier() {
        Scanner sc = new Scanner(System.in);
        String line = sc.nextLine();
        sc.close();

        /*Все манипуляции с текстом должны выполняться ровно в той последовательности, которая описана в пункте 2.
        То есть, сначала выполняется пункт A, затем пункт B, затем C и D.
        Это важно для получения корректного итогового результата.
        */
        return dSumInText(cReplacePlus(bReplaceCharsMinus(aLessSpaces(line))));
    }

    public static void main(String[] args) {
        /*
        Пимер ввода №1: генрих1  играет+2   л-июбит0школу
        Пример вывода: генрих играет! илюбитшколу 3

        Пример ввода №2: Я ю-лбю-л джаву   всем сердцем+
        Пример вывода: Я люблю джаву всем сердцем!
        */
        System.out.println(textModifier());
    }
}