def calculate_status(average, absences):
    total_classes = 60
    absence_percentage = absences / total_classes * 100

    if absence_percentage > 25:
        return "Reprovado por Falta"
    elif average < 50:
        return "Reprovado por Nota"
    elif 50 <= average < 70:
        return "Exame Final"
    elif average >= 70:
        return "Aprovado"

def calculate_final_passing_grade(average, status):
    if status == "Exame Final":
        return round((2 * 50) - average)
    else:
        return 0