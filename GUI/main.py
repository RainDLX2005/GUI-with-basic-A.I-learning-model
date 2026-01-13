import sys
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from GUI import Ui_MainWindow
from matplotlib.figure import Figure 
from PyQt5.QtWidgets import QGraphicsScene

from weather_api import get_hourly_forecast
from regression import predict_next_24h_from_csv


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.load_weather()

        forecast = get_hourly_forecast()["list"]
        real, predicted = predict_next_24h_from_csv("df_weather.csv")
        self.plot_prediction(real, predicted)

    def plot_prediction(self, real, predicted):
        view_width = self.ui.graphicsView.width()
        view_height = self.ui.graphicsView.height()

        dpi = 100
        fig = Figure(figsize=(view_width / dpi, view_height / dpi), dpi=dpi)
        canvas = FigureCanvas(fig)

        ax = fig.add_subplot(111)

        step = 3  
        hours_real = list(range(0, len(real) * step, step))
        hours_pred = list(range(hours_real[-1] + step,
                        hours_real[-1] + step * (len(predicted) + 1),step))

        time_labels = [f"{h % 24}:00" for h in hours_real + hours_pred]


        ax.plot(hours_real, real, label="Observed", linewidth=2)
        ax.plot(
            [hours_real[-1]] + hours_pred,
            [real[-1]] + list(predicted),
            "--o",
            label="Predicted (next 24h)",
            linewidth=2
        )
        ax.set_xticks(hours_real + hours_pred)
        ax.set_xticklabels(time_labels, rotation=45)


        ax.set_xlabel("Time (hours)")
        ax.set_ylabel("Temperature (°C)")
        ax.set_title("Temperature Prediction for Next 24 Hours")
        ax.grid(True)
        ax.legend()
        ax.set_xlim(hours_real[-12], hours_real[-1] + 24)

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