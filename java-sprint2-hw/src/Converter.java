public class Converter {
    int stepToCm = 75;
    int stepToCal = 50;

    int convertToKm(int steps) {
        return steps * stepToCm / 100000;
    }

    int convertStepsToKilocalories(int steps) {
        return steps * stepToCal / 1000;
    }
}
