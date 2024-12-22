import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        StepTracker stepTracker = new StepTracker(scanner);

        while (true) {
            printMenu();
            int command = scanner.nextInt();
            if (command == 1) {
                stepTracker.addNewNumberStepsPerDay();
            } else if (command == 2) {
                System.out.println("Введите новую цель по количеству шагов в день");
                int newDailyGoal = scanner.nextInt();
                if (newDailyGoal <= 0) {
                    System.out.println("Цель должна быть положительным числом.");
                } else {
                    stepTracker.changeStepGoal(newDailyGoal);
                }
            } else if (command == 3) {
                stepTracker.printStatistic();
            } else if (command == 0) {
                System.out.println("Приложение завершено. До скорой встречи!");
                return;
            } else {
                System.out.println("Такой команды нет");
            }
            System.out.println();
            System.out.println("-".repeat(20));
            System.out.println();
        }
    }

    static void printMenu() {
        System.out.println("Выберите номер команды: ");
        System.out.println("1. Ввести количество шагов за определённый день");
        System.out.println("2. Изменить цель по количеству шагов в день;");
        System.out.println("3. Показать статистику за определённый месяц;");
        System.out.println("0. Выход");
    }
}