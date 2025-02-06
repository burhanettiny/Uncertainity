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
    st.title("Belirsizlik Hesaplama Uyguluması, B. Yalçınkaya")
    days = ['1. Gün', '2. Gün', '3. Gün']
    total_measurements = []
    uncertainty_components = []
    
    for day in days:
        st.subheader(f"{day} İçin Ölçüm Sonucu Girin")
        measurements = []
        for i in range(5):
            value = st.number_input(f"{day} - Tekrar {i+1}", value=0.0, step=0.01, format="%.2f", key=f"{day}_{i}")
            measurements.append(value)
        total_measurements.append(measurements)
        
        uncertainty_component = st.number_input(f"{day} İçin Ekstra Belirsizlik Bileşeni (Opsiyonel)", value=0.0, step=0.01, format="%.4f", key=f"unc_{day}")
        uncertainty_components.append(uncertainty_component)
    
    if st.button("Sonuçları Hesapla"):
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
            
            st.write(f"### {day} Sonuçları")
            st.write(f"**Ortalama:** {avg:.4f}")
            st.latex(r"U = \sqrt{u^2 + u_{ek}^2}")
            st.write(f"**Belirsizlik:** {total_uncertainty:.4f}")
            st.latex(r"U_{exp} = 2U")
            st.write(f"**Genişletilmiş Belirsizlik (k=2):** {expanded_total_uncertainty:.4f}")
            st.latex(r"s_r = \sqrt{\frac{\sum (x_i - \bar{x})^2}{n-1}}")
            st.write(f"**Tekrarlanabilirlik:** {repeatability:.4f}")
            repeatability_values.extend(total_measurements[i])
            avg_values.append(avg)
            uncertainty_values.append(total_uncertainty)
        
        overall_measurements = [value for day in total_measurements for value in day]
        overall_avg = calculate_average(overall_measurements)
        overall_uncertainty = calculate_standard_uncertainty(overall_measurements)
        expanded_overall_uncertainty = overall_uncertainty * 2  # k=2 genişletilmiş belirsizlik
        repeatability_within_days = calculate_repeatability(repeatability_values)
        repeatability_between_days = calculate_repeatability(avg_values)
        
        st.write("## Genel Sonuçlar")
        st.write(f"**Genel Ortalama:** {overall_avg:.4f}")
        st.latex(r"U_{genel} = \sqrt{\frac{\sum (x_i - \bar{x})^2}{n(n-1)}}")
        st.write(f"**Günler Arası Tekrarlanabilirlik:** {repeatability_between_days:.4f}")
        st.write(f"**Güç İçi Tekrarlanabilirlik:** {repeatability_within_days:.4f}") 
        st.write(f"**Genel Belirsizlik:** {overall_uncertainty:.4f}")
        st.latex(r"U_{exp,genel} = 2U_{genel}")
        st.write(f"**Genişletilmiş Genel Belirsizlik (k=2):** {expanded_overall_uncertainty:.4f}")
        
        # Hata barı grafiği
        fig, ax = plt.subplots()
        ax.errorbar(days, avg_values, yerr=uncertainty_values, fmt='o', capsize=5, capthick=2, ecolor='red')
        ax.set_xlabel("Günler")
        ax.set_ylabel("Ölçüm Ortalaması")
        ax.set_title("Hata Barı Grafiği")
        st.pyplot(fig)

if __name__ == "__main__":
    main()
