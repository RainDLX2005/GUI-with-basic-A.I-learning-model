import sys
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from GUI import Ui_MainWindow
from matplotlib.figure import Figure 
from PyQt5.QtWidgets import QGraphicsScene

from weather_api import get_hourly_forecast
from regression import predict_from_csv


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.load_weather()

        forecast = get_hourly_forecast()["list"]
        real, predicted = predict_from_csv("df_weather.csv")
        self.plot_prediction(real, predicted)

    def plot_prediction(self, real, predicted):
        view_width = self.ui.graphicsView.width()
        view_height = self.ui.graphicsView.height()

        dpi = 100
        fig = Figure(figsize=(view_width / dpi, view_height / dpi), dpi=dpi)
        canvas = FigureCanvas(fig)

        ax = fig.add_subplot(111)

        days_real = list(range(len(real))) 
        days_pred = list(range(len(real), len(real) + len(predicted)))

        day_labels = (
            [f"Day-{len(real)-i}" for i in range(len(real), 0, -1)][::-1]
            + [f"Day+{i+1}" for i in range(len(predicted))]
        )

        ax.plot(days_real, real, label="Observed (history)", linewidth=2)

        ax.plot(
            [days_real[-1]] + days_pred,
            [real[-1]] + list(predicted),
            "--o",
            label="Predicted (next days)",
            linewidth=2
        )

        ax.set_xticks(days_real + days_pred)
        ax.set_xticklabels(day_labels, rotation=45)
        ax.set_xlabel("Day")
        ax.set_ylabel("Temperature (°C)")
        ax.set_title("Daily Temperature Prediction (Next 8 Days)")
        ax.grid(True)
        ax.legend()

        ax.set_xlim(max(0, len(real) - 10), len(real) + len(predicted))

        fig.tight_layout()

        scene = QGraphicsScene()
        scene.addWidget(canvas)
        self.ui.graphicsView.setScene(scene)
        scene.setSceneRect(0, 0, view_width, view_height)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
