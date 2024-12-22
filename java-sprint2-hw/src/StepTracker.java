import java.util.Scanner;

public class StepTracker {
    Scanner scanner;
    Converter converter = new Converter();
    MonthData monthData;
    MonthData[] monthToData = new MonthData[12];
    int goalByStepsPerDay = 10000;

    StepTracker(Scanner scanner) {
        this.scanner = scanner;
        for (int i = 0; i < monthToData.length; i++) {
            monthToData[i] = new MonthData();
        }
    }

    void addNewNumberStepsPerDay() {
        System.out.println("Введите номер месяца:");
        int month = scanner.nextInt();
        if (month < 1 || month > 12) {
            System.out.println("Номер вводимого месяца должен быть от 1 до 12 включительно");
            return;
        }
        System.out.println("Введите день от 1 до 30 (включительно)");
        int day = scanner.nextInt();
        if (day < 1 || day > 30) {
            System.out.println("Номер вводимого дня должен быть от 1 до 30 включительно");
            return;
        }
        System.out.println("Введите количество шагов");
        int steps = scanner.nextInt();
        if (steps < 0) {
            System.out.println("Количество шагов должно быть положительным числом");
            return;
        }
        MonthData monthData = monthToData[month - 1];
        monthData.days[day - 1] = steps;
        System.out.println("Количество шагов успешно записано!");
    }

    void changeStepGoal(int newGoalByStepsPerDay) {
        goalByStepsPerDay = newGoalByStepsPerDay;
        System.out.println("Цель в " + newGoalByStepsPerDay + " шага(-ов) успешно записана!");
    }

    void printStatistic() {
        System.out.println("Введите номер месяца");
        int month = scanner.nextInt();
        if (month < 1 || month > 12) {
            System.out.println("Номер вводимого месяца должен быть от 1 до 12 включительно");
            return;
        }
        monthData = monthToData[month - 1];
        int sumSteps = monthData.sumStepsFromMonth();
        System.out.println("Статистика за выбранный месяц:");
        monthData.printDaysAndStepsFromMonth();
        System.out.println("За месяц пройдено " + sumSteps + " шага(-ов)");
        System.out.println("Максимальное пройденное количество шагов в день: " + monthData.maxSteps());
        System.out.println("Среднее пройденное количество шагов за месяц: "
                + (sumSteps / monthData.days.length));
        System.out.println("Пройденная за месяц дистанция составила "
                + converter.convertToKm(sumSteps) + " километра(-ов)");
        System.out.println("Всего за месяц при ходьбе вы сожгли "
                + converter.convertStepsToKilocalories(sumSteps) + " килокалорий");
        System.out.println("Лучшая серия по достижению цели составила "
                + monthData.bestSeries(goalByStepsPerDay) + " дней подряд");
        System.out.println();
    }
}
