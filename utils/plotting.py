import matplotlib.pyplot as plt

def plot_predictions(y_true, y_pred, title="Tahmin vs Gerçek"):
    plt.figure(figsize=(12, 5))
    plt.plot(y_true.values, label="Gerçek", marker="o", linestyle="--")
    plt.plot(y_pred, label="Tahmin", marker="x", linestyle="-")
    plt.title(title)
    plt.xlabel("Veri Nokası")
    plt.ylabel("Units Sold")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
