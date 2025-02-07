import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

def calculate_average(measurements):
    return np.mean(measurements) if measurements else float('nan')

def calculate_standard_uncertainty(measurements):
    return (np.std(measurements, ddof=1) / np.sqrt(len(measurements))) if len(measurements) > 1 else float('nan')

def calculate_repeatability(measurements):
    return np.std(measurements, ddof=1) if len(measurements) > 1 else float('nan')

def main():
    # Dil seçimi
    language = st.selectbox("Dil / Language", ["Türkçe", "English"])
    
    # Metinler
    texts = {
        "Türkçe": {
            "title": "Belirsizlik Hesaplama Uyguluması, B. Yalçınkaya",
            "days": ['1. Gün', '2. Gün', '3. Gün'],
            "measurement_prompt": "{day} İçin Ölçüm Sonucu Girin",
            "repeat": "{day} - Tekrar {i}",
            "extra_uncertainty": "{day} İçin Ekstra Belirsizlik Bileşeni (Opsiyonel)",
            "calculate": "Sonuçları Hesapla",
            "results": "Sonuçlar",
            "average": "Ortalama",
            "uncertainty": "Belirsizlik",
            "expanded_uncertainty": "Genişletilmiş Belirsizlik (k=2)",
            "repeatability": "Tekrarlanabilirlik",
            "general_results": "Genel Sonuçlar",
            "general_average": "Genel Ortalama",
            "between_days": "Günler Arası Tekrarlanabilirlik",
            "within_days": "Güç İçi Tekrarlanabilirlik",
            "general_uncertainty": "Belirsizlik",
            "error_bar": "Hata Barı Grafiği",
        },
        "English": {
            "title": "Uncertainty Calculation App, B. Yalçınkaya",
            "days": ['Day 1', 'Day 2', 'Day 3'],
            "measurement_prompt": "Enter Measurement Results for {day}",
            "repeat": "{day} - Repeat {i}",
            "extra_uncertainty": "Extra Uncertainty Component for {day} (Optional)",
            "calculate": "Calculate Results",
            "results": "Results",
            "average": "Average",
            "uncertainty": "Uncertainty",
            "expanded_uncertainty": "Expanded Uncertainty (k=2)",
            "repeatability": "Repeatability",
            "general_results": "General Results",
            "general_average": "General Average",
            "between_days": "Between Days Repeatability",
            "within_days": "Within Days Repeatability",
            "general_uncertainty": "Uncertainty",
            "error_bar": "Error Bar Graph",
        }
    }
    
    t = texts[language]
    
    st.title(t["title"])
    days = t["days"]
    total_measurements = []
    uncertainty_components = []
    
    for day in days:
        st.subheader(t["measurement_prompt"].format(day=day))
        measurements = []
        for i in range(5):
            value = st.number_input(t["repeat"].format(day=day, i=i+1), value=0.0, step=0.01, format="%.2f", key=f"{day}_{i}")
            measurements.append(value)
        total_measurements.append(measurements)
        
        uncertainty_component = st.number_input(t["extra_uncertainty"].format(day=day), value=0.0, step=0.01, format="%.4f", key=f"unc_{day}")
        uncertainty_components.append(uncertainty_component)
    
    if st.button(t["calculate"]):
        repeatability_values = []
        avg_values = []
        uncertainty_values = []
        
        for i, day in enumerate(days):
            avg = calculate_average(total_measurements[i])
            uncertainty = calculate_standard_uncertainty(total_measurements[i])
            expanded_uncertainty = uncertainty * 2  # k=2 genişletilmiş belirsizlik
            repeatability = calculate_repeatability(total_measurements[i])
            total_uncertainty = np.sqrt(uncertainty**2 + uncertainty_components[i]**2)
            expanded_total_uncertainty = total_uncertainty * 2  # k=2 genişletilmiş belirsizlik
            
            st.write(f"### {day} {t['results']}")
            st.write(f"**{t['average']}:** {avg:.4f}")
            st.write(f"**{t['uncertainty']}:** {total_uncertainty:.4f}")
            st.write(f"**{t['expanded_uncertainty']}:** {expanded_total_uncertainty:.4f}")
            st.write(f"**{t['repeatability']}:** {repeatability:.4f}")
            repeatability_values.extend(total_measurements[i])
            avg_values.append(avg)
            uncertainty_values.append(total_uncertainty)
        
        overall_measurements = [value for day in total_measurements for value in day]
        overall_avg = calculate_average(overall_measurements)
        overall_uncertainty = calculate_standard_uncertainty(overall_measurements)
        expanded_overall_uncertainty = overall_uncertainty * 2  # k=2 genişletilmiş belirsizlik
        repeatability_within_days = calculate_repeatability(repeatability_values)
        repeatability_between_days = calculate_repeatability(avg_values)
        
        st.write(f"## {t['general_results']}")
        st.write(f"**{t['general_average']}:** {overall_avg:.4f}")
        st.write(f"**{t['between_days']}:** {repeatability_between_days:.4f}")
        st.write(f"**{t['within_days']}:** {repeatability_within_days:.4f}") 
        st.write(f"**{t['general_uncertainty']}:** {overall_uncertainty:.4f}")
        st.write(f"**{t['expanded_uncertainty']}:** {expanded_overall_uncertainty:.4f}")
        
        # Hata barı grafiği
        fig, ax = plt.subplots()
        ax.errorbar(days, avg_values, yerr=uncertainty_values, fmt='o', capsize=5, capthick=2, ecolor='red')
        ax.set_xlabel("Days")
        ax.set_ylabel("Measurement Average")
        ax.set_title(t["error_bar"])
        st.pyplot(fig)

if __name__ == "__main__":
    main()
