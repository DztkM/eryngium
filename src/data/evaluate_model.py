import numpy as np
import matplotlib.pyplot as plt
from typing import List


def evaluate_model(model_history, real_data, plot=True):
    # ACTIVE CASES COMPARISON

    model_I = np.array(model_history["I"], dtype=int)
    real_I = np.array(real_data["I"], dtype=int)
    
    L = min(len(model_I), len(real_I))
    model_I = model_I[:L]
    real_I = real_I[:L]

    mae_active = np.mean(np.abs(model_I - real_I))
    mse_active = np.mean((model_I - real_I) ** 2)
    rmse_active = np.sqrt(mse_active)

    metrics_active = {
        "MAE": mae_active,
        "MSE": mse_active,
        "RMSE": rmse_active,
    }

    # CUMULATIVE CASES COMPARISON
    
    model_cum = np.array(model_history["I_cumulative"], dtype=int)
    real_cum = np.array(real_data["I_cum"], dtype=int)

    Lc = min(len(model_cum), len(real_cum))
    model_cum = model_cum[:Lc]
    real_cum = real_cum[:Lc]
    

    mae_cum = np.mean(np.abs(model_cum - real_cum))
    mse_cum = np.mean((model_cum - real_cum) ** 2)
    rmse_cum = np.sqrt(mse_cum)

    metrics_cumulative = {
        "MAE": mae_cum,
        "MSE": mse_cum,
        "RMSE": rmse_cum,
    }

    # PLOTTING
    if plot:

        # Active cases plot
        plt.figure(figsize=(10, 5))
        plt.plot(real_I, label="Real active cases", linewidth=2)
        plt.plot(model_I, label="Model active cases", linestyle='--')
        plt.title("Model vs Real — Active Cases")
        plt.xlabel("Day")
        plt.ylabel("Active infections")
        plt.legend()
        plt.grid(True)
        plt.show()

        # Cumulative cases plot
        plt.figure(figsize=(10, 5))
        plt.plot(real_cum, label="Real cumulative cases", linewidth=2)
        plt.plot(model_cum, label="Model cumulative cases", linestyle='--')
        plt.title("Model vs Real — Cumulative Cases")
        plt.xlabel("Day")
        plt.ylabel("Cumulative infections")
        plt.legend()
        plt.grid(True)
        plt.show()

        # Error metrics plot
        plt.figure(figsize=(8, 5))
        
        labels = ["Active MAE", "Active MSE", "Active RMSE",
                  "Cumulative MAE", "Cumulative MSE", "Cumulative RMSE"]
        values = [
            mae_active, mse_active, rmse_active,
            mae_cum, mse_cum, rmse_cum
        ]

        plt.bar(labels, values)
        plt.xticks(rotation=45, ha='right')
        plt.title("Error Metrics (Active & Cumulative)")
        plt.ylabel("Error value")
        plt.grid(axis='y')
        plt.yscale("log")
        plt.tight_layout()
        plt.show()

    # RETURN BOTH METRIC SETS
    return {
        "active": metrics_active,
        "cumulative": metrics_cumulative
    }